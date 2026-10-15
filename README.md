# AI Telegram Bot & Lead Capture System

An intelligent Telegram bot powered by the Google Gemini API (`gemini-2.0-flash`), built for automated customer engagement, conversational AI support, and real-time lead capture.

---

## ✨ Features

- **Contextual AI Conversations:** Integrates Google Gemini API for fast, human-like responses with conversation history management.
- **Automated Lead Capture:** Detects email addresses and phone numbers during user interactions and stores them automatically in a local **SQLite database** (`leads.db`) and **CSV export** (`leads.csv`).
- **Real-Time Admin Notifications:** Instantly alerts the admin via Telegram whenever a new lead shares contact details.
- **No-Code Prompt Customization:** Easily adjust the bot's persona and instructions via external text files (`system_prompt.txt` and `welcome_message.txt`) without editing Python code.
- **Memory & Rate Limiting:** Implements anti-spam cooldowns and automatic memory management using TTL caching (`cachetools`) to clean up inactive chats.
- **Group Chat Smart Handling:** Filters group messages to respond only when explicitly tagged (`@bot_username`).
- **Production-Ready Docker Support:** Containerized with `Dockerfile` and `docker-compose` for seamless, one-command deployment.

---

## 📁 Repository Structure

```text
Bot-Telegram-IA/
├── bot.py                  # Main application script & event handlers
├── config.py               # Robust configuration & environment variable validation
├── database.py             # SQLite & CSV lead storage + regex contact extractor
├── system_prompt.txt       # System prompt instructions (customizable)
├── welcome_message.txt     # Initial /start message (customizable)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore              # Git exclusion rules
├── Dockerfile              # Docker container build file
├── docker-compose.yml      # Multi-container orchestrator with persistent volumes
└── README.md               # Project documentation
🛠️ Prerequisites
Python 3.10 or higher

A Telegram Bot Token (obtained via @BotFather)

A Google Gemini API Key (obtained via Google AI Studio)

⚙️ Configuration
Copy the configuration template to create your .env file:

Bash
cp .env.example .env
Open .env and fill in your credentials:

Extrait de code
# Required Configurations
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configurations
ADMIN_CHAT_ID=your_telegram_chat_id_for_lead_alerts
COOLDOWN_SECONDS=3
MAX_HISTORY_TURNS=10
MAX_CACHE_SIZE=1000
CACHE_TTL_HOURS=24
🚀 Quick Start
Option 1: Standard Python Execution
Clone the repository:

Bash
git clone [https://github.com/emmanuelvect99/Bot-Telegram-IA.git](https://github.com/emmanuelvect99/Bot-Telegram-IA.git)
cd Bot-Telegram-IA
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Run the bot:

Bash
python bot.py
Option 2: Deployment with Docker (Recommended)
Build and start the container:

Bash
docker-compose up -d --build
Check container status & logs:

Bash
docker-compose logs -f
Stop the container:

Bash
docker-compose down
📊 Lead Data Access
Captured leads are automatically stored locally in two formats:

SQLite Database: leads.db (Table: leads)

CSV File: leads.csv (Includes Timestamp, User ID, Full Name, Username, Email, Phone, and Raw Message)

🛡️ Tech Stack
Language: Python 3.11

Telegram Framework: python-telegram-bot

AI Model: google-genai (Gemini API)

Database: SQLite3

Caching: cachetools

Containerization: Docker & Docker Compose
