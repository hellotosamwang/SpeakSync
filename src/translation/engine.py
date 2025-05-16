import requests
from cachetools import TTLCache
from typing import Dict, Optional

class TranslationEngine:
    def __init__(self, config: Dict):
        """
        多引擎翻译控制器
        :param config: 引擎配置
        """
        self.providers = config['providers']
        self.cache = TTLCache(maxsize=1000, ttl=3600)
        self.fallback_enabled = config.get('fallback', True)
        self.current_provider = 0
        
    def translate(self, text: str, target_lang: str, 
                 domain: Optional[str] = None) -> str:
        """
        执行翻译
        :param text: 待翻译文本
        :param target_lang: 目标语言代码
        :param domain: 专业领域(可选)
        :return: 翻译结果
        """
        cache_key = f"{text}_{target_lang}_{domain}"
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        for attempt in range(3):
            try:
                provider = self.providers[self.current_provider]
                result = self._call_provider(provider, text, target_lang, domain)
                self.cache[cache_key] = result
                return result
            except Exception as e:
                self._handle_error(e)
                if not self.fallback_enabled:
                    raise
                    
        return self._fallback_translation(text)

    def _call_provider(self, provider: Dict, text: str, 
                      target_lang: str, domain: str) -> str:
        """
        调用具体翻译API
        """
        url = provider['endpoint']
        headers = {'Authorization': f"Bearer {provider['key']}"}
        data = {
            'text': text,
            'target': target_lang,
            'domain': domain
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()['translation']
        
    def _handle_error(self, error: Exception):
        """
        处理翻译错误
        """
        # 切换备用提供商
        self.current_provider = (self.current_provider + 1) % len(self.providers)
        # 记录错误日志
        print(f"Translation error: {str(error)}")
        
    def _fallback_translation(self, text: str) -> str:
        """
        降级翻译方案
        """
        # 简单词典查找或返回原文
        return text