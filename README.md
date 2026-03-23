🚀 AI-Powered Image Alt-Text Generator

🔗 Live Demo:
👉 https://ai-alt-text-generator-six-black.vercel.app/static/index.html

🌟 Overview

A web application that generates accurate, accessibility-friendly alt text for images using AI.
It helps make images WCAG-compliant by producing both short and long descriptions automatically.

✨ Features
🤖 AI Vision – Generates alt text using Google Gemini
⚙️ Smart Formatting – Follows accessibility rules (simple language, no unnecessary details)
🎨 Clean UI – Drag & drop image upload with preview
♿ Accessible Design – High contrast + dark mode support
📋 Copy in One Click – Quickly copy generated text
🛠 Tech Stack
Backend: Python, FastAPI
Frontend: HTML, CSS, JavaScript
AI Model: Gemini 2.5 Flash
Deployment: Vercel
⚡ Setup
1. Clone repo
git clone <your-repo-url>
cd <repo-folder>
2. Create virtual environment
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
3. Install dependencies
pip install fastapi uvicorn python-multipart google-generativeai python-dotenv
4. Add API key

Create .env file:

GEMINI_API_KEY=your_api_key_here
5. Run project
uvicorn main:app --host 0.0.0.0 --port 8000
6. Open in browser

👉 http://localhost:8000