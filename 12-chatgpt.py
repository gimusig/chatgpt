import streamlit as st
import openai
import os

def generate_transcription(files):
    # 오디오 파일의 경로 또는 파일 객체를 `file` 인자로 전달
    transcription = openai.audio.transcriptions.create(
        model="whisper-1",
        file=files,
    )
    return transcription

def generate_trans(script):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"한국어(한글)을 {language1}로 번역하고, {language1}로 출력해줘"},
            {"role": "user", "content": script}
        ]
    )
    return completion

def generate_audio(audio_test) : 
    response = openai.audio.speech.create(
        model="tts-1-hd",
        voice="alloy", #alloy, echo, fable, onyx, nova 가능
        response_format = 'mp3',
        input=audio_test
    )
    return response


with st.sidebar:
    st.markdown('''
**API KEY 발급 방법**
1. https://beta.openai.com/ 회원가입
2. https://beta.openai.com/account/api-keys 접속
3. `create new secret key` 클릭 후 생성된 KEY 복사
    ''')
    value=''
    apikey = st.text_input(label='OPENAI API 키', placeholder='OPENAI API키를 입력해 주세요', value=value)

    
    button = st.button('확인')

    if button:
        if apikey != "" : 
            st.markdown(f'OPENAI API KEY: `{apikey}`')
            openai.api_key = apikey
        else : 
            st.markdown('OPENAI API KEY를 입력해주세요')    
  


# 윗 단 탭을 만들어서, 가능한것들을 다 만들어줘
tab1, tab2, tab3 = st.tabs(['번역기', '대시보드', '운동추천']) 

with tab1 : 
# 타이틀 적용 예시
    st.title('음성 번역기')

    col1, col2, col3 = st.columns(3)
    with col1 : 
        # 선택 박스
        row_language = st.selectbox(
            '음성 파일 언어를 선택해 주세요',
            ('한국어', '영어', '중국어', '일본어'), 
            index=None,
            placeholder='Select contact language'
        )


    with col3 : 
        # 선택 박스
        language1 = st.selectbox(
            '번역을 원하는 언어를 선택해 주세요',
            ('한국어', '영어', '중국어', '일본어'), 
            index=None,
            placeholder='Select contact language'
        )
        
    st.text('')
    st.subheader('음성파일을 업로드해주세요')


    # 파일 업로드 버튼 (업로드 기능)
    uploaded_file = st.file_uploader("파일 선택은 wav만 지원됩니다.", type=['wav'])

    if uploaded_file is not None:
        # 업로드된 파일을 바이너리 모드로 읽기
        audio_data = uploaded_file.read()

        # 예시로 오디오 데이터를 저장하거나 처리하는 코드를 추가할 수 있습니다.
        with open('uploaded_file.wav', 'wb') as file:
            file.write(audio_data)
        st.write("파일이 로컬 시스템에 저장되었습니다.")

        # 임시 파일을 열어서 OpenAI API를 사용하여 변환
        with open('uploaded_file.wav', 'rb') as audio_file:
            transcript = generate_transcription(audio_file)
            transcript = transcript.text

            st.divider() 
            st.write(" ")
            st.write(f"음성 텍스트: {transcript}")

            completion = generate_trans(transcript)
            completion = completion.choices[0].message.content

            st.divider() 
            st.write(" ")
            st.write(f"한글 -> {language1} 변환기 : {completion}")

            audio_test = generate_audio(completion)
            
            speech_file_path = "speech_output.mp3"
            with open(speech_file_path, "wb") as audio_file:
                audio_file.write(audio_test.content)  # 응답 내용을 파일에 씁니다.

            st.divider() 
            st.write(" ")
            st.audio(speech_file_path)

    else:
        st.write("파일을 업로드 해주세요.")



with tab2 : 
    st.title('대시보드 테스트')

with tab3 : 
    st.title('운동추천 테스트')