import pytest
from unittest.mock import patch, MagicMock
from tests.conftest import translation_engine
from src.translation.engine import TranslationEngine

class TestTranslationEngine:
    @patch('requests.post')
    def test_translation_api(self, mock_post, translation_engine):
        # 模拟API成功响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'translation': '测试翻译'
        }
        mock_post.return_value = mock_response

        result = translation_engine.translate("test", "zh")
        assert result == "测试翻译"
        assert mock_post.called

    @patch('requests.post')
    def test_api_failure(self, mock_post, translation_engine):
        # 模拟API失败
        mock_post.side_effect = Exception("API error")
        
        # 测试降级翻译
        result = translation_engine.translate("test", "zh")
        assert result == "test"  # 应返回原文
        
    def test_cache_mechanism(self, translation_engine):
        # 测试缓存功能
        test_text = "cache test"
        
        # 第一次调用(未缓存)
        with patch.object(translation_engine, '_call_provider') as mock_call:
            mock_call.return_value = "cached translation"
            result1 = translation_engine.translate(test_text, "en")
        
        # 第二次调用(应使用缓存)
        with patch.object(translation_engine, '_call_provider') as mock_call:
            result2 = translation_engine.translate(test_text, "en")
            assert not mock_call.called  # 不应再次调用API
            assert result2 == result1

    @patch('requests.post')
    def test_provider_fallback(self, mock_post, translation_engine):
        # 测试提供商故障转移
        # 第一次调用模拟失败
        mock_post.side_effect = [
            Exception("First provider failed"),
            MagicMock(status_code=200, json=lambda: {'translation': 'fallback'})
        ]
        
        result = translation_engine.translate("test", "ja")
        assert result == "fallback"
        assert mock_post.call_count == 2  # 应尝试第二个提供商

    @pytest.mark.performance
    def test_concurrent_translation(self, translation_engine):
        # 并发性能测试
        from concurrent.futures import ThreadPoolExecutor
        import time
        
        test_data = [("text{}".format(i), "en") for i in range(50)]
        
        def translate(args):
            text, lang = args
            return translation_engine.translate(text, lang)
            
        start = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(translate, test_data))
        elapsed = time.time() - start
        
        assert len(results) == 50
        assert elapsed < 5.0  # 50个翻译应在5秒内完成