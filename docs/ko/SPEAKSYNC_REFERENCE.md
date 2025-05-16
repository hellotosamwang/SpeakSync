# SpeakSync 기술 레퍼런스

## 오디오 처리 프로세스
```mermaid
graph LR
    A[오디오 입력] --> B[잡음 제거]
    B --> C[음성 활동 감지]
    C --> D[음성 인식]
    D --> E[문맥 분석]
    E --> F[번역]
    F --> G[자막 렌더링]
```

## 주요 파라미터
| 파라미터 | 유형 | 기본값 | 설명 |
|---------|------|-------|------|
| `--mode` | 문자열 | `standard` | 동작 모드(academic/entertainment) |
| `--lang` | 문자열 | `en` | 대상 언어 코드 |
| `--threads` | 정수 | `4` | 처리 스레드 수 |
| `--buffer` | 정수 | `2000` | 오디오 버퍼 크기(ms) |

## 성능 튜닝
```python
# 학술 시나리오 추천 설정
config = {
    "vad_aggressiveness": 2,
    "max_alternatives": 1,
    "timeout": 3000,
    "enable_punctuation": True
}
```

## 장면별 설정
### 학술 회의
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

### 실시간 교육
```yaml
preset:
  name: education  
  params:
    simplify_sentences: true
    keyword_emphasis: true
    speed_limit: 1.2x
```

## 오류 처리
| 코드 | 심각도 | 복구 조치 |
|------|--------|----------|
| 1001 | 경고 | 오디오 캡처 재시도 |
| 2003 | 심각 | 예비 모델 전환 |
| 3005 | 치명적 | 서비스 재시작 |
```

## 한국어 특화 기능
```python
# 한영 자동 전환 설정
korean_config = {
    "auto_switch_lang": True,
    "font": "NanumGothic",
    "line_break": "word"
}
```