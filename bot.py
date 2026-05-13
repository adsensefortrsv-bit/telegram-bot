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
    ContextTypes,
    MessageHandler,
    filters
)

# =========================================
# BOT TOKEN
# =========================================
BOT_TOKEN = "8435083843:AAHlTI3Nk9VV35oHUzJnuZ0b1dJd9P1tkg0"

# =========================================
# ADMIN ID
# =========================================
ADMIN_ID = 8420559244

# =========================================
# TELEGRAM CHANNEL USERNAME
# =========================================
CHANNEL_USERNAME = "@trsveditz"

# =========================================
# YOUTUBE CHANNEL ID
# =========================================
CHANNEL_ID = "UC8JFmTOgcgqHB1bxKnSlIGQ"

# =========================================
# YOUTUBE RSS FEED
# =========================================
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

# =========================================
# WELCOME IMAGE
# =========================================
WELCOME_IMAGE = "https://i.ibb.co/HDf1gWgm/6060052766098395538.jpg"

# =========================================
# SOCIAL LINKS
# =========================================
YOUTUBE_LINK = "https://youtube.com/@trsv-editz"

INSTAGRAM_LINK = "https://instagram.com/trsv.editz"

TELEGRAM_LINK = "https://t.me/trsveditz"

WHATSAPP_LINK = "https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c"

FACEBOOK_LINK = "https://facebook.com/share/1CqE63Lf7S/"

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

🔥 <b>WELCOME TO TRSV EDITZ BOT</b>

🎬 Auto YouTube Upload Alerts
🚀 Instant Video Notifications
📸 Instagram Updates
💬 WhatsApp Channel
⚡ Premium Telegram Experience

━━━━━━━━━━━━━━━━━━

👑 <b>JOIN ALL OFFICIAL PLATFORMS</b>
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
                url=YOUTUBE_LINK
            )
        ],

        [
            InlineKeyboardButton(
                "📸 INSTAGRAM",
                url=INSTAGRAM_LINK
            ),

            InlineKeyboardButton(
                "💬 TELEGRAM",
                url=TELEGRAM_LINK
            )
        ],

        [
            InlineKeyboardButton(
                "🔥 WHATSAPP CHANNEL",
                url=WHATSAPP_LINK
            )
        ],

        [
            InlineKeyboardButton(
                "🌐 FACEBOOK PAGE",
                url=FACEBOOK_LINK
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
# USERS COUNT
# =========================================
async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    total = len(users)

    await update.message.reply_text(
        f"👥 Total Bot Users: {total}"
    )

# =========================================
# BROADCAST MESSAGE
# =========================================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) == 0:

        await update.message.reply_text(
            "❌ Use:\n/broadcast your_message"
        )

        return

    message = " ".join(context.args)

    success = 0

    for user_id in users:

        try:

            await context.bot.send_message(
                chat_id=user_id,
                text=f"📢 BROADCAST MESSAGE\n\n{message}"
            )

            success += 1

        except:
            pass

    await update.message.reply_text(
        f"✅ Broadcast Sent To {success} Users"
    )

# =========================================
# FORWARD USER MESSAGES TO ADMIN
# =========================================
async def forward_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    if update.message.text.startswith("/"):
        return

    user = update.effective_user

    text = update.message.text

    msg = f"""
📩 NEW USER MESSAGE

👤 Name: {user.first_name}
🆔 User ID: {user.id}

💬 Message:
{text}
"""

    try:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=msg
        )

    except Exception as e:
        print(e)

# =========================================
# AUTO REPLY
# =========================================
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = update.message.text.lower()

    if "hello" in text:

        await update.message.reply_text(
            "👋 Hello Welcome To TRSV EDITZ BOT"
        )

    elif "youtube" in text:

        await update.message.reply_text(
            f"🎬 YouTube Channel:\n{YOUTUBE_LINK}"
        )

    elif "instagram" in text:

        await update.message.reply_text(
            f"📸 Instagram:\n{INSTAGRAM_LINK}"
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

            # SEND TO BOT USERS
            for user_id in users:

                try:

                    await context.bot.send_message(
                        chat_id=user_id,
                        text=text,
                        parse_mode="HTML",
                        disable_web_page_preview=False
                    )

                except Exception as e:
                    print(f"Failed to send to {user_id}: {e}")

            # SEND TO TELEGRAM CHANNEL
            try:

                await context.bot.send_message(
                    chat_id=CHANNEL_USERNAME,
                    text=text,
                    parse_mode="HTML",
                    disable_web_page_preview=False
                )

            except Exception as e:
                print(f"Channel Error: {e}")

# =========================================
# BOT SETUP
# =========================================
app = Application.builder().token(BOT_TOKEN).build()

# =========================================
# COMMANDS
# =========================================
app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("users", users_count))

app.add_handler(CommandHandler("broadcast", broadcast))

# =========================================
# MESSAGE HANDLERS
# =========================================
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        forward_messages
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        auto_reply
    )
)

# =========================================
# AUTO CHECK YOUTUBE EVERY 60 SECONDS
# =========================================
job_queue = app.job_queue

job_queue.run_repeating(
    check_youtube,
    interval=60,
    first=10
)

# =========================================
# STARTING BOT
# =========================================
print("🔥 TRSV EDITZ BOT RUNNING 🔥")

app.run_polling()
