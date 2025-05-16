import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from tests.conftest import mock_controller
from src.core.controller import SystemState

class TestIntegration:
    @pytest.fixture
    def mock_audio(self):
        # 生成测试音频信号
        t = np.linspace(0, 1, 16000)
        return 0.5 * np.sin(2 * np.pi * 440 * t)

    @patch('src.audio.processor.AudioProcessor.capture_frame')
    @patch('src.translation.engine.TranslationEngine._call_provider')
    @patch('src.ui.renderer.SubtitleRenderer.render')
    def test_full_pipeline(self, mock_render, mock_translate, mock_capture, 
                         mock_controller, mock_audio):
        # 设置模拟返回值
        mock_capture.return_value = mock_audio
        mock_translate.return_value = {"translation": "测试翻译"}
        
        # 启动控制器
        mock_controller.start()
        
        # 验证状态转换
        assert mock_controller.state == SystemState.PROCESSING
        
        # 等待处理完成
        import time
        time.sleep(0.1)
        
        # 验证各模块调用
        assert mock_capture.called
        assert mock_translate.called
        assert mock_render.called
        
        # 停止系统
        mock_controller.stop()

    @patch('src.translation.engine.TranslationEngine._call_provider')
    def test_latency_measurement(self, mock_translate, mock_controller):
        # 测试端到端延迟
        mock_translate.side_effect = [
            {"translation": "测试1"},
            {"translation": "测试2"},
            {"translation": "测试3"}
        ]
        
        mock_controller.start()
        time.sleep(0.5)  # 运行500ms
        
        # 验证延迟指标
        stats = mock_controller.performance_stats
        assert stats['audio_latency'] > 0
        assert stats['translation_latency'] > 0
        assert stats['render_latency'] > 0
        
        total_latency = sum(stats.values())
        assert total_latency < 1000  # 总延迟应<1s
        mock_controller.stop()

    @patch('src.translation.engine.TranslationEngine._call_provider')
    def test_error_recovery(self, mock_translate, mock_controller):
        # 测试错误恢复
        mock_translate.side_effect = [
            Exception("First error"),
            {"translation": "恢复后的翻译"}
        ]
        
        mock_controller.start()
        time.sleep(0.1)
        
        # 验证状态恢复
        assert mock_controller.state == SystemState.PROCESSING
        mock_controller.stop()

    @pytest.mark.stress
    def test_concurrent_processing(self, mock_controller):
        # 压力测试：模拟高并发
        from concurrent.futures import ThreadPoolExecutor
        
        def simulate_user():
            mock_controller.start()
            time.sleep(0.01)
            mock_controller.stop()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(simulate_user) for _ in range(20)]
            for f in futures:
                f.result()  # 等待所有完成
        
        # 验证无资源泄漏
        assert len(mock_controller.threads) == 0

    @patch('src.audio.processor.AudioProcessor.process_frame')
    def test_degraded_mode(self, mock_process, mock_controller):
        # 测试降级模式
        mock_process.side_effect = Exception("模拟过载")
        
        mock_controller.start()
        time.sleep(0.1)
        
        # 验证进入降级状态
        assert mock_controller.state == SystemState.ERROR
        mock_controller.stop()