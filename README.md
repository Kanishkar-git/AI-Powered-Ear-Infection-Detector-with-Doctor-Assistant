# 👂 AI ENT Doctor Assistant

A comprehensive AI-powered medical application for ear infection detection and consultation, combining computer vision, advanced language models, and medical expertise.

## 🌟 Features

- **🔬 AI-Powered Detection**: Hospital-grade ear infection detection using Roboflow CV
- **👨‍⚕️ Virtual ENT Consultation**: Interactive chat with AI ENT specialist Dr. Sarah Chen
- **📊 Visual Analytics**: Comprehensive charts and medical insights
- **📋 PDF Reports**: Professional medical reports with patient data
- **💬 Context-Aware Chat**: LangChain-powered conversational AI with medical context

## 🏗️ Project Structure

```
ai-ent-doctor-assistant/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Dependencies
├── .streamlit/
│   └── secrets.toml           # API keys (create this)
├── config/
│   ├── __init__.py
│   ├── api_config.py          # API configuration
│   └── prompts.py             # System prompts
├── services/
│   ├── __init__.py
│   ├── detection_service.py   # Detection logic
│   ├── analysis_service.py    # Analysis logic
│   ├── chatbot_service.py     # Chatbot logic
│   └── report_service.py      # PDF generation
├── ui/
│   ├── __init__.py
│   ├── styles.py              # CSS styling
│   └── visualizations.py      # Charts
└── utils/
    ├── __init__.py
    ├── image_utils.py         # Image processing
    ├── parser_utils.py        # Response parsing
    └── session_utils.py       # Session management
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai-ent-doctor-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API keys**

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-gemini-api-key"
ROBOFLOW_API_KEY = "your-roboflow-api-key"
```

## 🎯 Usage

1. **Run the application**
```bash
streamlit run app.py
```

2. **Upload ear image** in the Detection tab
3. **Review analysis** with charts and insights
4. **Consult AI doctor** for medical guidance
5. **Generate PDF report** with all findings

## 🔧 Configuration

### API Keys

- **Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Roboflow API**: Get from [Roboflow](https://roboflow.com/)

### Customization

- **Prompts**: Edit `config/prompts.py`
- **Styling**: Modify `ui/styles.py`
- **Charts**: Customize `ui/visualizations.py`

## 📦 Dependencies

- `streamlit` - Web interface
- `pillow` - Image processing
- `opencv-python` - Computer vision
- `inference-sdk` - Roboflow integration
- `google-generativeai` - Gemini AI
- `langchain` - Conversational AI
- `reportlab` - PDF generation
- `plotly` - Interactive charts

## ⚠️ Medical Disclaimer

This application is for educational and clinical support purposes only. It does NOT provide medical diagnosis and should not replace consultation with qualified healthcare professionals.


- Roboflow for computer vision infrastructure
- Google for Gemini AI models
- LangChain for conversational AI framework
