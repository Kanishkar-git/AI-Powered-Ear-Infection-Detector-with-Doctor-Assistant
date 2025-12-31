"""Roboflow Detection Service"""
import tempfile
from config.api_config import get_roboflow_client
from utils.image_utils import process_detection_image

def run_detection(uploaded_image):
    """Run Roboflow detection on uploaded image"""
    client = get_roboflow_client()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        uploaded_image.save(temp_file.name)
        temp_file_path = temp_file.name
    
    result = client.run_workflow(
        workspace_name="privacydetailsdetection",
        workflow_id="custom-workflow-5",
        images={"image": temp_file_path},
        use_cache=True
    )

    predictions = []
    if isinstance(result, list) and len(result) > 0:
        for item in result:
            if isinstance(item, dict) and "predictions" in item:
                pred_data = item["predictions"]
                if isinstance(pred_data, dict) and "predictions" in pred_data:
                    predictions.extend(pred_data["predictions"])
    
    return predictions

def build_medical_context(predictions, patient_age):
    """Build medical context from predictions"""
    if not predictions:
        return {}
    
    confidence = predictions[0]['confidence'] * 100
    conf_label = "high" if confidence > 85 else "moderate" if confidence > 60 else "low"
    
    return {
        'condition': predictions[0]['class'],
        'confidence': confidence,
        'confidence_label': conf_label,
        'box_area': 'large' if predictions[0].get('width', 0) > 200 else 'standard',
        'age': patient_age if patient_age else 'Not provided',
        'visual_features': ['Redness detected', 'Inflammation visible', 'Structural changes']
    }