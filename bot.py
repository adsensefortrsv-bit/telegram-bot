from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import json
import os

# =========================
# BOT SETTINGS
# =========================

BOT_TOKEN = "8488142902:AAGL781OPUQoWAe5WwUiFIR8lS-8vG0JFDg"

ADMIN_ID = 8420559244

WELCOME_IMAGE = "https://i.ibb.co/HDf1gWgm/6060052766098395538.jpg"

YOUTUBE_LINK = "https://youtube.com/@trsv-editz"
INSTAGRAM_LINK = "https://instagram.com/trsv.editz"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c"

# =========================
# USERS SYSTEM
# =========================

USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

def get_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_user(user_id):

    users = get_users()

    if user_id not in users:

        users.append(user_id)

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# =========================
# START COMMAND
# =========================

WELCOME_TEXT = """
🔥 <b>WELCOME TO TRSV EDITZ BOT</b>

🎬 Auto YouTube Alerts
📢 WhatsApp Channel
📸 Instagram Updates
🚀 Premium Telegram Bot

━━━━━━━━━━━━━━━━━━

💎 Enjoy Premium Features
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    save_user(user_id)

    keyboard = [

        [
            InlineKeyboardButton(
                "🎬 YOUTUBE",
                url=YOUTUBE_LINK
            )
        ],

        [
            InlineKeyboardButton(
                "📸 INSTAGRAM",
                url=INSTAGRAM_LINK
            ),

            InlineKeyboardButton(
                "💬 WHATSAPP",
                url=WHATSAPP_LINK
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# =========================
# USERS COMMAND
# =========================

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    total = len(get_users())

    await update.message.reply_text(
        f"👥 Total Users: {total}"
    )

# =========================
# BROADCAST COMMAND
# =========================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) == 0:

        await update.message.reply_text(
            "❌ Usage:\n/broadcast your message"
        )

        return

    message = " ".join(context.args)

    users = get_users()

    success = 0
    failed = 0

    for user_id in users:

        try:

            await context.bot.send_message(
                chat_id=user_id,
                text=message
            )

            success += 1

        except:

            failed += 1

    await update.message.reply_text(
        f"✅ Broadcast Complete\n\n📤 Sent: {success}\n❌ Failed: {failed}"
    )

# =========================
# AUTO REPLY SYSTEM
# =========================

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if "hello" in text:

        await update.message.reply_text(
            "👋 Hello From TRSV EDITZ BOT"
        )

    elif "youtube" in text:

        await update.message.reply_text(
            f"🎬 YouTube:\n{YOUTUBE_LINK}"
        )

    elif "instagram" in text:

        await update.message.reply_text(
            f"📸 Instagram:\n{INSTAGRAM_LINK}"
        )

    elif "whatsapp" in text:

        await update.message.reply_text(
            f"💬 WhatsApp:\n{WHATSAPP_LINK}"
        )

# =========================
# MAIN SYSTEM
# =========================

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(CommandHandler("broadcast", broadcast))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        auto_reply
    )
)

print("🔥 TRSV EDITZ BOT STARTED SUCCESSFULLY")

app.run_polling()
