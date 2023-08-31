import pvporcupine
import pyaudio
import struct


PICOVOICE_API_KEY = "YDjXSOVWQgHmUnnjsYsUZ6MMBI4Fg2PvUf5BdbqNanxrpNlDD49Y0w=="
keyword_path = './hey-robot_en_linux_v2_2_0.ppn'

class PicoWakeWord:
    def __init__(self, PICOVOICE_API_KEY, keyword_path, model_path=None):
        self.PICOVOICE_API_KEY = PICOVOICE_API_KEY
        self.keyword_path = keyword_path
        self.model_path = model_path
        self.porcupine = pvporcupine.create(
            access_key=self.PICOVOICE_API_KEY,
            keyword_paths=[self.keyword_path],
            model_path=self.model_path
        )
        self.myaudio = pyaudio.PyAudio()
        self.stream = self.myaudio.open(
            input_device_index=0,
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def detect_wake_word(self):
        audio_obj = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, audio_obj)
        keyword_idx = self.porcupine.process(audio_obj_unpacked)
        return keyword_idx



if __name__ == '__main__':
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
    while True:
        audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
        keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
        if keyword_idx >= 0:
            print("我听到了！")
