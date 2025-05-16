# SpeakSync Real-time Subtitle Translator / 实时字幕翻译系统 / リアルタイム字幕翻訳システム / 실시간 자막 번역 시스템

## 🌍 Features / 功能特点 / 特徴 / 기능
- **Multi-scene Adaptation** / 多场景适配 / マルチシーン対応 / 다중 시나리오 지원
  - Academic/Education/Movie modes
  - 学术/教育/影视模式
  - 学術/教育/映画モード
  - 학술/교육/영화 모드

- **Ultra-low Latency** / 超低延迟 / 超低遅延 / 초저지연
  - End-to-end <1.5s latency
  - 端到端延迟<1.5秒
  - エンドツーエンド遅延<1.5秒
  - 엔드투엔드 지연 <1.5초

## 🛠️ SpeakSync Tool / SpeakSync工具 / SpeakSyncツール / SpeakSync 도구

### Core Functionality
```python
class SpeakSync:
    def __init__(self, mode='standard'):
        """
        :param mode: [standard|academic|entertainment]
        """
        self.audio_buffer = CircularBuffer()
        self.sync_controller = SyncController()
        
    def process(self, audio_frame):
        """Real-time audio processing"""
        return self._pipeline(audio_frame)
```

### Usage Example / 使用示例 / 使用例 / 사용 예제
```bash
# English
python speaksync.py --input mic --output screen --lang en

# 中文
python speaksync.py --input 麦克风 --output 屏幕 --lang zh

# 日本語
python speaksync.py --input マイク --output 画面 --lang ja

# 한국어
python speaksync.py --input 마이크 --output 화면 --lang ko
```

## 📦 Installation / 安装指南 / インストール / 설치 안내
### Prerequisites
```bash
# All languages
pip install -r requirements.txt
```

### Platform Specific
| OS       | Command                      |
|----------|------------------------------|
| Windows  | `install_win.bat`            |
| Linux    | `sudo ./install_linux.sh`    |
| macOS    | `brew install speaksync`     |

## 📄 Documentation / 文档 / ドキュメント / 문서
[Full Documentation](docs/en/INDEX.md) | 
[完整文档](docs/zh/INDEX.md) | 
[ドキュメント](docs/ja/INDEX.md) | 
[문서](docs/ko/INDEX.md)

## ⚠️ Known Issues / 已知问题 / 既知の問題 / 알려진 문제
- Japanese font rendering on Ubuntu
- Ubuntu上的日文字体渲染问题
- Ubuntuでの日本語フォント表示問題
- Ubuntu에서 일본어 폰트 렌더링 문제