import asyncio
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- CONFIGURATION ---
# Your provided reference token
TOKEN = "8615286526:AAEX65kXROmTVafC7ttG0LrGOstLIiLTQJ0"

# --- UTILS (Visual Effects) ---
GLITCH_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "Ø", "Σ", "☣️", "X", "0", "1"]

def get_glitch_text(length=20):
    return "".join(random.choices(GLITCH_CHARS + list(string.ascii_uppercase), k=length))

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the initial menu with interactive buttons.
    """
    keyboard = [
        [InlineKeyboardButton("🛑 TERMINATE SESSION", callback_data='start_attack')],
        [InlineKeyboardButton("🔍 SYSTEM SCAN", callback_data='scan')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔴 **OFFICER RAKSHAK: CYBER-WARFARE DIVISION**\n"
        "------------------------------------------\n"
        "STATUS: AUTHORIZED 🛡️\n"
        "MISSION: EXPOSE NETWORK VULNERABILITIES\n\n"
        "Select an operation to begin:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles button clicks from the inline menu.
    """
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_attack':
        await query.edit_message_text("📡 **TARGET ACQUISITION**\nEnter the mobile number to intercept:")
        context.user_data['state'] = 'WAITING_FOR_NUM'
    
    elif query.data == 'scan':
        await query.edit_message_text("🔎 Scanning local network... No threats found. Ready for `/terminate`.")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processes the phone number and runs the glitch sequence.
    """
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        context.user_data['state'] = 'ATTACKING'
        target = update.message.text
        
        # Initializing message
        msg = await update.message.reply_text(f"⚡ Establishing link to `{target}`...", parse_mode="Markdown")
        await asyncio.sleep(1.2)
        
        # Step 1: Simulated Progress
        for i in range(1, 4):
            progress = "█" * i + "░" * (3 - i)
            await msg.edit_text(f"🔓 **Bypassing Layer {i}/3...**\n`[{progress}]`", parse_mode="Markdown")
            await asyncio.sleep(1)

        # Step 2: High-Level Glitch Animation
        for _ in range(12):
            glitch = get_glitch_text(25)
            await msg.edit_text(
                f"⚠️ **CRITICAL BUFFER OVERFLOW** ⚠️\n"
                f"`{glitch}`\n"
                f"`ERR_0x{random.randint(1000, 9999)}_RETRY_FAILED`",
                parse_mode="Markdown"
            )
            await asyncio.sleep(0.15)

        # Step 3: Final Reality Check & Crash
        final_text = (
            "❌ **KERNEL PANIC: SYSTEM BREACHED**\n"
            "----------------------------------\n"
            "Mee over-confidence valla lakshala mandi bhagyam road meeda padedhi. "
            "Ippudu nenu donga ni kadu kabatti bathikipoyaru. 🇮🇳\n\n"
            "🛑 **API Connection Terminated.**"
        )
        await msg.edit_text(final_text, parse_mode="Markdown")
        context.user_data['state'] = None

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Registering handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("terminate", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_input))
    
    print("Officer Rakshak Terminal is running...")
    application.run_polling()
