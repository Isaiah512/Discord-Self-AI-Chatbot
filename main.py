#!/usr/bin/env python3
""" Main entry point """
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

required_env_vars = ['DISCORD_TOKEN', 'GEMINI_API_KEY', 'HF_API_TOKEN']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

from bot.client import client

if __name__ == "__main__":
    client.run(os.getenv('DISCORD_TOKEN'))
