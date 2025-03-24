"""
Configuration settings for the Discord bot
"""
import os
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold
from config.personality import PERSONALITY
from config.owner import OWNER_RECOGNITION

# System prompt for the AI
SYSTEM_PROMPT = f"""
You are a helpful and knowledgeable AI assistant.
Your personality traits:
- You provide information concisely
- You explain complex topics in simple terms
- You respond directly without unnecessary disclaimers
Important: Keep your responses brief, especially in casual conversations. Use 1-3 sentences when possible.
Only provide detailed explanations when specifically asked for in-depth information.
When sharing code, always format it using triple backticks with the appropriate language identifier. For example:
```py
# This is Python code
def hello_world():
    print("Hello, world!")
```
{PERSONALITY}
{OWNER_RECOGNITION}
"""

# Gemini Model settings
GEMINI_MODEL_TEXT = "gemini-2.0-flash"
GEMINI_MODEL_VISION = "gemini-2.0-flash"
GEMINI_TEMPERATURE = 0.5
GEMINI_MAX_OUTPUT_TOKENS = 2048

# Safety settings for the Gemini model
GEMINI_SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

# Image Generation settings
IMAGE_GENERATION_MODEL = "stabilityai/stable-diffusion-2"
IMAGE_GENERATION_GUIDANCE_SCALE = 7.5  
IMAGE_GENERATION_NUM_INFERENCE_STEPS = 70  

# Discord bot settings
MAX_MESSAGE_LENGTH = 2000
CHUNK_SIZE = 1900
MESSAGE_CHUNK_SUFFIX = " (continued...)"

# Conversation memory settings
MAX_USER_MESSAGES = 100
MAX_CHANNEL_MESSAGES = 50
MAX_CONTEXT_MESSAGES = 10
