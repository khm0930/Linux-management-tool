import speech_recognition as sr
from gtts import gTTS
import os
from transformers import pipeline
#https://developer.nvidia.com/cuda-downloads
#https://developer.nvidia.com/cudnn
#https://developer.nvidia.com/tensorrt
#export PATH=/usr/local/cuda/bin:$PATH
#export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# 음성 인식 함수 (한국어 지원)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("말씀하세요:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='ko-KR')
            print("말씀하신 내용: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition이 음성을 이해하지 못했습니다.")
            return None
        except sr.RequestError as e:
            print("결과를 요청할 수 없습니다; {0}".format(e))
            return None

# 자연어 처리 함수
def analyze_sentiment(text):
    nlp = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    result = nlp(text)[0]
    return result['label'], result['score']

# 음성 합성 함수 (한국어 지원)
def speak_text(text):
    tts = gTTS(text=text, lang='ko')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

# 메인 함수
def main():
    while True:
        print("명령을 기다리고 있습니다...")
        command = recognize_speech()
        if command:
            if "종료" in command.lower():
                speak_text("안녕히 가세요!")
                break
            label, score = analyze_sentiment(command)
            response = f"감정은 {label}로, 신뢰도는 {score:.2f}입니다."
            print(response)
            speak_text(response)
