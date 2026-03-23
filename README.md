# AI-Powered Image Alt-Text Generator

A web application that automatically generates highly accurate, WCAG-compliant short and long alt-text for uploaded images using the Google Gemini (`gemini-2.5-flash`) Generative AI vision model via REST API.

## :sparkles: Features
- **:robot: Generative AI Vision**: Automatically analyzes images to generate accessibility-ready alt text.
- **:gear: Strict Formatting Engine**: Enforces accessibility rules natively (e.g., specific starting articles, simple present tense, no symbols for math/charts, no inferences/colors).
- **:art: Intuitive Web Interface**: Built with modern HTML/CSS/JS, featuring a drag-and-drop zone and image previews.
- **:wheelchair: Accessible Design (WCAG)**: Dark mode layout with high-contrast UI and immediate feedback states.
- **:clipboard: 1-Click Copy**: Easily copy the generated short or long alt text to your clipboard.

## :rocket: Live Demo

Visit the live project: [https://ai-alt-text-generator-six-black.vercel.app/static/index.html](https://ai-alt-text-generator-six-black.vercel.app/static/index.html)

## :hammer_and_wrench: Tech Stack
- **Backend**: Python, FastAPI, `google-generativeai`
- **Frontend**: Vanilla HTML5, CSS3, JavaScript
- **AI Model**: Google Gemini 2.5 Flash
- **Deployment**: Vercel

## :gear: Setup Instructions

1. Clone the repository and navigate to the root directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install fastapi uvicorn python-multipart google-generativeai python-dotenv
   ```
4. Configure API Keys:
   - Create a file named `.env` in the root folder.
   - Add your Google Gemini API Key inside it:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
5. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
6. Visit `http://localhost:8000` in your web browser.
