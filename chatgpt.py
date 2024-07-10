# import streamlit as st
# import sounddevice as sd
# import wavio
# import numpy as np

# # 기본 설정
# fs = 44100
# device_id = 7  # 마이크 장치 ID
# channels = 2  # 마이크가 지원하는 입력 채널 수 설정

# st.title("오디오 녹음 및 저장")

# # Session state 초기화
# if "recording" not in st.session_state:
#     st.session_state["recording"] = False

# if "audio_data" not in st.session_state:
#     st.session_state["audio_data"] = []

# # 녹음 시작
# def start_recording():
#     if not st.session_state["recording"]:
#         st.session_state["recording"] = True
#         st.session_state["audio_data"] = []
#         try:
#             st.session_state["stream"] = sd.InputStream(
#                 samplerate=fs, channels=channels, device=device_id, callback=callback
#             )
#             st.session_state["stream"].start()
#             st.write("녹음 중...")
#         except Exception as e:
#             st.session_state["recording"] = False
#             st.error(f"녹음 시작에 실패했습니다: {e}")

# # 녹음 종료
# def stop_recording():
#     if st.session_state["recording"]:
#         st.session_state["recording"] = False
#         st.session_state["stream"].stop()
#         st.session_state["stream"].close()
#         st.write("녹음이 완료되었습니다.")

#         if st.session_state["audio_data"]:
#             # 오디오 데이터를 numpy 배열로 변환
#             audio_data = np.concatenate(st.session_state["audio_data"], axis=0)

#             # 파일 이름
#             file_path = "output.wav"

#             # 저장하기
#             wavio.write(file_path, audio_data, fs, sampwidth=2)
#             st.write(f"오디오 파일이 '{file_path}'에 저장되었습니다!")
#         else:
#             st.write("녹음할 데이터가 없습니다. 다시 시도하십시오.")

# # 콜백 함수
# def callback(indata, frames, time, status):
#     if st.session_state["recording"]:
#         st.session_state["audio_data"].append(indata.copy())

# # UI 생성
# if st.button("녹음 시작"):
#     start_recording()

# if st.button("녹음 종료"):
#     stop_recording()

# # 녹음된 오디오 파일을 다운로드할 수 있습니다.
# st.write("녹음된 오디오 파일을 다운로드할 수 있습니다.")
# try:
#     with open("output.wav", "rb") as file:
#         st.download_button(
#             label="오디오 파일 다운로드",
#             data=file,
#             file_name="recorded_audio.wav",
#             mime="audio/wav"
#         )
# except FileNotFoundError:
#     st.write("먼저 녹음을 진행해 주세요.")








import streamlit as st
import sounddevice as sd
import wavio
import numpy as np
import os
import uuid

# 기본 설정
fs = 44100
device_id = 7  # 스테레오 믹스 장치 ID (필요 시 변경)
channels = 2  # 장치가 지원하는 입력 채널 수

# 기본 저장 경로 설정
SAVE_DIR = "recordings"
os.makedirs(SAVE_DIR, exist_ok=True)  # 디렉토리가 존재하지 않으면 생성

st.title("오디오 녹음 및 저장")

# Session state 초기화
if "recording" not in st.session_state:
    st.session_state["recording"] = False

if "audio_data" not in st.session_state:
    st.session_state["audio_data"] = []

if "file_path" not in st.session_state:
    st.session_state["file_path"] = None

# 녹음 시작
def start_recording():
    if not st.session_state["recording"]:
        st.session_state["recording"] = True
        st.session_state["audio_data"] = []
        st.session_state["file_path"] = None
        try:
            st.session_state["stream"] = sd.InputStream(
                samplerate=fs, channels=channels, device=device_id, callback=callback
            )
            st.session_state["stream"].start()
            st.write("녹음 중...")
        except Exception as e:
            st.session_state["recording"] = False
            st.error(f"녹음 시작에 실패했습니다: {e}")

# 녹음 종료
def stop_recording():
    if st.session_state["recording"]:
        st.session_state["recording"] = False
        st.session_state["stream"].stop()
        st.session_state["stream"].close()
        st.write("녹음이 완료되었습니다.")

        if st.session_state["audio_data"]:
            # 오디오 데이터를 numpy 배열로 변환
            audio_data = np.concatenate(st.session_state["audio_data"], axis=0)

            # 고유 파일 이름 생성
            file_name = f"{uuid.uuid4().hex}.wav"
            file_path = os.path.join(SAVE_DIR, file_name)

            # 저장하기
            wavio.write(file_path, audio_data, fs, sampwidth=
2)
            st.session_state["file_path"] = file_path
            st.write(f"오디오 파일이 '{file_path}'에 저장되었습니다!")
        else:
            st.write("녹음할 데이터가 없습니다. 다시 시도하십시오.")

# 콜백 함수
def callback(indata, frames, time, status):
    if st.session_state["recording"]:
        st.session_state["audio_data"].append(indata.copy())

# UI 생성
if st.button("녹음 시작"):
    start_recording()

if st.button("녹음 종료"):
    stop_recording()

# 녹음된 오디오 파일을 다운로드할 수 있습니다.
if st.session_state.get("file_path"):
    st.write("녹음된 오디오 파일을 다운로드할 수 있습니다.")
    with open(st.session_state["file_path"], "rb") as file:
        st.download_button(
            label="오디오 파일 다운로드",
            data=file,
            file_name=os.path.basename(st.session_state["file_path"]),
            mime="audio/wav"
        )
else:
    st.write("먼저 녹음을 진행해 주세요.")
