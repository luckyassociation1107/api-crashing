import asyncio
import os
import random
import string
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- CONFIG ---
TOKEN = "8615286526:AAEX65kXROmTVafC7ttG0LrGOstLIiLTQJ0"
PORT = int(os.environ.get("PORT", 10000))

# --- GLITCH ENGINE ---
GLITCH_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "Ø", "Σ", "▒", "▓", "░", "☣️", "☢️", "⚡"]

def get_glitch_text(length=20):
    return "".join(random.choices(GLITCH_CHARS + list(string.ascii_uppercase), k=length))

async def glitch_animation(message, original_text, frames=5):
    """Text ni glitch chestu animate chestundi"""
    for _ in range(frames):
        glitched = "".join(random.choice(GLITCH_CHARS) if random.random() > 0.5 else c for c in original_text)
        try:
            await message.edit_text(f"<code>{glitched}</code>", parse_mode="HTML")
            await asyncio.sleep(0.2)
        except: pass
    await message.edit_text(f"<code>{original_text}</code>", parse_mode="HTML")

# --- WEB SERVER ---
async def handle_health_check(request):
    return web.Response(text="Officer Rakshak is Online 🛡️")

async def start_web_server():
    server = web.Application()
    server.router.add_get("/", handle_health_check)
    runner = web.AppRunner(server)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()

# --- BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ INITIALIZE BREACH", callback_data='start_attack')],
        [InlineKeyboardButton("🛑 TERMINATE SESSION", callback_data='terminate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>[RAKSHAK TERMINAL v4.0]</b>\n<code>SYSTEM: READY_TO_INFILTRATE</code>",
        reply_markup=reply_markup, parse_mode="HTML"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_attack':
        await query.edit_message_text("📡 <b>TARGET_ACQUISITION</b>\n<code>Enter target mobile number:</code>", parse_mode="HTML")
        context.user_data['state'] = 'WAITING_FOR_NUM'
    elif query.data == 'terminate':
        await query.edit_message_text("<code>TERMINATING... CONNECTION_LOST</code>")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        num = update.message.text
        msg = await update.message.reply_text("<code>[ ] 0% Connecting...</code>", parse_mode="HTML")
        
        # --- PROGRESS BAR ANIMATION ---
        for i in range(0, 101, 20):
            bar = "█" * (i // 10) + "░" * (10 - (i // 10))
            await msg.edit_text(f"<code>[{bar}] {i}% Injecting_Payload...</code>", parse_mode="HTML")
            await asyncio.sleep(0.5)
        
        # --- HIGH LEVEL GLITCH ATTACK ---
        await asyncio.sleep(0.5)
        for _ in range(8):
            crash_text = f"CRITICAL_ERROR: {get_glitch_text(15)}\n{get_glitch_text(30)}"
            await msg.edit_text(f"<code>{crash_text}</code>", parse_mode="HTML")
            await asyncio.sleep(0.1)
        
        final_msg = f"✅ BREACH_SUCCESSFUL\nTARGET: {num}\nSTATUS: DISCONNECTED"
        await msg.edit_text(f"<code>{final_msg}</code>", parse_mode="HTML")
        context.user_data['state'] = None

# --- MAIN ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_input))
    
    await app.initialize()
    await app.start()
    
    print("RAKSHAK DEPLOYED 🚀")
    await asyncio.gather(start_web_server(), app.updater.start_polling(), asyncio.Event().wait())

if __name__ == '__main__':
    asyncio.run(main())
