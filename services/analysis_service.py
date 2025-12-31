"""
Gemini Analysis Service
Handles clinical analysis, insights, and chart data generation
"""

import streamlit as st
import google.generativeai as genai
import json
import re

from config.api_config import get_gemini_api_key
from config.prompts import get_analysis_prompt
from utils.parser_utils import parse_gemini_response


# -------------------- Gemini Analysis Core --------------------

def get_advanced_gemini_response(
    detected_condition,
    confidence,
    patient_age=None,
    visual_features=None
):
    """Get comprehensive medical analysis from Gemini (SAFE & CLOUD-COMPATIBLE)"""

    if patient_age is None:
        patient_age = "Not provided"

    if visual_features is None:
        visual_features = [
            "Redness detected",
            "Inflammation visible",
            "Structural abnormalities"
        ]

    prompt = get_analysis_prompt(
        detected_condition,
        confidence,
        patient_age,
        visual_features
    )

    try:
        # ✅ Correct Gemini SDK usage
        genai.configure(api_key=get_gemini_api_key())

        model = genai.GenerativeModel("gemini-3-flash-preview")

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2500
            }
        )

        return response.text if response and response.text else None

    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None


# -------------------- Detection → Analysis Wrapper --------------------

def analyze_detection(predictions, patient_age):
    """Analyze detection results and return parsed analysis + chart data"""

    if not predictions:
        return {}, {}

    detected_condition = predictions[0]["class"]
    confidence = predictions[0]["confidence"] * 100

    response_text = get_advanced_gemini_response(
        detected_condition,
        confidence,
        patient_age,
        ["Redness detected", "Inflammation visible", "Structural changes"]
    )

    if not response_text:
        return {}, {}

    analysis = parse_gemini_response(response_text)
    chart_data = analysis.get("chart_data", {})

    return analysis, chart_data
