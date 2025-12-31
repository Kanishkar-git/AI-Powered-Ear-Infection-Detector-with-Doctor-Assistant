import streamlit as st
from inference_sdk import InferenceHTTPClient
import google.generativeai as genai


def get_roboflow_client():
    try:
        api_key = st.secrets["ROBOFLOW_API_KEY"]
    except KeyError:
        raise RuntimeError("ROBOFLOW_API_KEY not found in Streamlit secrets")

    return InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key=api_key
    )


def get_gemini_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except KeyError:
        raise RuntimeError("GEMINI_API_KEY not found in Streamlit secrets")


def get_gemini_client():
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    return genai
