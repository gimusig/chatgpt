import streamlit as st
from streamlit.components.v1 import html
import base64

st.title("오디오 녹음기")

# HTML and JavaScript for microphone recording
html_code = """
<div id="controls">
    <button id="recordButton" style="font-size: 12px;">🔴 Record</button>
    <button id="stopButton" style="font-size: 12px;" disabled>⬛ Stop</button>
    <button id="uploadButton" style="font-size: 12px;" disabled>⬆️ Upload</button>
</div>
<br>
<audio id="audioPlayback" controls></audio>
<script>
    let chunks = [];
    let recorder;
    let audioBlob;

    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const uploadButton = document.getElementById('uploadButton');
    const audioPlayback = document.getElementById('audioPlayback');

    recordButton.addEventListener('click', async () => {
        console.log('Record button clicked'); // 디버깅을 위한 콘솔 로그 추가
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            console.log('Microphone access granted'); // 마이크 접근 허용 확인
            recorder = new MediaRecorder(stream);
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = e => {
                audioBlob = new Blob(chunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;
                chunks = [];
            };
            recorder.start();
            console.log('Recording started'); // 녹음 시작 확인
            recordButton.disabled = true;
            stopButton.disabled = false;
        } catch (err) {
            console.error('Microphone access denied', err); // 오류 처리
        }
    });

    stopButton.addEventListener('click', () => {
        console.log('Stop button clicked'); // 디버깅을 위한 콘솔 로그 추가
        recorder.stop();
        recordButton.disabled = false;
        stopButton.disabled = true;
        uploadButton.disabled = false;
    });

    uploadButton.addEventListener('click', () => {
        console.log('Upload button clicked'); // 디버깅을 위한 콘솔 로그 추가
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav');
        fetch('/upload', { method: 'POST', body: formData });
        uploadButton.disabled = true;
    });
</script>
"""

html(html_code)


