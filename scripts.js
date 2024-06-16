const video = document.getElementById('video');

// Access the device camera and stream to video element
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => console.error('Error accessing camera: ', err));

document.getElementById('capture').addEventListener('click', () => {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('image', blob, 'image.jpg');

        fetch('http://<YOUR_COMPUTER_IP>:8000/detect', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Handle the detections
            data.forEach(detection => {
                context.strokeStyle = 'red';
                context.lineWidth = 2;
                context.strokeRect(detection.xmin, detection.ymin, detection.xmax - detection.xmin, detection.ymax - detection.ymin);
                context.fillStyle = 'red';
                context.fillText(detection.name, detection.xmin, detection.ymin > 10 ? detection.ymin - 5 : 10);
            });
        });
    }, 'image/jpeg');
});
