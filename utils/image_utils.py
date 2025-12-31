"""Image Processing Utilities"""
import cv2
import numpy as np
from PIL import Image

def draw_boxes(image, predictions):
    """Draw bounding boxes on image"""
    for pred in predictions:
        x = int(pred['x'] - pred['width'] / 2)
        y = int(pred['y'] - pred['height'] / 2)
        w = int(pred['width'])
        h = int(pred['height'])
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        label = f"{pred['class']}: {pred['confidence']:.2f}"
        cv2.putText(image, label, (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image

def process_detection_image(uploaded_image, predictions):
    """Process uploaded image with detection boxes"""
    try:
        img_array = np.array(uploaded_image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        processed_img_bgr = draw_boxes(img_bgr.copy(), predictions)
        processed_img_rgb = cv2.cvtColor(processed_img_bgr, cv2.COLOR_BGR2RGB)
        return Image.fromarray(processed_img_rgb)
    except:
        return uploaded_image.copy()