#Made with Nasim, BSc in CSE at ADUST 

import cv2
import numpy as np
# Direct imports to avoid 'AttributeError: module mediapipe has no attribute solutions'
import mediapipe as mp
from mediapipe.python.solutions import face_mesh as mp_face_mesh
from mediapipe.python.solutions import face_detection as mp_face_detection

class ExamMonitor:
    def __init__(self):
        # Initialize Face Mesh for head pose estimation
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize Face Detection for counting people
        self.face_detector = mp_face_detection.FaceDetection(
            model_selection=0, 
            min_detection_confidence=0.5
        )

    def get_head_pose(self, face_landmarks, img_w, img_h):
        # Specific landmark points for 3D pose estimation
        face_3d = []
        face_2d = []

        for idx, lm in enumerate(face_landmarks.landmark):
            # Key points: Nose tip, Chin, Left eye corner, Right eye corner, etc.
            if idx in [33, 263, 1, 61, 291, 199]:
                x, y = int(lm.x * img_w), int(lm.y * img_h) #Made with Nasim, BSc in CSE at ADUST 

                face_2d.append([x, y])
                face_3d.append([x, y, lm.z])

        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)

        # Camera Matrix approximation
        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, img_h / 2],
                              [0, focal_length, img_w / 2],
                              [0, 0, 1]])
        dist_matrix = np.zeros((4, 1), dtype=np.float64)

        # Solve PnP to find rotation
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
        rmat, _ = cv2.Rodrigues(rot_vec)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

        # Convert to degrees
        pitch = angles[0] * 360 # Up/Down
        yaw = angles[1] * 360   # Left/Right
        
        return pitch, yaw

    def analyze_frame(self, frame):
        img_h, img_w, _ = frame.shape
        # Convert BGR (OpenCV) to RGB (Mediapipe)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 1. Detect number of faces (Face Detection)
        results_detection = self.face_detector.process(rgb_frame)
        face_count = 0
        if results_detection.detections:
            face_count = len(results_detection.detections)

        # 2. Analyze head pose (Face Mesh)
        results_mesh = self.face_mesh.process(rgb_frame)
        status = "Focused" # Default
        
        if results_mesh.multi_face_landmarks:
            for face_landmarks in results_mesh.multi_face_landmarks:
                pitch, yaw = self.get_head_pose(face_landmarks, img_w, img_h)
                
                # Logic for detecting suspicious head movements
                if yaw < -12:
                    status = "Looking Right"
                elif yaw > 12:
                    status = "Looking Left"
                elif pitch < -10:
                    status = "Looking Down"
                else:
                    status = "Focused"

        # Overriding status based on face count
        if face_count > 1:
            status = "Multiple Faces! Suspicious"
        elif face_count == 0:
            status = "No Student Detected"

        return face_count, status
    #Made with Nasim, BSc in CSE at ADUST 
