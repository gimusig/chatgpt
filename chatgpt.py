import streamlit as st
from streamlit.components.v1 import html
from io import BytesIO
import os

st.title("오디오 녹음기")

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# HTML and JavaScript for microphone recording
html_code = """
<div id="controls">
    <button id="recordButton" style="font-size: 12px;">🔴 Record</button>
    <button id="stopButton" style="font-size: 12px;" disabled>⬛ Stop</button>
</div>
<br>
<audio id="audioPlayback" controls></audio>
<script>
    let chunks = [];
    let recorder;
    let audioBlob;

    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const audioPlayback = document.getElementById('audioPlayback');

    recordButton.addEventListener('click', async () => {
        console.log('Record button clicked');
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            console.log('Microphone access granted');
            recorder = new MediaRecorder(stream);
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = e => {
                audioBlob = new Blob(chunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;
                uploadAudio(audioBlob);
                chunks = [];
            };
            recorder.start();
            console.log('Recording started');
            recordButton.disabled = true;
            stopButton.disabled = false;
        } catch (err) {
            console.error('Microphone access denied', err);
        }
    });

    stopButton.addEventListener('click', () => {
        console.log('Stop button clicked');
        recorder.stop();
        recordButton.disabled = false;
        stopButton.disabled = true;
    });

    function uploadAudio(blob) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const base64Data = event.target.result.split(',')[1];
            const fileName = 'recording.wav';
            fetch(`/upload?name=${fileName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({file: base64Data})
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        };
        reader.readAsDataURL(blob);
    }
</script>
"""

html(html_code)

# Handle file upload
query_params = st.experimental_get_query_params()
if "name" in query_params:
    file_name = query_params["name"][0]
    file_data = st.experimental_get_query_params()["file"][0]
    file_bytes = BytesIO(base64.b64decode(file_data))
    with open(os.path.join(UPLOAD_DIR, file_name), "wb") as f:
        f.write(file_bytes.read())
    st.success(f"File {file_name} uploaded successfully")
