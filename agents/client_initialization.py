import os
from dotenv import load_dotenv
from openai import OpenAI
from google import genai

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))