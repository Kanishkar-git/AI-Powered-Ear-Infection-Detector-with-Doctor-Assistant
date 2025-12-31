import streamlit as st
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from config.api_config import get_gemini_api_key
from config.prompts import ENT_DOCTOR_SYSTEM_PROMPT
from utils.parser_utils import format_doctor_reply


# ------------------ FIX EVENT LOOP (CRITICAL) ------------------

def ensure_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


# ------------------ Medical Context ------------------

def get_medical_context_string(medical_context):
    if not medical_context:
        return "No scan data available."

    return f"""
Detected Condition: {medical_context.get('condition', 'Unknown')}
Confidence: {medical_context.get('confidence', 0):.1f}%
Patient Age: {medical_context.get('age', 'Not provided')}
Visual Indicators: {', '.join(medical_context.get('visual_features', []))}
"""


# ------------------ Initialize Chatbot ------------------

def initialize_langchain_chatbot(medical_context_str):
    try:
        ensure_event_loop()  # 🔥 REQUIRED FIX

        api_key = get_gemini_api_key()

        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            google_api_key=api_key,
            temperature=0.7,
            max_output_tokens=1200
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template=f"""
{ENT_DOCTOR_SYSTEM_PROMPT}

MEDICAL SCAN CONTEXT:
{medical_context_str}

RULES:
- Respond as Dr. Sarah Chen (ENT Specialist)
- Max 4 sentences
- Each sentence on a new line
- Clear medical explanation

Conversation History:
{{chat_history}}

Patient: {{input}}

Dr. Chen:
"""
        )

        return ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=False
        )

    except Exception as e:
        st.exception(e)
        return None


# ------------------ Get Response ------------------

def get_chatbot_response(chatbot, user_question):
    try:
        response = chatbot.predict(input=user_question)
        return format_doctor_reply(response)
    except Exception as e:
        st.exception(e)
        return "⚠️ The AI doctor is temporarily unavailable. Please try again."
