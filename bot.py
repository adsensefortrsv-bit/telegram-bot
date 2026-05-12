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

BOT_TOKEN = "8488142902:AAGL781OPUQoWAe5WwUiFIR8lS-8vG0JFDg"

WELCOME_IMAGE = "https://i.ibb.co/HDf1gWgm/6060052766098395538.jpg"

YOUTUBE_LINK = "https://youtube.com/@trsv-editz"
INSTAGRAM_LINK = "https://instagram.com/trsv.editz"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c"

ADMIN_ID = 8420559244

# ================= USERS =================

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

# ================= START =================

WELCOME_TEXT = """
🔥 <b>WELCOME TO TRSV EDITZ BOT</b>

🎬 Auto YouTube Alerts
📢 WhatsApp Channel
📸 Instagram Updates
🚀 Premium Telegram Bot

━━━━━━━━━━━━━━━━━━
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

# ================= USERS COUNT =================

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    total = len(get_users())

    await update.message.reply_text(
        f"👥 Total Users: {total}"
    )

# ================= BROADCAST =================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/broadcast your message"
        )
        return

    msg = " ".join(context.args)

    users = get_users()

    success = 0

    for user_id in users:

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=msg
            )

            success += 1

        except:
            pass

    await update.message.reply_text(
        f"✅ Sent to {success} users"
    )

# ================= AUTO REPLY =================

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if "hello" in text:
        await update.message.reply_text(
            "👋 Hello from TRSV EDITZ BOT"
        )

    elif "youtube" in text:
        await update.message.reply_text(
            YOUTUBE_LINK
        )

    elif "instagram" in text:
        await update.message.reply_text(
            INSTAGRAM_LINK
        )

# ================= MAIN =================

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

print("🔥 TRSV EDITZ BOT RUNNING")

app.run_polling()
