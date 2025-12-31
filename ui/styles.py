"""CSS Styling for the Application"""

def get_custom_css():
    """Return custom CSS styling"""
    return """
    <style>
    .main {
        padding: 20px;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .result-point {
        padding: 10px;
        margin: 8px 0;
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        border-radius: 5px;
    }
    .severity-mild {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .severity-moderate {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .severity-high {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .alert-box {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .doctor-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 10px 0;
    }
    .chat-message {
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        animation: fadeIn 0.5s;
        color: #0f172a;
    }
    .user-message {
        background-color: #dbeafe;
        border-left: 4px solid #2563eb;
        margin-left: 20px;
        color: #0f172a;
    }
    .doctor-message {
        background-color: #ede9fe;
        border-left: 4px solid #7c3aed;
        margin-right: 20px;
        color: #1e1b4b;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .scan-context-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .chat-input-container {
        position: sticky;
        bottom: 0;
        background-color: #f9fafb;
        padding: 15px 0;
        border-top: 2px solid #e5e7eb;
    }
    .medical-disclaimer {
        background-color: #fef3c7;
        color: #78350f;
        border: 2px solid #f59e0b;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.9em;
    }
    </style>
    """