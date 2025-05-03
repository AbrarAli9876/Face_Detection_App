from flask import Flask, render_template, Response, jsonify, request
import cv2
import time
import sys
import os
import base64
import numpy as np
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable for face count
face_count = 0

# Try to import the facial landmark detector
try:
    from face_landmarks import FacialLandmarkDetector, filter_faces_by_confidence, MEDIAPIPE_AVAILABLE
    
    if MEDIAPIPE_AVAILABLE:
        # Initialize Facial Landmark Detector
        face_detector = FacialLandmarkDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        USING_LANDMARKS = True
    else:
        print("WARNING: Using basic face detection instead of facial landmarks due to MediaPipe import error.", file=sys.stderr)
        USING_LANDMARKS = False
        # Initialize basic OpenCV face detection as fallback
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
except ImportError as e:
    print(f"ERROR: Could not import face_landmarks module: {str(e)}", file=sys.stderr)
    print("WARNING: Using basic face detection instead of facial landmarks.", file=sys.stderr)
    USING_LANDMARKS = False
    # Initialize basic OpenCV face detection as fallback
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(frame):
    """
    Detect faces in a frame and return the processed frame, face count, and face locations
    """
    global face_count
    face_locations = []
    
    if USING_LANDMARKS:
        # Process the frame with our facial landmark detector
        processed_frame, faces_data, current_face_count = face_detector.process_frame(frame)
        
        # Extract face locations for drawing on client-side
        if faces_data and len(faces_data) > 0:
            for face in faces_data:
                if 'bbox' in face:
                    x, y, width, height = face['bbox']
                    face_locations.append({
                        'x': int(x),
                        'y': int(y),
                        'width': int(width),
                        'height': int(height)
                    })
    else:
        # Fallback to basic OpenCV face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_locations.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h)
            })
        
        current_face_count = len(faces)
        processed_frame = frame
    
    # Update face count
    face_count = current_face_count
    
    return processed_frame, face_count, face_locations

@app.route('/')
def index():
    """
    Render the index page
    """
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    """
    Process a frame sent from the client
    """
    if request.method == 'POST':
        try:
            # Get the base64 image data from the request
            data = request.json
            if not data or 'image' not in data:
                return jsonify({'error': 'No image data received'}), 400
            
            # Extract the base64 string (remove data URL prefix)
            base64_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
            
            # Decode the base64 string to image
            img_data = base64.b64decode(base64_data)
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return jsonify({'error': 'Failed to decode image'}), 400
            
            # Process the frame to detect faces
            _, face_count, face_locations = detect_faces(frame)
            
            # Return the face count and face locations
            return jsonify({
                'count': face_count,
                'faces': face_locations
            })
            
        except Exception as e:
            print(f"Error processing frame: {str(e)}", file=sys.stderr)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid request method'}), 405

@app.route('/face_count')
def get_face_count():
    """
    Return the current face count
    """
    global face_count
    return jsonify({'count': face_count})

# Add health check endpoint for Render
@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring
    """
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    finally:
        # Make sure to release resources when the app is closed
        if USING_LANDMARKS:
            face_detector.release() 