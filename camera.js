// Get video and canvas elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-button');
const capturedImage = document.getElementById('captured-image');

// Define a function to request camera access
function requestCameraAccess() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                video.onloadedmetadata = function (e) {
                    video.play(); // Start playing the video
                };
            })
            .catch(function (error) {
                console.error('Error accessing the camera: ' + error);
            });
    } else {
        console.error('Camera not supported on this device.');
    }
}

// Capture image when the button is clicked
captureButton.addEventListener('click', function () {
    
    if (video.paused || video.ended) {
        return;
    }

    // Capture a frame from the video feed and display it on the canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas image to a data URL (base64)
    const imageDataURL = canvas.toDataURL('image/png');

    // Display the captured image on the page
    capturedImage.src = imageDataURL;
    capturedImage.style.display = 'inline-block'; // Use inline-block to maintain the layout
});

// the camera access function when the page loads
requestCameraAccess();
