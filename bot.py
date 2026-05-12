from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

# =========================
# BOT TOKEN
# =========================
BOT_TOKEN = "8488142902:AAGL781OPUQoWAe5WwUiFIR8lS-8vG0JFDg"

# =========================
# PHOTO / BANNER
# =========================
WELCOME_IMAGE = "https://i.ibb.co/HDf1gWgm/6060052766098395538.jpg"

# =========================
# WELCOME MESSAGE
# =========================
WELCOME_TEXT = """
╔══❖•ೋ° °ೋ•❖══╗
      💎 𝗧𝗥𝗦𝗩 𝗘𝗗𝗜𝗧𝗭 💎
╚══❖•ೋ° °ೋ•❖══╝

🚀 <b>WELCOME TO TRSV EDITZ BOT</b>

⚡️ Auto YouTube Upload Notifications
🎬 New Videos Instantly
🔥 Stay Connected With Us

━━━━━━━━━━━━━━━━━━

👑 <b>OFFICIAL PLATFORMS</b>

🔥 Enjoy Premium Experience
"""

# =========================
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "🎬 YOUTUBE",
                url="https://youtube.com/@trsv-editz"
            )
        ],

        [
            InlineKeyboardButton(
                "📸 INSTAGRAM",
                url="https://instagram.com/trsv.editz"
            ),

            InlineKeyboardButton(
                "💬 TELEGRAM",
                url="https://t.me/trsveditz"
            )
        ],

        [
            InlineKeyboardButton(
                "🌐 FACEBOOK",
                url="https://facebook.com/"
            )
        ],

        [
            InlineKeyboardButton(
                "🔥 WHATSAPP",
                url="https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c"
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
# BOT START
# =========================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("🔥 BOT RUNNING SUCCESSFULLY 🔥")

app.run_polling()
