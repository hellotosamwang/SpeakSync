import time
import numpy as np
import sounddevice as sd
from src.audio.processor import AudioProcessor
from src.translation.engine import TranslationEngine
from src.ui.renderer import SubtitleRenderer

class LocalTester:
    def __init__(self):
        # 初始化各模块
        self.audio_processor = AudioProcessor()
        self.translation_engine = TranslationEngine({
            "providers": [{
                "name": "test",
                "endpoint": "http://localhost:8000/translate",
                "key": "test_key"
            }],
            "fallback": True
        })
        self.renderer = SubtitleRenderer()
        
        # 性能统计
        self.stats = {
            "audio_latency": [],
            "translation_latency": [],
            "render_latency": []
        }

    def test_audio_capture(self, duration=5):
        """测试音频采集"""
        print(f"\n=== 测试音频采集 ({duration}秒) ===")
        audio_data = []
        
        def callback(indata, frames, time, status):
            audio_data.append(indata.copy())
            
        with sd.InputStream(callback=callback,
                           channels=1,
                           samplerate=16000):
            print("正在采集音频... (请说话)")
            sd.sleep(int(duration * 1000))
            
        audio = np.concatenate(audio_data)
        print(f"采集到 {len(audio)/16000:.2f} 秒音频")
        return audio

    def test_full_pipeline(self, text="Hello world", lang="zh"):
        """测试完整流程"""
        print(f"\n=== 测试完整流程 (翻译到 {lang}) ===")
        
        # 模拟音频处理
        start_time = time.time()
        _, is_speech = self.audio_processor.process_frame(
            self._text_to_audio(text))
        audio_time = time.time()
        
        if is_speech:
            # 模拟识别结果直接使用输入文本
            trans_start = time.time()
            translation = self.translation_engine.translate(text, lang)
            trans_time = time.time()
            
            # 渲染字幕
            self.renderer.render(translation, 
                SubtitleStyle(font_size=24))
            render_time = time.time()
            
            # 记录性能
            self.stats["audio_latency"].append(audio_time - start_time)
            self.stats["translation_latency"].append(trans_time - trans_start)
            self.stats["render_latency"].append(render_time - trans_time)
            
            print(f"翻译结果: {translation}")
            print(f"音频处理: {(audio_time-start_time)*1000:.1f}ms")
            print(f"翻译耗时: {(trans_time-trans_start)*1000:.1f}ms")
            print(f"渲染耗时: {(render_time-trans_time)*1000:.1f}ms")
        else:
            print("未检测到语音")

    def _text_to_audio(self, text):
        """模拟语音生成（简化版）"""
        # 实际使用时替换为真实音频
        return np.random.rand(16000) * 0.1

    def run_interactive_test(self):
        """交互式测试"""
        print("""
        ==============================
        实时字幕翻译工具 - 本地测试控制台
        ==============================
        1. 测试音频采集
        2. 测试完整流程
        3. 查看性能统计
        4. 退出
        """)
        
        while True:
            choice = input("请选择测试项目 [1-4]: ")
            if choice == "1":
                self.test_audio_capture()
            elif choice == "2":
                text = input("输入测试文本: ")
                lang = input("目标语言代码(如zh): ")
                self.test_full_pipeline(text, lang)
            elif choice == "3":
                self.show_stats()
            elif choice == "4":
                break

    def show_stats(self):
        """显示性能统计"""
        print("\n=== 性能统计 ===")
        for k, v in self.stats.items():
            if v:
                avg = sum(v) / len(v) * 1000
                print(f"{k}: {avg:.1f}ms (共 {len(v)} 次)")
            else:
                print(f"{k}: 无数据")

if __name__ == "__main__":
    tester = LocalTester()
    tester.run_interactive_test()