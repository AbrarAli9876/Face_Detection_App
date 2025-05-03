# Deploying Face Detection App on Render

This guide provides instructions for deploying this Face Detection application on Render.

## Prerequisites

- A Render account (https://render.com)
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

1. Log in to your Render dashboard
2. Click "New" and select "Web Service"
3. Connect your Git repository
4. Configure your service:
   - **Name**: Choose a name for your service (e.g., face-detection-app)
   - **Environment**: Select "Python"
   - **Region**: Choose the region closest to your target users
   - **Branch**: Select your main branch (e.g., main or master)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Plan**: Choose the appropriate plan for your needs (minimum of Basic plan recommended for this app)

5. Click "Create Web Service"

## Environment Variables

If needed, configure these environment variables in the Render dashboard:
- `PORT`: Default is 5000, Render will set this automatically

## How the Web Camera Works

This application uses a client-side approach for webcam functionality:

1. The user's browser accesses their webcam using the MediaDevices Web API
2. Captured frames are sent to the server via AJAX requests
3. The server processes each frame with OpenCV/MediaPipe to detect faces
4. Face detection results are returned to the client
5. The client draws face boxes on the video feed in real time

This approach offers several advantages:
- No need for a physical camera on the server
- Works on cloud platforms like Render
- Reduces network bandwidth by only sending detection results, not full video

## HTTPS Requirements

Your app must be served over HTTPS for the webcam access to work properly in most browsers. Render automatically provides HTTPS for all web services.

## Important Notes

- The web interface requires camera access, which might not work in a deployed environment 
  due to browser security restrictions. Consider handling this gracefully.
- If using OpenCV's camera features, they might not work in a serverless environment.
- This deployment is mainly suitable for the Flask web interface without the live camera
  features, or would need WebRTC or other solutions for remote camera access.

## Troubleshooting

If you encounter issues:
1. Check Render logs for error messages
2. Verify that all requirements are properly installed
3. Ensure gunicorn is in your requirements.txt file
4. If webcam access fails in the browser, check for console errors related to camera permissions
5. For camera issues, ensure the user has granted camera permissions to your site 