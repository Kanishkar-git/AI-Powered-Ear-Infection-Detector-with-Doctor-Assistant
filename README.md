# 👂 AI ENT Doctor Assistant

An advanced **AI-powered medical web application** for **ear infection detection, clinical analysis, and virtual ENT consultation**, built using **Computer Vision, Google Gemini, LangChain, and Streamlit**.

> ⚠️ **Disclaimer**: This system is designed for **clinical support and educational purposes only**. It does **not provide medical diagnoses** and must not replace consultation with a certified ENT specialist.

---

## 🌟 Key Features

### 🔬 AI-Powered Ear Infection Detection

* Uses **hospital-grade computer vision models** via **Roboflow**
* Detects ear conditions from uploaded otoscope images
* Highlights affected regions with bounding boxes

### 📊 Clinical Analysis & Visual Insights

* AI-generated medical overview and severity assessment
* Confidence-based severity classification (Mild / Moderate / High)
* Interactive charts:

  * Detection confidence gauge
  * Symptom probability distribution
  * Infection progression timeline
  * Visual feature contribution
  * Prevention effectiveness

### 👨‍⚕️ Virtual ENT Doctor Consultation

* Chat with **Dr. Sarah Chen**, an AI-simulated ENT specialist
* Powered by **LangChain + Google Gemini**
* Context-aware responses using detection results
* Medical-safe rules:

  * No prescriptions
  * No diagnoses
  * Clear red-flag escalation guidance

### 📋 Professional PDF Medical Reports

* Auto-generated clinical reports including:

  * Patient details
  * Detection results
  * AI analysis summary
  * Visual evidence
* Downloadable PDF format using **ReportLab**

---

## 🏗️ Project Structure

```
ai-ent-doctor-assistant/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for deployment
├── README.md                   # Project documentation
│
├── .streamlit/
│   └── secrets.toml            # API keys (local / cloud)
│
├── config/
│   ├── api_config.py           # API key handling
│   └── prompts.py              # Gemini & LangChain prompts
│
├── services/
│   ├── detection_service.py    # Roboflow detection logic
│   ├── analysis_service.py     # Gemini medical analysis
│   ├── chatbot_service.py      # LangChain chatbot logic
│   └── report_service.py       # PDF report generation
│
├── ui/
│   ├── styles.py               # Custom CSS styles
│   └── visualizations.py       # Plotly charts
│
└── utils/
    ├── image_utils.py          # Image processing helpers
    ├── parser_utils.py         # Gemini response parsing
    └── session_utils.py        # Streamlit session state
```

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-github-repo-url>
cd ai-ent-doctor-assistant
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 API Configuration

### 📁 Local Development

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
ROBOFLOW_API_KEY = "your_roboflow_api_key"
```

### ☁️ Streamlit Cloud Deployment

* Go to **Manage App → Secrets**
* Add the same keys (do NOT commit them to GitHub)

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

Then open the URL shown in the terminal.

---

## 🧪 How to Use

1. **Upload an ear image** (JPG / PNG)
2. Click **Run Detection**
3. Review:

   * Detected condition
   * Confidence score
   * Clinical insights & charts
4. Switch to **Consult ENT Doctor**

   * Ask questions about severity, symptoms, next steps
5. Generate and **download PDF medical report**

---

## ⚙️ Configuration & Customization

* **Medical prompts** → `config/prompts.py`
* **Chat behavior** → `services/chatbot_service.py`
* **Charts & analytics** → `ui/visualizations.py`
* **Styling & UI** → `ui/styles.py`

---

## 📦 Core Technologies Used

* **Streamlit** – Web application framework
* **Roboflow Inference SDK** – Computer vision detection
* **Google Gemini (google-generativeai)** – Medical AI analysis
* **LangChain** – Context-aware conversational AI
* **OpenCV** – Image processing
* **Plotly** – Interactive data visualizations
* **ReportLab** – PDF report generation

---

## ⚠️ Medical Disclaimer

This application is **not a diagnostic tool**.
All outputs are **AI-generated clinical support insights** and must be reviewed by a **qualified ENT specialist** before any medical decision is made.

---

## 🙌 Acknowledgements

* **Roboflow** – Computer vision infrastructure
* **Google Gemini** – Large language models
* **LangChain** – Conversational AI framework
* **Streamlit** – Rapid ML app deployment


