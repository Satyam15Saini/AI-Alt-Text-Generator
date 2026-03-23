# Ì∫Ä AI-Powered Image Alt-Text Generator

[![Live Demo](https://img.shields.io/badge/Ì¥ó%20Live%20Demo-Visit%20Now-brightgreen?style=for-the-badge)](https://ai-alt-text-generator-six-black.vercel.app/static/index.html)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-brightgreen?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)

---

## **Ìºü Overview**

A web application that generates accurate, accessibility-friendly alt text for images using AI. It helps make images WCAG-compliant by producing both short and long descriptions automatically.

---

## **‚ú® Features**

- Ì¥ñ **AI Vision** ‚Äì Generates alt text using Google Gemini  
- ‚öôÔ∏è **Smart Formatting** ‚Äì Follows accessibility rules (simple language, no unnecessary details)  
- Ìæ® **Clean UI** ‚Äì Drag & drop image upload with preview  
- ‚ôø **Accessible Design** ‚Äì High contrast + dark mode support  
- Ì≥ã **Copy in One Click** ‚Äì Quickly copy generated text  

---

## **Ìª† Tech Stack**

| Component | Technology |
|-----------|------------|
| **Backend** | Python, FastAPI |
| **Frontend** | HTML, CSS, JavaScript |
| **AI Model** | Gemini 2.5 Flash |
| **Deployment** | Vercel |

---

## **‚ö° Quick Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/Satyam15Saini/AI-Alt-Text-Generator.git
cd AI-Alt-Text-Generator
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install fastapi uvicorn python-multipart google-generativeai python-dotenv
```

### **4. Configure API Key**

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### **5. Run the Application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### **6. Open in Browser**

Ì±â Visit: **[http://localhost:8000](http://localhost:8000)**

---

## **Ì∫Ä Live Demo**

Ì±â **[Try the Live Demo Now!](https://ai-alt-text-generator-six-black.vercel.app/static/index.html)**

---

## **Ì≥ù License**

This project is open source and available under the MIT License.

---

**Made with ‚ù§Ô∏è by [Satyam15Saini](https://github.com/Satyam15Saini)**
