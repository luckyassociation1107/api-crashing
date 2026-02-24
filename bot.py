import asyncio
import os
import random
import string
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- CONFIG ---
# Mee Telegram Bot Token ikkada undali
TOKEN = "8615286526:AAEX65kXROmTVafC7ttG0LrGOstLIiLTQJ0"
# Render provide chese PORT ni use chestunnam
PORT = int(os.environ.get("PORT", 10000)) 

# --- UTILS ---
GLITCH_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "Ø", "Σ", "☣️"]

def get_glitch_text(length=20):
    return "".join(random.choices(GLITCH_CHARS + list(string.ascii_uppercase), k=length))

# --- WEB SERVER (Health Check for Render/UptimeRobot) ---
async def handle_health_check(request):
    return web.Response(text="Officer Rakshak is Active 🛡️")

async def start_web_server():
    server = web.Application()
    server.router.add_get("/", handle_health_check)
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Web server started on port {PORT} 🌐")

# --- BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛑 TERMINATE SESSION", callback_data='start_attack')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔴 **RAKSHAK TERMINAL**\n------------------\nSelect operation:", 
        reply_markup=reply_markup, 
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'start_attack':
        await query.edit_message_text("📡 **TARGET ACQUISITION**\nEnter target mobile number:")
        context.user_data['state'] = 'WAITING_FOR_NUM'

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        msg = await update.message.reply_text("⚡ Initializing breach...")
        await asyncio.sleep(1)
        await msg.edit_text(f"⚠️ **SYSTEM CRASH**\n`{get_glitch_text(25)}`")
        context.user_data['state'] = None

# --- MAIN ENGINE ---
async def main():
    # 1. Application setup
    application = ApplicationBuilder().token(TOKEN).build()
    
    # 2. Handlers registration
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_input))
    
    # 3. Bot initialization
    await application.initialize()
    await application.start()
    
    print("Starting Web Server and Bot Polling... 🚀")

    # 4. Web server mariyu Bot polling renditini parallel ga run chestunnam
    # Deeni valla Render health check fail avvadu
    await asyncio.gather(
        start_web_server(),
        application.updater.start_polling(),
        asyncio.Event().wait()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
