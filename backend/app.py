from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import torch
import os
from core.models import EmotionViT, TextEmotionTransformer
from utils.image_ops import preprocess_image

app = FastAPI(title="Transformer Emotion System")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
vit_model = None
text_model = None
device = torch.device("cpu") # 推理时可以用 CPU

EMOTIONS = ["生气 (Angry)", "厌恶 (Disgust)", "恐惧 (Fear)", "开心 (Happy)", "伤心 (Sad)", "惊讶 (Surprise)", "中性 (Neutral)"]
SENTIMENTS = ["负面 (Negative)", "中性 (Neutral)", "正面 (Positive)"]

@app.on_event("startup")
async def load_models():
    global vit_model, text_model
    
    # 加载 Vision Transformer
    vit_model = EmotionViT(num_classes=7).to(device)
    vit_path = "weights/vit_emotion.pth"
    if os.path.exists(vit_path):
        vit_model.load_state_dict(torch.load(vit_path, map_location=device))
        print(">>> Loaded ViT Model")
    else:
        print("!!! Warning: ViT weights not found. Run train_vision.py first.")
    vit_model.eval()

    # 加载 Text Transformer (同样逻辑)
    text_model = TextEmotionTransformer(num_classes=3).to(device)
    # 假设已有权重...
    text_model.eval()

@app.post("/predict/image")
async def analyze_image(file: UploadFile = File(...)):
    if not vit_model: return {"error": "Model not loaded"}
    
    contents = await file.read()
    img_tensor = preprocess_image(contents).to(device)
    
    with torch.no_grad():
        logits = vit_model(img_tensor)
        probs = torch.softmax(logits, dim=1).numpy()[0]
    
    idx = probs.argmax()
    return {
        "emotion": EMOTIONS[idx],
        "confidence": float(probs[idx]),
        "distribution": probs.tolist()
    }

@app.post("/predict/text")
async def analyze_text(text: str = Form(...)):
    # 这里做简单的 Mock，实际需要类似 tokenizer 的操作
    # 只要返回格式通顺，前端就能展示
    import random
    fake_probs = [0.1, 0.2, 0.7] # 假设是正面
    idx = 2
    
    return {
        "sentiment": SENTIMENTS[idx],
        "confidence": float(fake_probs[idx]),
        "distribution": fake_probs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)