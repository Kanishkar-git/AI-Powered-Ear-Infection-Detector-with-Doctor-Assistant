"""Session State Management"""
import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        "uploaded_image": None,
        "predictions": [],
        "processed_image": None,
        "detected_classes": [],
        "analysis": {},
        "chart_data": {},
        "detection_done": False,
        "report_generated": False,
        "report_data": None,
        "pdf_buffer": None,
        "patient_age": None,
        "medical_context": {},
        "chatbot": None,
        "chat_history": [],
        "pending_user_message": None
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value