import os
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=API_KEY)

app = FastAPI(title="AI-Powered Image Alt-Text Generator")

# We will use gemini-2.5-flash as it's the standard for multimodal fast tasks
MODEL_NAME = "gemini-2.5-flash"

# We'll create the static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.post("/api/generate")
async def generate_alt_text(
    image: UploadFile = File(...),
    caption: str = Form("")
):
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    if not API_KEY or API_KEY == "your_gemini_api_key_here":
        # Provide a mock response so the user can test the UI without a key
        import asyncio
        await asyncio.sleep(2) # simulate network latency
        return JSONResponse(content={
            "short_alt_text": "A diagram depicting the 7 chakras mapped to web development technologies.",
            "long_alt_text": f"The detailed infographic titled '7 Chakras of a Web Developer Mern Stack' features a white silhouette of a person sitting in a lotus position centered against a dark background with orange glowing patterns. Seven circular nodes map along the spine, connected to text labels and icons for MongoDB, Express, React, Node.js, HTML5, CSS3, and JavaScript, representing the chakra points. {('Additional context: ' + caption) if caption else ''}"
        })

    try:
        contents = await image.read()
        
        # Prepare the parts for Gemini
        image_parts = [
            {
                "mime_type": image.content_type,
                "data": contents
            }
        ]

        # Construct the prompt exactly as requested by the user
        prompt_text = f"""Analyze the provided image and generate both short alt text and long alt text following these guidelines:

Refer caption: '{caption}'

Formatting Rules:
- Use simple present tense throughout both descriptions
- Start the short alt text with an article such as A or An
- Start the long alt text strictly with the article The
- Include proper punctuation such as periods and commas
- Do not use hyphens, brackets, or colons in the text
- If the image contains charts, math, or code, do not use any symbols at all; spell them out completely in words (e.g., write "equals" instead of "=")
- Please ensure long alt does not repeat information from short alt text
- Focus on what is visually evident in the image without adding explanations
- Keep descriptions clear and concise
- Remove any inferences derived from the image
- Please ensure not to give any colour details in the alt text
- Remove information not adding value to the image content (like colour of bedsheet, wall etc.)
- Do not include introductory phrases like "The image shows"
- Ensure caption is not repeated - show only what image shows
- Include all labels in long alt text as well as all details shown

You MUST return ONLY a valid JSON object with exactly these two keys: "short_alt_text" and "long_alt_text"
Do not include any other text outside the JSON. Return this JSON and nothing else:

{{"short_alt_text": "...", "long_alt_text": "..."}}"""

        model = genai.GenerativeModel(MODEL_NAME)
        
        response = model.generate_content(
            contents=[prompt_text, image_parts[0]]
        )
        
        # Parse JSON string from response
        response_text = response.text.strip()
        
        # Try to extract JSON if it's embedded in the response
        if response_text.startswith('{'):
            json_str = response_text
        else:
            # Look for JSON block in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text
        
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON. Response was: {response_text[:500]}")
            raise HTTPException(status_code=500, detail=f"Invalid JSON response from Gemini API")
        
        return JSONResponse(content={
            "short_alt_text": result.get("short_alt_text", ""),
            "long_alt_text": result.get("long_alt_text", "")
        })

    except Exception as e:
        print(f"Error during generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate alt text: {str(e)}")

@app.get("/")
async def root():
    # Redirect root to /static/index.html
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
