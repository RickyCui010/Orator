from speechmodules.wakeword import PicoWakeWord
from speechmodules.speech2text import BaiduASR
from speechmodules.text2speech import BaiduTTS, Python3TTS
from chatmodule.openai_chat_module import OpenaiChatModule

import struct



PICOVOICE_API_KEY = "YDjXSOVWQgHmUnnjsYsUZ6MMBI4Fg2PvUf5BdbqNanxrpNlDD49Y0w=="  # picovoice key
keyword_path = './speechmodules/hey-robot_en_windows_v2_2_0.ppn'  # 唤醒词检测离线文件地址
Baidu_APP_ID = '33233995'  # 百度APP_ID
Baidu_API_KEY = 'mih6OzRDinv3vdgO5pTqDRMN'  # 百度API_KEY
Baidu_SECRET_KEY = 'SV3kBCNsIZEgVthaspeL1rdExce3TlZn'  # 百度SECRET_KEY
openai_api_key = "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"  # openai key


def run(picowakeword, asr, tts, openai_chat_module):
    while True:  # 开始需要始终保持对唤醒词的监听
        print("我在,请讲！")
        tts.text_to_speech_and_play("我在,请讲！")
        while True:  # 进入一次对话
            q = asr.speech_to_text()
            print(f'recognize_from_microphone, text={q}')
            if q is None:
                break
            if "再见" in q or "拜拜" in q:
                break
            else:
                res = openai_chat_module.chat_with_model(q)
                tts.text_to_speech_and_play(res)

def Orator():
    # 唤醒
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)

    # 语音转文字
    asr = BaiduASR(Baidu_APP_ID, Baidu_API_KEY, Baidu_SECRET_KEY)
    # asr = OpenaiASR(openai_api_key)

    # 文字转语音
    # tts = BaiduTTS(Baidu_APP_ID, Baidu_API_KEY, Baidu_SECRET_KEY)
    tts = Python3TTS()

    # chatgpt模块
    openai_chat_module = OpenaiChatModule(openai_api_key)
    # openai_chat_module = OpenaiAgentModule(openai_api_key)

    try:
        run(picowakeword, asr, tts, openai_chat_module)
    except KeyboardInterrupt:  # 键盘退出，云资源释放
            exit(0)
    finally:
        print('本轮对话结束')
        tts.text_to_speech_and_play('我退下啦！')

if __name__ == '__main__':
    Orator()
