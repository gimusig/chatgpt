import streamlit as st
from streamlit.components.v1 import html
from flask import Flask, request
import os

st.title("오디오 녹음기")

import streamlit as st

st.title("Streamlit Microphone Recorder")

# HTML and JavaScript for microphone recording and file upload
html_code = """
<div id="controls">
    <button id="recordButton" style="font-size: 20px;">🔴 Record</button>
    <button id="stopButton" style="font-size: 20px;" disabled>⬛ Stop</button>
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
        const formData = new FormData();
        formData.append('file', blob, 'recording.wav');
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }
</script>
"""

html(html_code)


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return 'File uploaded successfully', 200

if __name__ == '__main__':
    app.run(port=5000)
