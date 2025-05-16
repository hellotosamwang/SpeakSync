import numpy as np
import pytest
from tests.conftest import audio_processor

class TestAudioProcessor:
    @pytest.fixture
    def sample_frame(self):
        # 生成1秒的测试音频(16kHz采样率)
        t = np.linspace(0, 1, 16000)
        signal = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440Hz正弦波
        noise = 0.1 * np.random.randn(16000)  # 高斯噪声
        return signal + noise

    def test_noise_suppression(self, audio_processor, sample_frame):
        # 测试噪声抑制功能
        processed_frame = audio_processor.noise_suppression(sample_frame)
        assert processed_frame.shape == sample_frame.shape
        assert np.max(processed_frame) <= np.max(sample_frame)

    def test_vad_detection(self, audio_processor):
        # 测试语音活动检测
        silence = np.zeros(16000)  # 静音帧
        voice = 0.3 * np.random.randn(16000)  # 语音帧
        
        _, is_speech_silence = audio_processor.process_frame(silence)
        _, is_speech_voice = audio_processor.process_frame(voice)
        
        assert not is_speech_silence
        assert is_speech_voice

    @pytest.mark.performance
    def test_processing_speed(self, audio_processor, sample_frame):
        # 性能测试：处理100帧的耗时
        import time
        start = time.time()
        for _ in range(100):
            audio_processor.process_frame(sample_frame)
        elapsed = time.time() - start
        assert elapsed < 0.5  # 100帧应在0.5秒内完成