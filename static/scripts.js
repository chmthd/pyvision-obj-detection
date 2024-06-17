(async () => {
    try {
        console.log('Fetching ngrok URL...');
        const response = await fetch('/ngrok-url');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const ngrokData = await response.json();
        console.log('ngrok URL:', ngrokData);

        if (ngrokData.error) {
            throw new Error(ngrokData.error);
        }

        const ngrokUrl = ngrokData.url;
        console.log('Fetching IP from:', ngrokUrl);
        const responseIp = await fetch(`${ngrokUrl}/ip`);
        if (!responseIp.ok) {
            throw new Error(`HTTP error! status: ${responseIp.status}`);
        }
        const { ip } = await responseIp.json();
        console.log('Local IP:', ip);

        const video = document.getElementById('video');

        // Access the device camera and stream to video element
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
            })
            .catch(err => {
                console.error('Error accessing camera: ', err);
                alert('Error accessing camera: ' + err.message);
            });

        document.getElementById('capture').addEventListener('click', () => {
            const canvas = document.getElementById('canvas');
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            canvas.toBlob(blob => {
                const formData = new FormData();
                formData.append('image', blob, 'image.jpg');

                fetch(`${ngrokUrl}/detect`, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Detection results:', data);
                    // Handle the detections
                    data.forEach(detection => {
                        context.strokeStyle = 'red';
                        context.lineWidth = 2;
                        context.strokeRect(detection.xmin, detection.ymin, detection.xmax - detection.xmin, detection.ymax - detection.ymin);
                        context.fillStyle = 'red';
                        context.fillText(detection.name, detection.xmin, detection.ymin > 10 ? detection.ymin - 5 : 10);
                    });
                })
                .catch(err => {
                    console.error('Error during detection:', err);
                    alert('Error during detection: ' + err.message);
                });
            }, 'image/jpeg');
        });
    } catch (err) {
        console.error('Initialization error:', err);
        alert('Initialization error: ' + err.message);
    }
})();
