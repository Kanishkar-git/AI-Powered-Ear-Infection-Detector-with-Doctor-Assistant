"""Visualization Components"""
import plotly.graph_objects as go
import streamlit as st

def create_visualizations(chart_data):
    """Create interactive Plotly charts"""
    charts = {}
    
    if not chart_data:
        return charts
    
    try:
        # Confidence Gauge
        if 'detection_confidence' in chart_data:
            conf = chart_data['detection_confidence']['confidence_percent']
            fig_conf = go.Figure(go.Indicator(
                mode="gauge+number",
                value=conf,
                title={'text': "Detection Confidence"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 85], 'color': "gold"},
                        {'range': [85, 100], 'color': "limegreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_conf.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            charts['confidence'] = fig_conf
        
        # Symptom Probability
        if 'symptom_probability_distribution' in chart_data:
            symptoms = chart_data['symptom_probability_distribution']
            fig_symptoms = go.Figure(data=[
                go.Bar(
                    x=list(symptoms.keys()),
                    y=list(symptoms.values()),
                    marker_color='indianred',
                    text=list(symptoms.values()),
                    textposition='auto',
                )
            ])
            fig_symptoms.update_layout(
                title="Symptom Probability Distribution",
                xaxis_title="Symptoms",
                yaxis_title="Probability (%)",
                height=400,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            charts['symptoms'] = fig_symptoms
        
        # Infection Timeline
        if 'infection_progress_timeline' in chart_data:
            timeline = chart_data['infection_progress_timeline']
            fig_timeline = go.Figure(data=[
                go.Scatter(
                    x=list(timeline.keys()),
                    y=list(timeline.values()),
                    mode='lines+markers',
                    line=dict(color='firebrick', width=3),
                    marker=dict(size=10)
                )
            ])
            fig_timeline.update_layout(
                title="Predicted Infection Progression (3 Days)",
                xaxis_title="Day",
                yaxis_title="Severity Score (1-5)",
                height=400,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            charts['timeline'] = fig_timeline
        
        # Visual Features Pie Chart
        if 'visual_feature_contribution' in chart_data:
            features = chart_data['visual_feature_contribution']
            fig_features = go.Figure(data=[
                go.Pie(
                    labels=list(features.keys()),
                    values=list(features.values()),
                    hole=0.3
                )
            ])
            fig_features.update_layout(
                title="Visual Feature Contribution",
                height=400,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            charts['features'] = fig_features
        
        # Prevention Effectiveness
        if 'prevention_effectiveness' in chart_data:
            prevention = chart_data['prevention_effectiveness']
            fig_prevention = go.Figure(data=[
                go.Bar(
                    y=list(prevention.keys()),
                    x=list(prevention.values()),
                    orientation='h',
                    marker_color='lightseagreen',
                    text=list(prevention.values()),
                    textposition='auto',
                )
            ])
            fig_prevention.update_layout(
                title="Prevention Strategy Effectiveness",
                xaxis_title="Effectiveness Score (1-5)",
                yaxis_title="Prevention Strategy",
                height=400,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            charts['prevention'] = fig_prevention
            
    except Exception as e:
        st.warning(f"Could not generate all visualizations: {str(e)}")
    
    return charts