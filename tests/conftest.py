import pytest
from src.core.controller import SystemController
from src.audio.processor import AudioProcessor
from src.translation.engine import TranslationEngine
from src.ui.renderer import SubtitleRenderer

@pytest.fixture
def sample_config():
    return {
        "audio": {
            "sample_rate": 16000,
            "buffer_size": 2000
        },
        "translation": {
            "providers": [
                {
                    "name": "test",
                    "endpoint": "http://mock/api",
                    "key": "test_key"
                }
            ],
            "fallback": True,
            "target_lang": "en"
        },
        "ui": {
            "style": {
                "font_name": "Arial",
                "font_size": 24,
                "color": [255, 255, 255],
                "position": "bottom"
            }
        },
        "performance": {
            "max_latency": 2000
        }
    }

@pytest.fixture
def mock_controller(sample_config):
    return SystemController(sample_config)

@pytest.fixture
def audio_processor(sample_config):
    return AudioProcessor(**sample_config["audio"])

@pytest.fixture
def translation_engine(sample_config):
    return TranslationEngine(sample_config["translation"])

@pytest.fixture
def subtitle_renderer():
    return SubtitleRenderer()