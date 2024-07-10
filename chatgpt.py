import streamlit as st
from streamlit.components.v1 import html
import base64

st.title("오디오 녹음기")

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
                downloadAudio(audioBlob);
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

    function downloadAudio(blob) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'recording.wav';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    }
</script>
"""

html(html_code)

