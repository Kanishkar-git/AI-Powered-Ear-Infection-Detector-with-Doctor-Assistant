"""Response Parsing Utilities"""
import re
import json
import streamlit as st

def parse_gemini_response(response_text):
    """Parse Gemini response into structured sections"""
    sections = {
        'overview': '',
        'severity': '',
        'visual_reasoning': '',
        'timeline': '',
        'symptoms': [],
        'prevention': [],
        'red_flags': [],
        'disclaimer': '',
        'chart_data': {}
    }

    if not response_text:
        return sections

    # Extract JSON
    try:
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            json_text = json_match.group()
            sections['chart_data'] = json.loads(json_text)
    except Exception as e:
        st.warning(f"Could not parse chart data: {str(e)}")

    # Parse text sections
    lines = response_text.split("\n")
    current_section = None

    for line in lines:
        l = line.strip()
        
        if "SECTION 1" in l or "OVERVIEW" in l:
            current_section = "overview"
        elif "SECTION 2" in l or "SEVERITY" in l:
            current_section = "severity"
        elif "SECTION 3" in l or "VISUAL REASONING" in l:
            current_section = "visual_reasoning"
        elif "SECTION 4" in l or "TIMELINE" in l:
            current_section = "timeline"
        elif "SECTION 5" in l or "SYMPTOMS" in l:
            current_section = "symptoms"
        elif "SECTION 6" in l or "PREVENTION" in l:
            current_section = "prevention"
        elif "SECTION 7" in l or "RED-FLAG" in l or "ALERTS" in l:
            current_section = "red_flags"
        elif "SECTION 8" in l or "DISCLAIMER" in l:
            current_section = "disclaimer"
        elif current_section and l and not l.startswith("{"):
            if current_section in ["symptoms", "prevention", "red_flags"]:
                if l.startswith("-") or l.startswith("•") or l.startswith("*"):
                    sections[current_section].append(l.lstrip("-•* ").strip())
            else:
                sections[current_section] += l + " "

    return sections

def format_doctor_reply(text):
    if not text:
        return ""

    # Normalize whitespace
    text = text.strip().replace("\n", " ")

    # Protect decimal numbers like 91.7%
    text = re.sub(r'(\d)\.(\d)', r'\1<dot>\2', text)

    # Split into sentences safely
    sentences = re.split(r'(?<=[.!?])\s+', text)

    clean_sentences = []
    for s in sentences:
        s = s.replace("<dot>", ".").strip()
        if len(s) > 12:
            clean_sentences.append(s)

    # Enforce max 4 sentences
    clean_sentences = clean_sentences[:4]

    return "\n".join(clean_sentences)