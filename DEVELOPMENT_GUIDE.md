# 实时字幕翻译系统开发指南

## 1. 开发环境配置

### 1.1 基础环境
```bash
# 创建虚拟环境 (Python 3.8+)
python -m venv .venv

# 激活环境
# Linux/macOS:
source .venv/bin/activate  
# Windows:
.venv\Scripts\activate

# 安装依赖
pip install -r requirements-dev.txt
```

### 1.2 平台特定配置
#### Windows:
```powershell
# 安装音频开发包
choco install portaudio -y
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt install portaudio19-dev python3-dev

# CentOS/RHEL 
sudo yum install portaudio-devel python3-devel
```

#### macOS:
```bash
brew install portaudio
```

## 2. 开发工具配置

### 2.1 VS Code推荐插件
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "eamodio.gitlens",
    "GitHub.vscode-pull-request-github",
    "EditorConfig.EditorConfig"
  ]
}
```

### 2.2 代码格式化配置 (.editorconfig)
```ini
[*.py]
indent_style = space
indent_size = 4
max_line_length = 120
```

## 3. 测试环境准备

### 3.1 测试数据生成
```python
# tests/generate_test_data.py
import numpy as np

def generate_audio(duration=1.0, sample_rate=16000):
    t = np.linspace(0, duration, int(sample_rate * duration))
    return 0.5 * np.sin(2 * np.pi * 440 * t)
```

### 3.2 模拟翻译服务
```bash
# 启动测试API服务
python -m http.server 8000 &
```

## 4. 开发工作流

### 4.1 日常开发流程
```bash
# 1. 创建特性分支
git flow feature start [feature-name]

# 2. 开发并运行测试
pytest tests/ -xvs --cov=src

# 3. 提交代码
git commit -m "feat(module): description" 

# 4. 创建PR并审核
git flow feature finish [feature-name]
```

### 4.2 文档生成
```bash
# 生成API文档
sphinx-apidoc -o docs/source src/
make -C docs/ html

# 构建用户手册
mkdocs build
```

## 5. 调试技巧

### 5.1 音频调试
```python
import sounddevice as sd
sd.play(test_audio, samplerate=16000)
```

### 5.2 性能分析
```python
# 使用cProfile
python -m cProfile -o profile.stats main.py
```

## 6. 常见问题

### 6.1 音频设备问题
```text
解决方案：
1. 检查默认音频设备
2. 确认采样率支持
3. 测试PortAudio安装
```

### 6.2 翻译API限制
```text
解决方案：
1. 使用缓存机制
2. 实现请求队列
3. 添加备用服务商
```

## 7. 发布流程

```mermaid
graph LR
    A[代码冻结] --> B[版本测试]
    B --> C[文档生成]
    C --> D[打包发布]
    D --> E[版本归档]
```