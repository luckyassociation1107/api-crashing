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

# --- GLITCH ENGINE ASSETS ---
GLITCH_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "Ø", "Σ", "▒", "▓", "░", "☣️", "☢️", "⚡", "Δ", "Ω"]

def get_glitch_line(length=25):
    return "".join(random.choices(GLITCH_CHARS + list(string.ascii_uppercase), k=length))

# --- WEB SERVER (For Render Health Check) ---
async def handle_health_check(request):
    return web.Response(text="Terminal Active 🛡️")

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
    welcome_text = (
        "<b>[RAKSHAK TERMINAL v5.0]</b>\n"
        "<code>------------------------</code>\n"
        "<code>STATUS: SYSTEM_READY</code>\n"
        "<code>ENCRYPTION: AES-256_ACTIVE</code>\n"
        "<code>------------------------</code>\n"
        "<i>Select Operation...</i>"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="HTML")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_attack':
        await query.edit_message_text(
            "📡 <b>TARGET_ACQUISITION</b>\n<code>------------------------</code>\n<code>ENTER TARGET MOBILE NUMBER:</code>", 
            parse_mode="HTML"
        )
        context.user_data['state'] = 'WAITING_FOR_NUM'
    elif query.data == 'terminate':
        await query.edit_message_text("<code>TERMINATING... SESSION_CLOSED.</code>", parse_mode="HTML")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        num = update.message.text
        context.user_data['state'] = None
        
        # --- 1. INITIALIZING ---
        msg = await update.message.reply_text("<code>[SYSTEM] SEARCHING_FOR_UPLINK...</code>", parse_mode="HTML")
        await asyncio.sleep(1)

        # --- 2. HIGH-LEVEL PROGRESS BAR ---
        stages = ["FIREWALL_BYPASS", "PACKET_INJECTION", "DATA_MINING", "OVERRIDING_LOGS"]
        for i, stage in enumerate(stages):
            for p in range(0, 26, 5): # Each stage sub-progress
                progress = (i * 25) + p
                filled = "█" * (progress // 10)
                empty = "░" * (10 - (progress // 10))
                
                ui = (
                    f"<b>BREACH_IN_PROGRESS</b>\n"
                    f"<code>------------------------</code>\n"
                    f"<code>TARGET: {num}</code>\n"
                    f"<code>STAGE:  {stage}</code>\n"
                    f"<code>PROGRESS: [{filled}{empty}] {progress}%</code>\n"
                    f"<code>------------------------</code>"
                )
                await msg.edit_text(ui, parse_mode="HTML")
                await asyncio.sleep(0.2)

        # --- 3. RAPID FRAME FLICKER (THE GLITCH) ---
        glitch_frames = ["CRITICAL_OVERLOAD", "µ§¥_CORRUPTION", "X000492_FATAL", "!!_STUCK_!!", "SIGNAL_LOST"]
        for _ in range(15):
            frame = random.choice(glitch_frames)
            # Add random noise to frame
            noisy = "".join(random.choice(GLITCH_CHARS) if random.random() > 0.4 else c for c in frame)
            flicker_ui = (
                f"<code>{get_glitch_line(20)}</code>\n"
                f"<code>{noisy}</code>\n"
                f"<code>{get_glitch_line(20)}</code>"
            )
            try:
                await msg.edit_text(flicker_ui, parse_mode="HTML")
                await asyncio.sleep(0.08) # Rapid refresh for flicker
            except: pass

        # --- 4. FINAL SUCCESS ---
        final_ui = (
            "✅ <b>BREACH_SUCCESSFUL</b>\n"
            "<code>------------------------</code>\n"
            f"<code>TARGET: {num}</code>\n"
            "<code>STATUS: DISCONNECTED</code>\n"
            "<code>RESULT: DATA_MIRRORED</code>\n"
            "<code>------------------------</code>"
        )
        await msg.edit_text(final_ui, parse_mode="HTML")

# --- MAIN ENGINE ---
async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_input))
    
    await application.initialize()
    await application.start()
    
    print("RAKSHAK_TERMINAL_ONLINE 🚀")
    
    # Run Web Server and Bot Polling together
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
