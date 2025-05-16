from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/translate")
async def translate(text: str, target_lang: str):
    """模拟翻译API接口"""
    return {
        "translation": f"[MOCK] {text}",
        "detected_language": "en",
        "confidence": 0.95
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "OK"}

if __name__ == "__main__":
    # 启动模拟服务器
    uvicorn.run(app, host="0.0.0.0", port=8000)