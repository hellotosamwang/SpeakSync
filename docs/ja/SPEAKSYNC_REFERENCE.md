# SpeakSync 技術リファレンス

## 音声処理フロー
```mermaid
graph LR
    A[音声入力] --> B[ノイズ抑制]
    B --> C[音声活動検出]
    C --> D[音声認識]
    D --> E[文脈解析]
    E --> F[翻訳]
    F --> G[字幕表示]
```

## 主要パラメータ
| パラメータ | 型 | デフォルト | 説明 |
|-----------|----|-----------|------|
| `--mode` | 文字列 | `standard` | 動作モード(academic/entertainment) |
| `--lang` | 文字列 | `en` | 対象言語コード |
| `--threads` | 整数 | `4` | 処理スレッド数 |
| `--buffer` | 整数 | `2000` | 音声バッファサイズ(ms) |

## 性能チューニング
```python
# 学術用途推奨設定
config = {
    "vad_aggressiveness": 2,
    "max_alternatives": 1,
    "timeout": 3000,
    "enable_punctuation": True
}
```

## シーン別設定
### 学術会議
```yaml
preset:
  name: academic
  features:
    - speaker_diarization
    - term_highlight
  params:
    min_confidence: 0.9
    enable_glossary: true
```

### ライブ授業
```yaml
preset:
  name: education  
  params:
    simplify_sentences: true
    keyword_emphasis: true
    speed_limit: 1.2x
```

## エラー処理
| コード | 深刻度 | 回復処理 |
|------|-------|----------|
| 1001 | 警告 | 音声取得再試行 |
| 2003 | 深刻 | 予備モデル切替 |
| 3005 | 致命的 | サービス再起動 |
```