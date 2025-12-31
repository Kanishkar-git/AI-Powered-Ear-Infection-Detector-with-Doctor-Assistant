"""Gemini Analysis Service"""
import streamlit as st
from config.api_config import get_gemini_client
from config.prompts import get_analysis_prompt
from utils.parser_utils import parse_gemini_response

def get_advanced_gemini_response(detected_condition, confidence, patient_age=None, visual_features=None):
    """Get comprehensive medical analysis from Gemini"""
    
    if patient_age is None:
        patient_age = "Not provided"
    if visual_features is None:
        visual_features = ["Redness detected", "Inflammation visible", "Structural abnormalities"]
    
    prompt = get_analysis_prompt(detected_condition, confidence, patient_age, visual_features)
    
    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt,
            config={
                'temperature': 0.7,
                'max_output_tokens': 2500,
            }
        )
        
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'candidates') and len(response.candidates) > 0:
            return response.candidates[0].content.parts[0].text
        else:
            return None
            
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None

def analyze_detection(predictions, patient_age):
    """Analyze detection results"""
    if not predictions:
        return {}, {}
    
    detected_condition = predictions[0]['class']
    confidence = predictions[0]['confidence'] * 100
    
    response = get_advanced_gemini_response(
        detected_condition,
        confidence,
        patient_age,
        ["Redness detected", "Inflammation visible", "Structural changes"]
    )
    
    if response:
        analysis = parse_gemini_response(response)
        chart_data = analysis.get('chart_data', {})
        return analysis, chart_data
    
    return {}, {}