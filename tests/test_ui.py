import pytest
import pygame
from unittest.mock import MagicMock
from tests.conftest import subtitle_renderer
from src.ui.renderer import SubtitleRenderer, SubtitleStyle

class TestUIRenderer:
    @pytest.fixture(autouse=True)
    def setup_renderer(self):
        # 初始化pygame显示
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_text_rendering(self, subtitle_renderer):
        # 测试基本文本渲染
        style = SubtitleStyle(
            font_name="Arial",
            font_size=24,
            color=(255, 255, 255)
        )
        
        # 模拟pygame.font.render
        with patch('pygame.font.Font.render') as mock_render:
            mock_render.return_value = MagicMock(get_size=lambda: (100, 20))
            subtitle_renderer.render("Test Text", style)
            
            assert mock_render.called
            args, kwargs = mock_render.call_args
            assert args[0] == "Test Text"
            assert kwargs['color'] == (255, 255, 255)

    def test_style_application(self, subtitle_renderer):
        # 测试样式属性应用
        style = SubtitleStyle(
            font_name="Times New Roman",
            font_size=32,
            color=(255, 0, 0),
            background=(0, 0, 0, 128),
            outline=(0, 0, 255),
            position="top"
        )
        
        with patch('pygame.font.Font') as mock_font:
            mock_font.return_value.render.return_value = MagicMock(get_size=lambda: (150, 30))
            subtitle_renderer.render("Styled Text", style)
            
            # 验证字体创建
            assert mock_font.called
            assert mock_font.call_args[0][1] == 32  # 字体大小

    def test_unicode_support(self, subtitle_renderer):
        # 测试Unicode字符渲染
        test_cases = [
            ("中文测试", "NotoSansSC"),
            ("日本語テスト", "NotoSansJP"),
            ("한글 테스트", "NanumGothic")
        ]
        
        for text, font in test_cases:
            style = SubtitleStyle(font_name=font)
            try:
                subtitle_renderer.render(text, style)
            except pygame.error:
                pytest.fail(f"Failed to render {text} with {font}")

    @pytest.mark.performance
    def test_rendering_performance(self, subtitle_renderer):
        # 渲染性能测试
        import time
        style = SubtitleStyle()
        
        start = time.time()
        for _ in range(100):
            subtitle_renderer.render("Performance Test", style)
        elapsed = time.time() - start
        
        assert elapsed < 1.0  # 100次渲染应在1秒内完成

    def test_cache_mechanism(self, subtitle_renderer):
        # 测试纹理缓存
        style = SubtitleStyle()
        
        with patch('pygame.font.Font.render') as mock_render:
            mock_render.return_value = MagicMock(get_size=lambda: (100, 20))
            
            # 第一次渲染
            subtitle_renderer.render("Cached Text", style)
            call_count = mock_render.call_count
            
            # 第二次渲染相同文本
            subtitle_renderer.render("Cached Text", style)
            assert mock_render.call_count == call_count  # 不应再次调用render

    def test_error_handling(self, subtitle_renderer):
        # 测试错误处理
        with patch('pygame.font.Font.render', side_effect=pygame.error):
            try:
                subtitle_renderer.render("Error Test", SubtitleStyle())
            except Exception as e:
                pytest.fail(f"Renderer crashed with error: {str(e)}")