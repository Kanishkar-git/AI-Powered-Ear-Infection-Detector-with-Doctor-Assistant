"""AI ENT Doctor Assistant - Main Application"""
import streamlit as st
from datetime import datetime

# Import services
from services.detection_service import run_detection, build_medical_context
from services.analysis_service import analyze_detection
from services.chatbot_service import (
    initialize_langchain_chatbot, 
    get_medical_context_string,
    get_chatbot_response
)
from services.report_service import generate_pdf_report

# Import UI components
from ui.styles import get_custom_css
from ui.visualizations import create_visualizations

# Import utilities
from utils.session_utils import initialize_session_state
from utils.image_utils import process_detection_image

# Page Config
st.set_page_config(page_title="AI ENT Doctor Assistant", page_icon="👂", layout="wide")

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Header
st.markdown("<div class='header'>", unsafe_allow_html=True)
st.title("👂 AI ENT Doctor Assistant")
st.markdown("*Hospital-Grade Detection with Expert AI Consultation*")
st.markdown("</div>", unsafe_allow_html=True)

# Main Layout
tab1, tab2, tab3 = st.tabs(["🔬 Detection & Analysis", "👨‍⚕️ Consult ENT Doctor", "📋 Generate Report"])

# ==================== TAB 1: DETECTION ====================
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.subheader("📸 Image Upload & Detection")
        
        patient_age_input = st.number_input("Patient Age (Optional)", min_value=0, max_value=150, value=0, key="age_input")
        if patient_age_input > 0:
            st.session_state.patient_age = patient_age_input
        
        uploaded_file = st.file_uploader("Upload ear image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if uploaded_file:
            from PIL import Image
            st.session_state.uploaded_image = Image.open(uploaded_file)
        
        if st.session_state.uploaded_image:
            st.image(st.session_state.uploaded_image, caption="Uploaded Image", use_container_width=True)
            
            if st.button("🔍 Run Detection", use_container_width=True, type="primary"):
                with st.spinner("Analyzing image..."):
                    try:
                        predictions = run_detection(st.session_state.uploaded_image)
                        
                        if predictions and len(predictions) > 0:
                            st.session_state.processed_image = process_detection_image(
                                st.session_state.uploaded_image, 
                                predictions
                            )
                            
                            st.session_state.detected_classes = [p.get('class', 'Unknown') for p in predictions]
                            st.session_state.predictions = predictions
                            
                            # Build medical context
                            st.session_state.medical_context = build_medical_context(
                                predictions, 
                                st.session_state.patient_age
                            )
                            
                            # Initialize chatbot
                            medical_context_str = get_medical_context_string(st.session_state.medical_context)
                            st.session_state.chatbot = initialize_langchain_chatbot(medical_context_str)
                            st.session_state.chat_history = []
                            
                            st.session_state.analysis = {}
                            st.session_state.chart_data = {}
                        else:
                            st.warning("No infections detected in the image.")
                        
                        st.session_state.detection_done = True
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Detection failed: {str(e)}")
        
        if st.session_state.detection_done and st.session_state.processed_image:
            st.image(st.session_state.processed_image, caption="Detection Result", use_container_width=True)

    with col_right:
        st.subheader("📊 Clinical Analysis")
        
        if st.session_state.detection_done:
            if st.session_state.detected_classes:
                # Detection Results
                st.markdown("### ✅ Detected Conditions")
                for i, p in enumerate(st.session_state.predictions):
                    with st.container(border=True):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"**{p['class']}**")
                        with col2:
                            confidence = p['confidence']*100
                            st.metric("Confidence", f"{confidence:.2f}%")
                
                # Generate Analysis
                if not st.session_state.analysis:
                    with st.spinner("Generating clinical insights..."):
                        st.session_state.analysis, st.session_state.chart_data = analyze_detection(
                            st.session_state.predictions,
                            st.session_state.patient_age
                        )
                
                # Display Analysis
                if st.session_state.analysis:
                    analysis = st.session_state.analysis
                    
                    if analysis.get('overview'):
                        st.markdown("#### 📋 Overview")
                        st.info(analysis['overview'])
                    
                    if analysis.get('severity'):
                        st.markdown("#### ⚠️ Severity Assessment")
                        confidence = st.session_state.predictions[0]['confidence'] * 100
                        if confidence < 60:
                            st.success(analysis['severity'])
                        elif confidence < 85:
                            st.warning(analysis['severity'])
                        else:
                            st.error(analysis['severity'])
                    
                    # Display Charts
                    if st.session_state.chart_data:
                        st.markdown("#### 📈 Visual Analytics")
                        
                        charts = create_visualizations(st.session_state.chart_data)
                        
                        if 'confidence' in charts:
                            st.plotly_chart(charts['confidence'], use_container_width=True, key="conf_chart")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'symptoms' in charts:
                                st.plotly_chart(charts['symptoms'], use_container_width=True, key="symp_chart")
                        with col2:
                            if 'timeline' in charts:
                                st.plotly_chart(charts['timeline'], use_container_width=True, key="time_chart")
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            if 'features' in charts:
                                st.plotly_chart(charts['features'], use_container_width=True, key="feat_chart")
                        with col4:
                            if 'prevention' in charts:
                                st.plotly_chart(charts['prevention'], use_container_width=True, key="prev_chart")
                    
                    # Additional sections
                    if analysis.get('symptoms'):
                        with st.expander("🩺 Probable Symptoms", expanded=False):
                            for symptom in analysis['symptoms']:
                                st.markdown(f"• {symptom}")
                    
                    if analysis.get('prevention'):
                        with st.expander("🛡️ Prevention & Care Guidance", expanded=False):
                            for prev in analysis['prevention']:
                                st.markdown(f"• {prev}")
                    
                    if analysis.get('red_flags'):
                        with st.expander("🚨 Red-Flag Alerts", expanded=False):
                            st.error("Seek immediate medical attention if you experience:")
                            for flag in analysis['red_flags']:
                                st.markdown(f"• {flag}")
                    
                    if analysis.get('disclaimer'):
                        st.markdown("---")
                        st.caption(analysis['disclaimer'])

