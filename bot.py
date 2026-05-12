import feedparser
import logging

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

# =========================================
# BOT TOKEN
# =========================================
BOT_TOKEN = "8488142902:AAGL781OPUQoWAe5WwUiFIR8lS-8vG0JFDg"

# =========================================
# YOUTUBE CHANNEL ID
# =========================================
CHANNEL_ID = "UC8JFmTOgcgqHB1bxKnSlIGQ"

# =========================================
# YOUTUBE RSS FEED
# =========================================
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

# =========================================
# PHOTO / BANNER
# =========================================
WELCOME_IMAGE = "https://i.ibb.co/HDf1gWgm/6060052766098395538.jpg"

# =========================================
# LOGGING
# =========================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================================
# SAVE USERS
# =========================================
users = set()

# =========================================
# WELCOME MESSAGE
# =========================================
WELCOME_TEXT = """
╔══❖•ೋ° °ೋ•❖══╗
       💎 𝗧𝗥𝗦𝗩 𝗘𝗗𝗜𝗧𝗭 💎
╚══❖•ೋ° °ೋ•❖══╝

🚀 <b>WELCOME TO TRSV EDITZ BOT</b>

⚡️ Auto YouTube Upload Notifications
🎬 Get New Videos Instantly
🔥 Stay Connected With Our Community

━━━━━━━━━━━━━━━━━━

👑 <b>JOIN ALL OFFICIAL PLATFORMS</b>

💜 Enjoy Premium Style Experience
"""

# =========================================
# START COMMAND
# =========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_chat.id

    users.add(user_id)

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
                "🔥 WHATSAPP CHANNEL",
                url="https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c"
            )
        ],

        [
            InlineKeyboardButton(
                "🌐 FACEBOOK PAGE",
                url="https://facebook.com/share/1CqE63Lf7S/"
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

# =========================================
# YOUTUBE CHECKER
# =========================================
latest_video = ""

async def check_youtube(context: ContextTypes.DEFAULT_TYPE):

    global latest_video

    feed = feedparser.parse(RSS_URL)

    if len(feed.entries) > 0:

        newest_video = feed.entries[0]

        video_title = newest_video.title
        video_link = newest_video.link

        if video_link != latest_video:

            latest_video = video_link

            text = f"""
🔥 <b>NEW VIDEO UPLOADED</b>

🎬 <b>{video_title}</b>

🚀 WATCH NOW:
{video_link}
"""

            for user_id in users:

                try:

                    await context.bot.send_message(
                        chat_id=user_id,
                        text=text,
                        parse_mode="HTML",
                        disable_web_page_preview=False
                    )

                except Exception as e:
                    print(f"Failed to send message to {user_id}: {e}")

# =========================================
# BOT START
# =========================================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

# =========================================
# AUTO CHECK EVERY 60 SECONDS
# =========================================
job_queue = app.job_queue

job_queue.run_repeating(
    check_youtube,
    interval=60,
    first=10
)

print("🔥 TRSV EDITZ BOT RUNNING 🔥")

app.run_polling()
