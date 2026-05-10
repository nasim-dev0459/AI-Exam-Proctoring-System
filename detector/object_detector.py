from ultralytics import YOLO
import cv2

class ObjectDetector:
    def __init__(self):
        # Loads YOLOv8 Nano model (Lightweight for real-time)
        self.model = YOLO('yolov8n.pt') 

    def detect_phone(self, frame):
        # Run inference with low confidence threshold to be safe
        results = self.model(frame, verbose=False, conf=0.4)
        phone_detected = False
        
        for r in results:
            for box in r.boxes:
                # Class 67 is 'cell phone'
                cls = int(box.cls[0])
                if cls == 67:
                    phone_detected = True
                    # Draw a rectangle around the phone for visual proof
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, "PHONE DETECTED", (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return phone_detected
    #Made with Nasim, BSc in CSE at ADUST 
