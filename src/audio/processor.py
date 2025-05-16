import numpy as np
from collections import deque

class AudioProcessor:
    def __init__(self, sample_rate=16000, buffer_size=2000):
        """
        实时音频处理器
        :param sample_rate: 采样率(Hz)
        :param buffer_size: 缓冲大小(ms)
        """
        self.sample_rate = sample_rate
        self.buffer = deque(maxlen=int(sample_rate * buffer_size / 1000))
        self.vad_threshold = 0.5
        self.noise_profile = None

    def noise_suppression(self, frame):
        """
        基于谱减法的噪声抑制
        :param frame: 音频帧(numpy数组)
        :return: 降噪后的音频帧
        """
        if self.noise_profile is None:
            self.noise_profile = np.abs(np.fft.rfft(frame))
            return frame
            
        spec = np.fft.rfft(frame)
        phase = np.angle(spec)
        magnitude = np.maximum(np.abs(spec) - self.noise_profile, 0)
        self.noise_profile = 0.9 * self.noise_profile + 0.1 * np.abs(spec)
        return np.fft.irfft(magnitude * np.exp(1j * phase))

    def voice_activity_detection(self, frame):
        """
        基于能量的语音活动检测
        :param frame: 音频帧
        :return: bool(是否包含语音)
        """
        energy = np.sum(frame ** 2) / len(frame)
        return energy > self.vad_threshold

    def process_frame(self, frame):
        """
        处理单帧音频
        :param frame: 原始音频帧
        :return: 处理后的音频帧
        """
        frame = self.noise_suppression(frame)
        is_speech = self.voice_activity_detection(frame)
        return frame, is_speech