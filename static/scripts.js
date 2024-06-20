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
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');

        const startCamera = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                video.play();
            } catch (err) {
                console.error('Error accessing camera: ', err);
                alert('Error accessing camera: ' + err.message);
            }
        };

        const detectObjects = async () => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(async (blob) => {
                const formData = new FormData();
                formData.append('file', blob, 'image.jpg');

                try {
                    const response = await fetch(`${ngrokUrl}/detect`, {
                        method: 'POST',
                        body: formData
                    });
                    if (!response.ok) {
                        const errorText = await response.text();
                        throw new Error(`HTTP error! status: ${response.status}, detail: ${errorText}`);
                    }
                    const data = await response.json();
                    console.log('Detection results:', data);

                    if (!Array.isArray(data)) {
                        console.error('Unexpected response format:', data);
                        throw new Error('Unexpected response format');
                    }

                    context.clearRect(0, 0, canvas.width, canvas.height);
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    data.forEach(detection => {
                        context.strokeStyle = 'red';
                        context.lineWidth = 2;
                        context.strokeRect(detection.xmin, detection.ymin, detection.xmax - detection.xmin, detection.ymax - detection.ymin);
                        context.fillStyle = 'red';
                        context.fillText(detection.name, detection.xmin, detection.ymin > 10 ? detection.ymin - 5 : 10);
                    });
                } catch (err) {
                    console.error('Error during detection:', err);
                    alert('Error during detection: ' + err.message);
                }
            }, 'image/jpeg');
        };

        document.getElementById('capture').addEventListener('click', async () => {
            await startCamera();
            console.log('Camera feed started');
            setInterval(detectObjects, 100);
        });
    } catch (err) {
        console.error('Initialization error:', err);
        alert('Initialization error: ' + err.message);
    }
})();
