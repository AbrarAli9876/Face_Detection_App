import cv2
import numpy as np
import sys

# Try to import mediapipe with better error handling
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError as e:
    MEDIAPIPE_AVAILABLE = False
    error_message = f"""
ERROR: MediaPipe module not found or could not be resolved. Error: {str(e)}
Please install it using one of the following commands:
    pip install mediapipe==0.10.21
    python -m pip install mediapipe==0.10.21
    
If you already have it installed, there might be a dependency issue or path problem.
Try reinstalling it with the specific version: mediapipe==0.10.21
"""
    print(error_message, file=sys.stderr)

class FacialLandmarkDetector:
    """
    Class for detecting facial landmarks with a focus on forehead, eyes, nose, and chin.
    """
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe is required for FacialLandmarkDetector but it's not installed or could not be resolved. "
                             "Please install the correct version: mediapipe==0.10.21")
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize the Face Mesh model
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=10,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Define facial landmark indices for specific features
        # These indices are based on MediaPipe's 468 facial landmarks
        self.FOREHEAD_INDICES = [10, 151, 9, 8, 107, 106, 105, 66, 69, 104, 103, 67, 109, 108]
        self.LEFT_EYE_INDICES = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
        self.RIGHT_EYE_INDICES = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
        self.NOSE_INDICES = [168, 6, 197, 195, 5, 4, 19, 94, 2, 164, 0, 11, 12, 13, 14, 15, 16, 17, 18, 200, 199, 175]
        self.CHIN_INDICES = [152, 175, 199, 200, 18, 217, 122, 174, 194]
        
        # Colors for drawing
        self.FOREHEAD_COLOR = (0, 255, 0)  # Green
        self.EYE_COLOR = (255, 0, 0)       # Blue
        self.NOSE_COLOR = (0, 0, 255)      # Red
        self.CHIN_COLOR = (255, 255, 0)    # Cyan
        
    def process_frame(self, frame):
        """
        Process a frame to detect facial landmarks and draw them
        
        Args:
            frame: Input RGB frame/image
            
        Returns:
            processed_frame: Frame with landmarks drawn
            faces_data: List of dictionaries containing face feature confidence scores
            face_count: Number of faces detected
        """
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
        frame_height, frame_width, _ = rgb_frame.shape
        
        # Process the frame with MediaPipe Face Mesh
        results = self.face_mesh.process(rgb_frame)
        
        # Convert back to BGR for display
        processed_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        # List to store face data
        faces_data = []
        face_count = 0
        
        if results.multi_face_landmarks:
            face_count = len(results.multi_face_landmarks)
            
            for face_landmarks in results.multi_face_landmarks:
                # Dictionary to store feature confidence scores
                face_data = {
                    'forehead': 0.0,
                    'eyes': 0.0,
                    'nose': 0.0,
                    'chin': 0.0,
                    'overall': 0.0
                }
                
                # Draw forehead landmarks (green)
                self._draw_specific_landmarks(processed_frame, face_landmarks, self.FOREHEAD_INDICES, self.FOREHEAD_COLOR)
                face_data['forehead'] = self._calculate_feature_confidence(face_landmarks, self.FOREHEAD_INDICES)
                
                # Draw left eye landmarks (blue)
                self._draw_specific_landmarks(processed_frame, face_landmarks, self.LEFT_EYE_INDICES, self.EYE_COLOR)
                
                # Draw right eye landmarks (blue)
                self._draw_specific_landmarks(processed_frame, face_landmarks, self.RIGHT_EYE_INDICES, self.EYE_COLOR)
                face_data['eyes'] = self._calculate_feature_confidence(face_landmarks, 
                                                                     self.LEFT_EYE_INDICES + self.RIGHT_EYE_INDICES)
                
                # Draw nose landmarks (red)
                self._draw_specific_landmarks(processed_frame, face_landmarks, self.NOSE_INDICES, self.NOSE_COLOR)
                face_data['nose'] = self._calculate_feature_confidence(face_landmarks, self.NOSE_INDICES)
                
                # Draw chin landmarks (cyan)
                self._draw_specific_landmarks(processed_frame, face_landmarks, self.CHIN_INDICES, self.CHIN_COLOR)
                face_data['chin'] = self._calculate_feature_confidence(face_landmarks, self.CHIN_INDICES)
                
                # Calculate overall confidence
                face_data['overall'] = (face_data['forehead'] + face_data['eyes'] + 
                                      face_data['nose'] + face_data['chin']) / 4.0
                
                faces_data.append(face_data)
        
        return processed_frame, faces_data, face_count
    
    def _draw_specific_landmarks(self, image, landmarks, indices, color, radius=1):
        """
        Draw specific landmarks on the image
        """
        height, width, _ = image.shape
        for idx in indices:
            point = landmarks.landmark[idx]
            x, y = int(point.x * width), int(point.y * height)
            cv2.circle(image, (x, y), radius, color, -1)
    
    def _calculate_feature_confidence(self, landmarks, indices):
        """
        Calculate a simple confidence score for a feature based on landmark visibility
        """
        total_visibility = 0
        for idx in indices:
            # MediaPipe landmarks have a visibility score
            total_visibility += landmarks.landmark[idx].visibility
        
        # Return average visibility as confidence
        return total_visibility / len(indices) if indices else 0.0
    
    def release(self):
        """
        Release resources
        """
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()


# Function to filter faces based on feature confidence
def filter_faces_by_confidence(faces_data, threshold=0.5):
    """
    Filter faces based on a confidence threshold
    
    Args:
        faces_data: List of dictionaries containing face feature confidence scores
        threshold: Minimum confidence threshold (0.0 to 1.0)
        
    Returns:
        filtered_count: Number of faces that passed the threshold
    """
    filtered_faces = [face for face in faces_data if face['overall'] > threshold]
    return len(filtered_faces)