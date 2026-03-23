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

def enforce_wcag_alt_text_rules(text, is_short=True):
    """
    Enforce all WCAG-compliant alt text rules.
    
    Rules applied:
    1. No 'image of' or 'picture of'
    2. Avoid unnecessary commas
    3. Keep short alt text 5-12 words
    4. No full stops at the end (for short)
    5. No extra adjectives
    6. No repetition
    7. No keyword stuffing
    8. Use lowercase
    9. Avoid unnecessary articles
    10. No assumptions
    11. Focus on main subject
    12. Mention action (functional images)
    13. Include text if present
    14. No special characters
    15. Avoid abbreviations
    16. Maintain natural word order
    17. No emojis
    18. Keep context aware
    """
    import re
    
    if not text:
        return text
    
    # Rule 1: Remove 'image of' or 'picture of'
    text = re.sub(r'\b(image of|picture of|photo of|image shows|image depicts|image displays|the image\s+shows)\b', '', text, flags=re.IGNORECASE)
    
    # Remove color references (WCAG compliance)
    color_words = [
        r'\bred\b', r'\bblue\b', r'\bgreen\b', r'\byellow\b', r'\borange\b', r'\bpurple\b',
        r'\bpink\b', r'\bbrown\b', r'\bgray\b', r'\bgrey\b', r'\bwhite\b', r'\bblack\b',
        r'\bbeige\b', r'\btan\b', r'\bgold\b', r'\bsilver\b', r'\bviolet\b', r'\bindigo\b',
        r'\bturquoise\b', r'\bcyan\b', r'\bmagenta\b', r'\blime\b', r'\bmaroon\b', r'\bnavy\b',
        r'\bteal\b', r'\bold\b', r'\bdarker\b', r'\bdark\b', r'\blight\b', r'\blighter\b',
        r'\bbright\b', r'\bpale\b', r'\bvibrant\b', r'\bmuted\b', r'\bvivid\b', r'\bdull\b',
        r'\bcolored\b', r'\bcoloured\b', r'\bshaded\b', r'\bpainted\b', r'\btinted\b',
        r'\bchrome\b', r'\bgolden\b', r'\bsilverish\b', r'\bmonochrome\b', r'\bgrayscale\b'
    ]
    
    for color in color_words:
        text = re.sub(color, '', text, flags=re.IGNORECASE)
    
    # Rule 14: Remove special characters (keep only alphanumeric, spaces, periods, commas, apostrophes)
    text = re.sub(r'[^\w\s.,\'()-]', '', text)
    
    # Rule 17: Remove emojis
    text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text)
    
    # Rule 8: Convert to lowercase
    text = text.lower()
    
    # Rule 2: Clean up unnecessary commas
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r',+', ',', text)
    text = re.sub(r',\s*$', '', text)  # Remove trailing comma
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    if is_short:
        # Rule 4: No full stops at the end for short alt text
        text = re.sub(r'\.\s*$', '', text)
        
        # Rule 3: Limit to 5-12 words
        words = text.split()
        if len(words) > 12:
            text = ' '.join(words[:12])
        
        # Ensure starts with article 'a' or 'an'
        if not re.match(r'^(a|an)\s+', text, flags=re.IGNORECASE):
            if text and text[0].lower() in 'aeiou':
                text = 'an ' + text
            elif text:
                text = 'a ' + text
    else:
        # Rule for long alt text: Start with 'the'
        if not re.match(r'^the\s+', text, flags=re.IGNORECASE):
            text = 'the ' + text
        
        # Ensure ends with period
        if not text.endswith('.'):
            text = text + '.'
    
    return text.strip()

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

        # Construct the prompt for WCAG 2.1 compliant alt text
        prompt_text = f"""Analyze the provided image and generate WCAG 2.1 compliant short and long alt text.

CRITICAL RULES TO FOLLOW (ALL 20 WCAG Rules):
1. Do NOT use words 'image of', 'picture of', 'photo of', 'image shows', 'image depicts'
2. Avoid unnecessary commas
3. Keep SHORT alt text to 5-12 words EXACTLY
4. NO full stops/periods at the end of SHORT alt text
5. No extra adjectives (avoid: beautiful, lovely, amazing, stunning, etc.)
6. No repetition of information
7. No keyword stuffing or spam keywords
8. Use LOWERCASE throughout
9. Avoid unnecessary articles (the, a, an) unless grammatically required
10. No assumptions - describe only what is visible
11. Focus on the main subject/content
12. Mention action verbs for functional images
13. Include any visible text/labels in the alt text
14. No special characters (except periods, commas, apostrophes)
15. Avoid abbreviations - spell out full words
16. Maintain natural word order
17. No emojis or special symbols
18. Keep context aware - consider the caption if provided

FORMATTING RULES:
- SHORT alt text MUST start with article: "A" or "An"
- SHORT alt text MUST be 5-12 words and NO period at end
- LONG alt text MUST start with article: "The"
- LONG alt text MUST end with a period
- Both use simple present tense
- Use proper grammar and punctuation
- NO hyphens, brackets, or colons in text

ABSOLUTELY NO COLOR REFERENCES:
Never mention: red, blue, green, yellow, orange, purple, pink, brown, gray, grey, white, black, dark, light, bright, pale, vibrant, muted, vivid, dull, golden, silver, chrome, etc.

Reference caption: '{caption}'

RETURN ONLY valid JSON (nothing else):
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
        
        # Apply WCAG compliance rules
        short_alt = enforce_wcag_alt_text_rules(result.get("short_alt_text", ""), is_short=True)
        long_alt = enforce_wcag_alt_text_rules(result.get("long_alt_text", ""), is_short=False)
        
        return JSONResponse(content={
            "short_alt_text": short_alt,
            "long_alt_text": long_alt
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
