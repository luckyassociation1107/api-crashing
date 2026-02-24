import asyncio
import os
import random
import string
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- CONFIG ---
TOKEN = "8615286526:AAEX65kXROmTVafC7ttG0LrGOstLIiLTQJ0"
PORT = int(os.environ.get("PORT", 10000)) 🛡️

# --- UTILS ---
GLITCH_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "Ø", "Σ", "☣️", "X", "0", "1"]

def get_glitch_text(length=20):
    return "".join(random.choices(GLITCH_CHARS + list(string.ascii_uppercase), k=length))

# --- WEB SERVER (For UptimeRobot) ---
async def handle_health_check(request):
    return web.Response(text="Officer Rakshak is Active 🛡️")

async def start_web_server():
    server = web.Application()
    server.router.add_get("/", handle_health_check)
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Web server started on port {PORT}")

# --- BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛑 TERMINATE SESSION", callback_data='start_attack')],
        [InlineKeyboardButton("🔍 SYSTEM SCAN", callback_data='scan')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔴 **WARFARE DIVISION**\n"
        "------------------------------------------\n"
        "STATUS: AUTHORIZED 🛡️\n"
        "Select an operation to begin:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'start_attack':
        await query.edit_message_text("📡 **TARGET ACQUISITION**\nEnter the mobile number to intercept:")
        context.user_data['state'] = 'WAITING_FOR_NUM'
    elif query.data == 'scan':
        await query.edit_message_text("🔎 Scanning local network... No threats found.")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        context.user_data['state'] = 'ATTACKING'
        target = update.message.text
        msg = await update.message.reply_text(f"⚡ Establishing link to `{target}`...", parse_mode="Markdown")
        await asyncio.sleep(1)
        
        # Simulated Progress
        for i in range(1, 4):
            await msg.edit_text(f"🔓 **Bypassing Layer {i}/3...**")
            await asyncio.sleep(1)

        # High-Level Glitch
        for _ in range(10):
            await msg.edit_text(f"⚠️ **OVERLOAD**\n`{get_glitch_text(25)}`")
            await asyncio.sleep(0.15)

        await msg.edit_text("❌ **KERNEL PANIC: SYSTEM BREACHED**\n🛑 *API Connection Terminated.*", parse_mode="Markdown")
        context.user_data['state'] = None

# --- MAIN LOOP ---
async def main():
    await start_web_server() 🌐
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_input))
    
    async with application:
        await application.initialize()
        await application.start_polling()
        print("Bot is polling...")
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
