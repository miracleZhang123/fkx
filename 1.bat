@echo off
chcp 65001 > nul
echo ==============================================
echo 正在创建 Multimodal-Emotion-System 项目目录结构
echo ==============================================

:: 设置项目根目录名称
set "PROJECT_ROOT="

:: 创建根目录
mkdir "%PROJECT_ROOT%"
echo [1/4] 已创建根目录: %PROJECT_ROOT%

:: 创建根目录下的空文件
cd "%PROJECT_ROOT%"
type nul > README.md
type nul > requirements.txt
echo [2/4] 已创建根目录文件: README.md, requirements.txt

:: 创建 train_scripts 目录及文件
mkdir train_scripts
cd train_scripts
type nul > datasets.py
type nul > train_vision.py
type nul > train_text.py
cd ..
echo [3/4] 已创建 train_scripts 目录及文件

:: 创建 backend 目录及子目录/文件
mkdir backend
cd backend
type nul > app.py

:: 创建 backend/core 子目录及文件
mkdir core
cd core
type nul > config.py
type nul > models.py
cd ..

:: 创建 backend/utils 子目录及文件
mkdir utils
cd utils
type nul > image_ops.py
type nul > text_ops.py
cd ..

:: 创建 backend/weights 子目录及空的模型文件（仅占位）
mkdir weights
cd weights
type nul > vit_emotion.pth
type nul > text_emotion.pth
cd ..
cd ..
echo [4/4] 已创建 backend 目录及所有子文件/目录

:: 创建 frontend 目录及子目录/文件
mkdir frontend
cd frontend
type nul > package.json

:: 创建 frontend/public 子目录
mkdir public

:: 创建 frontend/src 子目录及文件
mkdir src
cd src
type nul > App.vue
type nul > main.js
type nul > api.js

:: 创建 frontend/src/components 子目录及文件
mkdir components
cd components
type nul > ImageAnalyzer.vue
type nul > TextAnalyzer.vue
cd ..
cd ..
cd ..

echo ==============================================
echo 目录结构创建完成！
echo 项目根目录: %cd%\%PROJECT_ROOT%
echo ==============================================
pause