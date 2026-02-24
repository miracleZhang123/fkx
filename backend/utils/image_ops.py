import cv2
import numpy as np
import torch

def preprocess_image(image_bytes, target_size=(48, 48)):
    # 将字节转换为 numpy 数组
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # BGR
    
    # 转换为 RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 可以在这里加入 OpenCV 人脸检测 (Haar Cascade) 来裁剪人脸
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # faces = face_cascade.detectMultiScale(img, 1.1, 4)
    # if len(faces) > 0:
    #     x, y, w, h = faces[0]
    #     img = img[y:y+h, x:x+w]

    # Resize
    img = cv2.resize(img, target_size)
    
    # 归一化并转为 Tensor [C, H, W]
    img = img.astype(np.float32) / 255.0
    tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0) # Add batch dim
    return tensor