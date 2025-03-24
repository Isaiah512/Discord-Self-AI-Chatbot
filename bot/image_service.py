"""
Image generation module for Discord self-bot
"""
import os
import time
import requests
import re
from config.settings import (
    IMAGE_GENERATION_MODEL, 
    IMAGE_GENERATION_GUIDANCE_SCALE, 
    IMAGE_GENERATION_NUM_INFERENCE_STEPS
)

def is_html_response(content):
    """Check if the response content is HTML."""
    try:
        # convert bytes to string
        content_str = content.decode('utf-8', errors='ignore')
        
        # check for common HTML elements
        html_indicators = [
            '<!DOCTYPE html>',
            '<html',
            '<!doctype html>',
            '<head>',
            '<!DOCTYPE',
            '<title>',
            'Content-Type: text/html'
        ]
        
        return any(indicator.lower() in content_str.lower() for indicator in html_indicators)
    except Exception:
        return False

async def generate_image(prompt):
    """Generate an image using Hugging Face Inference API."""
    api_token = os.getenv('HF_API_TOKEN')
    if not api_token:
        return "Hugging Face API token not found. Please set HF_API_TOKEN in .env file."
    
    url = f"https://api-inference.huggingface.co/models/{IMAGE_GENERATION_MODEL}"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "guidance_scale": IMAGE_GENERATION_GUIDANCE_SCALE,
            "num_inference_steps": IMAGE_GENERATION_NUM_INFERENCE_STEPS
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if is_html_response(response.content):
            # extract any error message from the HTML
            try:
                error_match = re.search(r'<p[^>]*>(.*?)</p>', response.content.decode('utf-8'), re.IGNORECASE)
                error_text = error_match.group(1) if error_match else "Unexpected HTML response from API"
            except Exception:
                error_text = "Received HTML response instead of an image"
            
            return f"API Error: {error_text}"
        
        # check response status code
        if response.status_code == 200:
            if not response.content or len(response.content) < 1000:
                return "Received invalid image data"
            
            # Ensure images directory exists
            os.makedirs('generated_images', exist_ok=True)
            
            # Use a timestamp-based filename
            filename = f"generated_images/image_{int(time.time())}.png"
            
            with open(filename, "wb") as f:
                f.write(response.content)
            
            return filename
        elif response.status_code == 401:
            return "Invalid API token. Please check your Hugging Face API token."
        elif response.status_code == 429:
            return "Rate limit exceeded. Please try again later."
        else:
            # Try to extract any error message
            try:
                error_details = response.json()
                return f"Error: {response.status_code} - {error_details}"
            except:
                return f"Error: {response.status_code} - {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    except Exception as e:
        return f"Unexpected error during image generation: {e}"
