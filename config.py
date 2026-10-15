import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("TelegramBotIA")

def parse_int_env(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None or val.strip() == "":
        return default
    try:
        return int(val)
    except ValueError:
        logger.error(f"❌ La variable d'environnement '{key}' doit être un nombre entier valide (valeur reçue: '{val}').")
        sys.exit(1)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    logger.error("❌ 'TELEGRAM_BOT_TOKEN' est manquant dans le fichier .env.")
    sys.exit(1)

if not GEMINI_API_KEY:
    logger.error("❌ 'GEMINI_API_KEY' est manquant dans le fichier .env.")
    sys.exit(1)

COOLDOWN_SECONDS = parse_int_env("COOLDOWN_SECONDS", 3)
MAX_HISTORY_TURNS = parse_int_env("MAX_HISTORY_TURNS", 10)
MAX_CACHE_SIZE = parse_int_env("MAX_CACHE_SIZE", 1000)
CACHE_TTL_HOURS = parse_int_env("CACHE_TTL_HOURS", 24)
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "").strip()

def load_text_file(filepath: str, default_text: str) -> str:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    return default_text

SYSTEM_PROMPT = load_text_file("system_prompt.txt", "Vous êtes un assistant virtuel professionnel.")
WELCOME_MESSAGE = load_text_file("welcome_message.txt", "Bonjour ! Bienvenue. Comment puis-je vous aider aujourd'hui ?")
