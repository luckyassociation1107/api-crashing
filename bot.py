import asyncio
import os
import random
import string
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- CONFIG ---
TOKEN = "8615286526:AAEX65kXROmTVafC7ttG0LrGOstLIiLTQJ0"
PORT = int(os.environ.get("PORT", 8080)) # Render provides the port automatically

# --- WEB SERVER (For UptimeRobot & Render) ---
async def handle_health_check(request):
    return web.Response(text="Officer Rakshak is Active 🛡️")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Web server started on port {PORT}")

# --- BOT LOGIC (Shortened for brevity) ---
# ... (Include your existing start, button_callback, and handle_input functions here) ...

async def main():
    # Start the web server in the background
    await start_web_server()

    # Initialize the Telegram Bot
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add your handlers here as before
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_input))
    
    async with application:
        await application.initialize()
        await application.start_polling()
        # Keep the loop running
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
