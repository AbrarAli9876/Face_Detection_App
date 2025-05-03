// Face Detection App - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const videoFeed = document.getElementById('video-feed');
    const cameraOffMessage = document.getElementById('camera-off-message');
    const enableCameraButton = document.getElementById('enable-camera');
    const faceCountElement = document.getElementById('face-count');
    
    // Function to request camera access
    function requestCameraAccess() {
        // Show loading state
        enableCameraButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        enableCameraButton.disabled = true;
        
        // Try to access the video feed
        videoFeed.style.display = 'block';
        videoFeed.addEventListener('error', handleVideoError);
        
        // Set a timeout to check if video is playing after a few seconds
        setTimeout(checkVideoStatus, 3000);
    }
    
    // Function to check if video is playing
    function checkVideoStatus() {
        if (videoFeed.readyState === 0) {
            // Video failed to load
            handleVideoError();
        } else {
            // Video is loading or playing
            cameraOffMessage.style.display = 'none';
            startFaceCountUpdates();
        }
    }
    
    // Function to handle video errors
    function handleVideoError() {
        videoFeed.style.display = 'none';
        cameraOffMessage.style.display = 'flex';
        enableCameraButton.innerHTML = 'Enable Camera';
        enableCameraButton.disabled = false;
    }
    
    // Function to start updating face count
    function startFaceCountUpdates() {
        // Update face count every second
        setInterval(updateFaceCount, 1000);
    }
    
    // Function to update face count
    function updateFaceCount() {
        fetch('/face_count')
            .then(response => response.json())
            .then(data => {
                faceCountElement.textContent = data.count;
                
                // Add animation effect on count change
                faceCountElement.classList.add('count-updated');
                setTimeout(() => {
                    faceCountElement.classList.remove('count-updated');
                }, 300);
            })
            .catch(error => {
                console.error('Error fetching face count:', error);
            });
    }
    
    // Event listener for enable camera button
    enableCameraButton.addEventListener('click', requestCameraAccess);
    
    // Check browser camera support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Your browser does not support camera access. Please use a modern browser like Chrome, Firefox, or Edge.');
    }
    
    // Automatically try to enable camera on page load
    requestCameraAccess();
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            // Page is visible again, check camera status
            checkVideoStatus();
        }
    });
    
    // Add responsive behavior for different screen orientations
    window.addEventListener('resize', function() {
        // You can add specific behavior for orientation changes here if needed
    });
}); 