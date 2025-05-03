# Face Detection Web Application

A real-time face detection web application that uses your camera to detect and count human faces. Built with Python, Flask, MediaPipe, and modern web technologies.

## Features

- Real-time face detection using facial landmarks (forehead, eyes, nose, chin)
- Live camera feed access via web browser
- Responsive design for mobile and desktop platforms
- Clear face counting display
- User-friendly camera access prompts

## Requirements

- Python 3.8 or higher
- Web camera
- Modern web browser (Chrome, Firefox, Edge recommended)

## Installation

1. Clone this repository or download the source code.

2. For the easiest setup, use the included setup script:
   ```
   python setup.py
   ```
   This script will:
   - Check if you're in a virtual environment
   - Create one if needed
   - Install all required dependencies
   - Verify the installation

3. Alternatively, you can set up manually:

   a. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```

   b. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

   c. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Troubleshooting MediaPipe Installation

If you encounter issues with MediaPipe not being resolved, try these steps:

1. Run the diagnostics script to check your environment:
   ```
   python setup_check.py
   ```

2. Try reinstalling MediaPipe with the exact version:
   ```
   pip uninstall -y mediapipe
   pip install mediapipe==0.10.21
   ```

3. If you still have issues, the application will automatically fall back to basic face detection without the advanced facial landmarks. You can still use the app, but it will have limited feature detection capabilities.

## Running the Application

1. Make sure you're in the project directory with your virtual environment activated.

2. Start the Flask server:
   ```
   python app.py
   ```

3. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

4. Allow camera access when prompted by your browser.

## Usage

- When you first access the application, you'll be prompted to allow camera access.
- Once camera access is granted, you should see the live video feed.
- The application will automatically detect faces and display the count.
- If your camera is turned off or not accessible, you'll see a message with instructions.

## Technical Details

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **Face Detection**: MediaPipe Face Detection/Mesh (with OpenCV Haar Cascade fallback)
- **Video Processing**: OpenCV

## Deployment

This application can be deployed to various cloud platforms:

- Heroku
- Google App Engine
- AWS Elastic Beanstalk
- Azure App Service

Specific deployment instructions will vary based on your chosen platform.

## Customization

You can customize various aspects of the application:

- Adjust the face detection confidence threshold in `app.py`
- Modify the UI styling in `static/css/style.css`
- Change the page behavior in `static/js/script.js`

## Troubleshooting

- **Camera access issues**: Make sure your browser has permission to access your camera. Check browser settings if needed.
- **Slow performance**: Try closing other applications using your camera or reduce the quality settings.
- **Detection problems**: Ensure adequate lighting and position your face clearly in view of the camera.
- **MediaPipe issues**: See the "Troubleshooting MediaPipe Installation" section above.

## License

This project is licensed under the MIT License - see the LICENSE file for details."# Face_Detection_App" 
"# Face_Detection_App" 
