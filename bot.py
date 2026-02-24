import asyncio
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQuery_Handler, filters, ContextTypes

# --- UTILS ---
GLITCH_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "Ø", "Σ", "☣️"]

def get_glitch():
    return "".join(random.choices(GLITCH_CHARS + list(string.ascii_uppercase), k=15))

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Creating the Menu Button
    keyboard = [[InlineKeyboardButton("🛑 TERMINATE SESSION", callback_data='start_terminate')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔴 **OFFICER RAKSHAK TERMINAL v4.0**\n"
        "Status: Online | Location: [REDACTED]\n\n"
        "Select an operation from the menu below:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_terminate':
        await query.edit_message_text("📡 **TARGET ACQUISITION**\nEnter the mobile number to intercept:")
        context.user_data['state'] = 'WAITING_FOR_NUM'

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        context.user_data['state'] = 'ATTACKING'
        target = update.message.text
        
        # Start the sequence
        msg = await update.message.reply_text(f"⚡ Establishing link to `{target}`...", parse_mode="Markdown")
        await asyncio.sleep(1)
        
        # Step 1: Fake Progress
        for i in range(1, 4):
            await msg.edit_text(f"🔓 Bypassing Layer {i}/3...\nProgress: [{'█'*i}{'░'*(3-i)}]")
            await asyncio.sleep(1)

        # Step 2: High-Level Glitch
        for _ in range(10):
            await msg.edit_text(f"⚠️ **CRITICAL OVERLOAD**\n`{get_glitch()}`\n`0x{random.randint(1000, 9999)}_FAIL`")
            await asyncio.sleep(0.15)

        # Step 3: Final Slap & Crash
        await msg.edit_text(
            "❌ **KERNEL PANIC: SYSTEM BREACHED**\n"
            "----------------------------------\n"
            "Mee over-confidence valla lakshala mandi bhagyam road meeda padedhi. "
            "Ippudu nenu donga ni kadu kabatti bathikipoyaru.\n\n"
            "🛑 *API Connection Terminated.*",
            parse_mode="Markdown"
        )
        context.user_data['state'] = None

if __name__ == '__main__':
    # REPLACE 'YOUR_TOKEN' with your token from @BotFather
    app = ApplicationBuilder().token("8615286526:AAEX65kXROmTVafC7ttG0LrGOstLIiLTQJ0").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_input))
    
    print("Officer Rakshak is deployed...")
    app.run_polling()
