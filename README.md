# 🤖 Telegram AI Bot & Lead Capture System

An intelligent Telegram bot powered by the **Google Gemini API**, designed to handle conversational interactions with context memory and automatically extract lead contact information into both an SQLite database and a CSV file.

## 🌟 Key Features

- **AI-Powered Conversations**: Generates smooth, contextual responses using Google Gemini (`gemini-3.8-flash`).
- **Contextual Memory**: Remembers recent conversation history per user session.
- **Automated Lead Capture**: Detects and extracts emails and phone numbers shared in messages.
- **Dual Data Persistence**: Stores captured leads in a local SQLite database (`leads.db`) and exports them to `leads.csv`.
- **Instant Admin Alerts**: Sends real-time notifications to the administrator whenever a new lead is captured.
- **Rate-Limiting Protection**: Built-in configurable cooldown mechanism to prevent spamming.

---

## 🛠️ Prerequisites

- **Python 3.10+**
- A **Telegram Bot Token** (obtained from [@BotFather](https://t.me/BotFather))
- A **Google Gemini API Key** (obtained from [Google AI Studio](https://aistudio.google.com/))

---

## 🚀 Quickstart & Setup (Windows CMD)

### 1. Clone the Repository
```cmd
git clone https://github.com/emmanuelvect99/Bot-Telegram-IA.git
cd Bot-Telegram-IA
```

### 2. Create and Activate Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory by copying the example file:

```cmd
copy .env.example .env
```

Open `.env` in any text editor and fill in your API keys:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configurations
ADMIN_CHAT_ID=your_telegram_chat_id
COOLDOWN_SECONDS=3
MAX_HISTORY_TURNS=10
MAX_CACHE_SIZE=1000
CACHE_TTL_HOURS=24
```

### 5. Run the Bot
```cmd
python bot.py
```

---

## 🐧 Setup for Linux / macOS

```bash
# 1. Clone & Navigate
git clone https://github.com/emmanuelvect99/Bot-Telegram-IA.git
cd Bot-Telegram-IA

# 2. Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 3. Dependencies & Config
pip install -r requirements.txt
cp .env.example .env

# 4. Launch Bot
python bot.py
```

---

## 🐳 Alternative Deployment: Docker

If you prefer running the application inside a Docker container:

```bash
# 1. Set up your .env configuration
cp .env.example .env

# 2. Build and start containers in detached mode
docker-compose up -d --build

# 3. View live logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
Bot-Telegram-IA/
├── bot.py             # Core entry point (Telegram handlers & Gemini interaction)
├── config.py          # Environment variable loading & validation
├── database.py        # SQLite persistence & CSV export logic
├── requirements.txt    # Python dependency specifications
├── .env.example       # Template for environment configuration
├── Dockerfile         # Docker image definition
└── docker-compose.yml # Container orchestration configuration
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
