from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY is not set in your environment variables.")

genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Only message required in request
class ChatMessage(BaseModel):
    message: str

@app.post("/chatbot")
def chatbot_interaction(chat: ChatMessage):
    """
    Responds to a single user message using Gemini AI.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(chat.message)
        return {
            "success": True,
            "response": response.text.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chatbot interaction: {str(e)}")
