import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import torch

# ==========================================
# 1. 生命周期管理
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f">>> 系统启动，正在加载 AI 模型...")
    # 这里加载你的模型，例如:
    # app.state.model = MyModel()
    yield
    print(">>> 系统关闭")

app = FastAPI(lifespan=lifespan)

# ==========================================
# 2. 你的 API 接口 (必须放在静态文件挂载之前)
# ==========================================
@app.post("/predict/image")
async def predict_image():
    return {"message": "这是测试接口，你的模型逻辑应该放在这"}

@app.post("/predict/text")
async def predict_text():
    return {"message": "Text API works"}

# ==========================================
# 3. 静态文件托管 (最稳健的写法)
# ==========================================
# 获取 dist 绝对路径
frontend_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

if os.path.exists(frontend_dist_path):
    print(f"前端路径挂载成功: {frontend_dist_path}")
    
    # 【方案 A】: 挂载静态资源 (assets, css, js 等)
    # Vue CLI 生成的 js/css 文件夹，我们需要显式挂载，否则 index.html 里的 <script src="/js/..."> 找不到
    for dir_name in ["css", "js", "img", "assets"]:
        full_path = os.path.join(frontend_dist_path, dir_name)
        if os.path.isdir(full_path):
            app.mount(f"/{dir_name}", StaticFiles(directory=full_path), name=dir_name)
            print(f"  - 已挂载: /{dir_name}")

    # 【方案 B】: 根路径 catch-all (解决 SPA 路由和 index.html)
    # 任何没有被上面 API 捕获的请求，都返回 index.html
    # 这样你就不用担心 favicon.ico 或者 user/123 这种前端路由报错了
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # 如果请求的是个具体文件 (比如 favicon.ico)，且该文件存在，就返回文件
        file_path = os.path.join(frontend_dist_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # 否则一律返回 index.html (SPA 的核心)
        return FileResponse(os.path.join(frontend_dist_path, "index.html"))

else:
    print(f"!!! 警告: 找不到 dist 文件夹: {frontend_dist_path}")

if __name__ == "__main__":
    import uvicorn
    # 建议 host 写 127.0.0.1 避免 0.0.0.0 的误解，但写 0.0.0.0 也没错
    uvicorn.run(app, host="0.0.0.0", port=8000)