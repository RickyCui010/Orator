from aip import AipSpeech
from playsound import playsound
import pygame # 导入pygame，playsound报错或运行不稳定时直接使用
import pyttsx3



class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def text_to_speech_and_play(self, text=""):
        result = self.client.synthesis(text,'zh',1,{
            'spd': 5,  # 语速
            'vol': 5,  # 音量大小
            'per':1  # 发声人 百度丫丫
        })# 得到音频的二进制文件

        if not isinstance(result, dict):
            with open("./audio.mp3", "wb") as f:
                f.write(result)
        else:
            print("语音合成失败", result)
        # playsound('./audio.mp3')#播放音频
        self.play_audio_with_pygame('audio.mp3')  # 注意pygame只能识别mp3格式

    def play_audio_with_pygame(self, audio_file_path):
        # 代码来自Linky的贡献
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()



class Python3TTS:
    def __init__(self):
        pass

    def text_to_speech_and_play(self, text=""):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

if __name__ =='__main__':
    APP_ID = "33233995"
    API_KEY = "mih6OzRDinv3vdgO5pTqDRMN"
    SECRET_KEY = "SV3kBCNsIZEgVthaspeL1rdExce3TlZn"

    baidutts = BaiduTTS(APP_ID,API_KEY,SECRET_KEY)
    baidutts.text_to_speech_and_play("真他妈好吃，真他妈香，哈哈哈哈哈哈")

    # pyttsx3tts = Python3TTS()
    # pyttsx3tts.text_to_speech_and_play('天气真不错')

