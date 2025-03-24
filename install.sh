#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' 

# Detect Linux distribution
install_python() {
    echo -e "${YELLOW}Installing Python 3.9...${NC}"
    
    # Ubuntu/Debian
    if [ -x "$(command -v apt-get)" ]; then
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt-get update
        sudo apt-get install -y python3.9 python3.9-venv python3.9-dev python3-pip git
    
    # Fedora
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y python39 python39-devel python39-pip git
    
    # CentOS/RHEL
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install -y https://repo.ius.io/ius-release-el7.rpm
        sudo yum install -y python39 python39-devel python39-pip git
    
    # Arch Linux
    elif [ -x "$(command -v pacman)" ]; then
        sudo pacman -S --noconfirm python-pip git
    
    else
        echo -e "${RED}Unsupported Linux distribution. Please install Python 3.9 manually.${NC}"
        exit 1
    fi
}

# Check if Python is installed
if ! command -v python3.9 &> /dev/null; then
    install_python
fi

# Create installation directory
mkdir -p ~/discord-ai-chatbot
cd ~/discord-ai-chatbot

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3.9 -m venv venv

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${GREEN}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${GREEN}Installing project dependencies...${NC}"
pip install discord.py python-dotenv langchain langchain-google-genai google-generativeai Pillow aiohttp requests

# Clone the project repository
echo -e "${GREEN}Downloading project files...${NC}"
git clone https://github.com/isaiah76/Discord-Self-AI-Chatbot.git .

# Create .env file template
echo -e "${GREEN}Creating .env file template...${NC}"
cat > .env << EOL
DISCORD_TOKEN=your_discord_token_here
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_TOKEN=your_huggingface_api_token_here
EOL

echo -e "${GREEN}===================================================
Installation Complete!
1. Open .env and fill in your tokens
2. Activate venv with: source venv/bin/activate
3. Run the bot with: python main.py
===================================================${NC}"