# ==================== TAB 2: ENT DOCTOR CHAT ====================
with tab2:
    st.markdown("<div class='doctor-badge'>👨‍⚕️ Dr. Sarah Chen, ENT Specialist</div>", unsafe_allow_html=True)
    
    if not st.session_state.detection_done:
        st.warning("⚠️ Please complete the detection in Tab 1 before consulting the doctor.")
        st.info("The AI doctor needs scan results to provide accurate medical guidance.")
    else:
        # Display medical context
        with st.expander("📋 View Scan Context", expanded=False):
            st.markdown("<div class='scan-context-box'>", unsafe_allow_html=True)
            context = st.session_state.medical_context
            st.write(f"**Detected Condition:** {context.get('condition', 'Unknown')}")
            st.write(f"**Confidence:** {context.get('confidence', 0):.1f}% ({context.get('confidence_label', 'unknown')})")
            st.write(f"**Patient Age:** {context.get('age', 'Not provided')}")
            st.write(f"**Visual Features:** {', '.join(context.get('visual_features', []))}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Medical Disclaimer
        st.markdown("""
        <div class='medical-disclaimer'>
        <b>⚕️ Medical Disclaimer:</b> This AI consultation supports clinical understanding. 
        It does not replace physical examination or professional diagnosis by a qualified ENT specialist.
        </div>
        """, unsafe_allow_html=True)
        
        # Chat History Display
        st.markdown("### 💬 Consultation")
        chat_container = st.container(height=500)
        
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div class='doctor-message chat-message'>
                <b>Dr. Chen:</b><br>
                Hello! I've reviewed your ear scan results. I'm here to help you understand the findings 
                and answer any questions you may have. What would you like to know?
                </div>
                """, unsafe_allow_html=True)
            
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div class='user-message chat-message'>
                    <b>You:</b><br>{msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='doctor-message chat-message'>
                    <b>Dr. Chen:</b><br>{msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Process pending message
        if st.session_state.pending_user_message:
            user_question = st.session_state.pending_user_message
            
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_question
            })
            
            with st.spinner("Dr. Chen is typing..."):
                if st.session_state.chatbot is None:
                    medical_context_str = get_medical_context_string(st.session_state.medical_context)
                    st.session_state.chatbot = initialize_langchain_chatbot(medical_context_str)
                
                formatted_response = get_chatbot_response(st.session_state.chatbot, user_question)
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': formatted_response
            })
            
            st.session_state.pending_user_message = None
            st.rerun()
        
        # Chat Input
        st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([5, 1])
        with col1:
            user_question = st.text_input(
                "Ask Dr. Chen about your scan results...",
                key="user_input",
                placeholder="e.g., What does this infection mean? Is this serious?"
            )
        with col2:
            send_button = st.button("Send", use_container_width=True, type="primary")
        
        if send_button and user_question and st.session_state.pending_user_message is None:
            st.session_state.pending_user_message = user_question
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick question buttons
        st.markdown("#### 💡 Common Questions:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("What is this condition?", use_container_width=True):
                st.session_state.pending_user_message = 'Can you explain what this condition means?'
                st.rerun()
        
        with col2:
            if st.button("How serious is this?", use_container_width=True):
                st.session_state.pending_user_message = 'How serious is this infection?'
                st.rerun()
        
        with col3:
            if st.button("What should I do next?", use_container_width=True):
                st.session_state.pending_user_message = 'What are the next steps I should take?'
                st.rerun()

# ==================== TAB 3: GENERATE REPORT ====================
with tab3:
    st.subheader("📋 Generate Medical Report")
    
    if not st.session_state.detection_done:
        st.warning("⚠️ Please complete detection in Tab 1 first.")
    else:
        st.info("Generate a comprehensive PDF report with all detection results and analysis.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id = st.text_input("Patient ID", value="PAT-" + datetime.now().strftime("%Y%m%d-%H%M"))
            patient_name = st.text_input("Patient Name", value="John Doe")
        
        with col2:
            patient_age_report = st.number_input("Age", min_value=0, max_value=150, 
                                                value=st.session_state.patient_age if st.session_state.patient_age else 30)
            patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        doctor_notes = st.text_area("Doctor's Notes (Optional)", 
                                    placeholder="Add any additional observations or recommendations...")
        
        if st.button("🔄 Generate PDF Report", use_container_width=True, type="primary"):
            with st.spinner("Generating comprehensive medical report..."):
                report_data = {
                    'report_id': f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'report_date': datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                    'patient': {
                        'id': patient_id,
                        'name': patient_name,
                        'age': patient_age_report,
                        'gender': patient_gender
                    },
                    'detection': {
                        'infections': [
                            {
                                'name': p['class'],
                                'confidence': f"{p['confidence']*100:.2f}%"
                            }
                            for p in st.session_state.predictions
                        ]
                    },
                    'analysis': st.session_state.analysis,
                    'doctor_notes': doctor_notes if doctor_notes else "None provided"
                }
                
                st.session_state.report_data = report_data
                st.session_state.pdf_buffer = generate_pdf_report(report_data, st.session_state.processed_image)
                st.session_state.report_generated = True
                st.success("✅ Report generated successfully!")
        
        if st.session_state.report_generated and st.session_state.pdf_buffer:
            st.download_button(
                label="📥 Download PDF Report",
                data=st.session_state.pdf_buffer,
                file_name=f"ear_infection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            
            # Report Preview
            with st.expander("📄 Report Preview", expanded=False):
                if st.session_state.report_data:
                    rd = st.session_state.report_data
                    st.markdown(f"**Report ID:** {rd['report_id']}")
                    st.markdown(f"**Patient:** {rd['patient']['name']} ({rd['patient']['age']}y, {rd['patient']['gender']})")
                    st.markdown(f"**Date:** {rd['report_date']}")
                    
                    st.markdown("**Detected Conditions:**")
                    for inf in rd['detection']['infections']:
                        st.markdown(f"- {inf['name']} ({inf['confidence']})")
                    
                    if rd.get('doctor_notes') != "None provided":
                        st.markdown(f"**Doctor's Notes:** {rd['doctor_notes']}")

# Footer
st.markdown("---")
st.caption("🏥 AI ENT Doctor Assistant | Powered by Roboflow CV, Google Gemini & LangChain | For medical guidance only")