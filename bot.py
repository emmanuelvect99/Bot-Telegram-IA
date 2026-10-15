import time
import asyncio
from cachetools import TTLCache
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import config
import database

conversation_history = TTLCache(
    maxsize=config.MAX_CACHE_SIZE,
    ttl=config.CACHE_TTL_HOURS * 3600
)
last_message_time = {}

gemini_client = genai.Client(api_key=config.GEMINI_API_KEY)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(config.WELCOME_MESSAGE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user = update.effective_user
    user_text = update.message.text.strip()

    if update.effective_chat.type in ["group", "supergroup"]:
        bot_username = context.bot.username
        if f"@{bot_username}" not in user_text:
            return
        user_text = user_text.replace(f"@{bot_username}", "").strip()

    now = time.time()
    if chat_id in last_message_time and (now - last_message_time[chat_id]) < config.COOLDOWN_SECONDS:
        await update.message.reply_text("⏳ Merci de patienter quelques secondes entre chaque message.")
        return
    last_message_time[chat_id] = now

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    lead_info = database.extract_and_save_lead_info(
        user_id=user.id,
        username=user.username or "Anonyme",
        full_name=user.full_name or "Inconnu",
        message_text=user_text
    )

    if lead_info and config.ADMIN_CHAT_ID:
        try:
            admin_msg = (
                f"🚨 **Nouveau Lead Capturé !**\n"
                f"👤 Nom: {user.full_name}\n"
                f"💬 Username: @{user.username or 'N/A'}\n"
                f"📧 Email: {lead_info.get('email', 'N/A')}\n"
                f"📞 Tél: {lead_info.get('phone', 'N/A')}\n"
                f"📝 Message: {user_text}"
            )
            await context.bot.send_message(chat_id=config.ADMIN_CHAT_ID, text=admin_msg)
        except Exception as e:
            config.logger.error(f"Erreur d'envoi de notification admin: {e}")

    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    history = conversation_history[chat_id]
    history.append({"role": "user", "parts": [{"text": user_text}]})

    if len(history) > config.MAX_HISTORY_TURNS * 2:
        history = history[-(config.MAX_HISTORY_TURNS * 2):]
        conversation_history[chat_id] = history

    contents = [
        {"role": "user", "parts": [{"text": f"Instruction système : {config.SYSTEM_PROMPT}"}]},
        *history
    ]

    try:
        response = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model="gemini-2.0-flash",
            contents=contents
        )
        bot_response = response.text if response and response.text else "Désolé, je n'ai pas pu générer de réponse."
    except Exception as e:
        config.logger.error(f"Erreur Gemini API: {e}")
        bot_response = "Désolé, une erreur technique est survenue lors de la génération de la réponse."

    history.append({"role": "model", "parts": [{"text": bot_response}]})

    for i in range(0, len(bot_response), 4000):
        await update.message.reply_text(bot_response[i:i + 4000])

def main():
    database.init_db()
    config.logger.info("🤖 Démarrage du Bot Telegram IA...")

    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
