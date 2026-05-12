import os
import json
import logging
import feedparser

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

# ==================================================
# BOT TOKEN
# ==================================================
BOT_TOKEN = "8488142902:AAGL781OPUQoWAe5WwUiFIR8lS-8vG0JFDg"

# ==================================================
# OWNER ID
# ==================================================
OWNER_ID = 8420559244

# ==================================================
# YOUTUBE CHANNEL ID
# ==================================================
CHANNEL_ID = "UC8JFmTOgcgqHB1bxKnSlIGQ"

# ==================================================
# RSS FEED
# ==================================================
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

# ==================================================
# FORCE SUB CHANNEL
# ==================================================
FORCE_SUB_CHANNEL = "trsveditz"

# ==================================================
# WELCOME IMAGE
# ==================================================
WELCOME_IMAGE = "https://i.ibb.co/HDf1gWgm/6060052766098395538.jpg"

# ==================================================
# DATABASE FILE
# ==================================================
USERS_FILE = "users.json"

# ==================================================
# LOGGING
# ==================================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==================================================
# LOAD USERS
# ==================================================
if os.path.exists(USERS_FILE):

    with open(USERS_FILE, "r") as f:
        users = set(json.load(f))

else:
    users = set()

# ==================================================
# SAVE USERS
# ==================================================
def save_users():

    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

# ==================================================
# CHECK SUBSCRIBE
# ==================================================
async def is_subscribed(user_id, bot):

    try:

        member = await bot.get_chat_member(
            chat_id=f"@{FORCE_SUB_CHANNEL}",
            user_id=user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:
        return False

# ==================================================
# START COMMAND
# ==================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id

    # FORCE SUB CHECK
    subscribed = await is_subscribed(user_id, context.bot)

    if not subscribed:

        join_button = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📢 JOIN CHANNEL",
                    url=f"https://t.me/{FORCE_SUB_CHANNEL}"
                )
            ]

        ])

        await update.message.reply_text(
            "🚫 Please Join Our Telegram Channel First",
            reply_markup=join_button
        )

        return

    # SAVE USER
    users.add(user_id)
    save_users()

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
                "🔥 WHATSAPP",
                url="https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c"
            )
        ],

        [
            InlineKeyboardButton(
                "🌐 FACEBOOK",
                url="https://facebook.com/share/1CqE63Lf7S/"
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = f"""
╔══❖•ೋ° °ೋ•❖══╗
      💎 𝗧𝗥𝗦𝗩 𝗘𝗗𝗜𝗧𝗭 💎
╚══❖•ೋ° °ೋ•❖══╝

👋 Welcome {user.first_name}

🚀 Auto YouTube Notifications
🎬 Instant Video Alerts
🔥 Premium Community Access

━━━━━━━━━━━━━━━━━━

✅ Bot Status: ONLINE
👥 Total Users: {len(users)}

💜 Enjoy Premium Experience
"""

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=caption,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ==================================================
# USERS COMMAND
# ==================================================
async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    await update.message.reply_text(
        f"👥 Total Users: {len(users)}"
    )

# ==================================================
# BROADCAST COMMAND
# ==================================================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/broadcast your message"
        )
        return

    message = " ".join(context.args)

    success = 0

    for user_id in users:

        try:

            await context.bot.send_message(
                chat_id=user_id,
                text=f"📢 BROADCAST\n\n{message}"
            )

            success += 1

        except:
            pass

    await update.message.reply_text(
        f"✅ Sent to {success} users"
    )

# ==================================================
# USER MESSAGE FORWARD
# ==================================================
async def forward_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    text = update.message.text

    msg = f"""
📩 NEW MESSAGE

👤 Name: {user.first_name}

🆔 User ID: {user.id}

💬 Message:
{text}
"""

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=msg
    )

# ==================================================
# YOUTUBE CHECKER
# ==================================================
latest_video = ""

async def check_youtube(context: ContextTypes.DEFAULT_TYPE):

    global latest_video

    feed = feedparser.parse(RSS_URL)

    if len(feed.entries) == 0:
        return

    newest = feed.entries[0]

    title = newest.title
    link = newest.link

    if link == latest_video:
        return

    latest_video = link

    message = f"""
🔥 NEW YOUTUBE VIDEO

🎬 {title}

🚀 WATCH NOW:
{link}
"""

    for user_id in users:

        try:

            await context.bot.send_message(
                chat_id=user_id,
                text=message
            )

        except:
            pass

# ==================================================
# BOT SETUP
# ==================================================
app = Application.builder().token(BOT_TOKEN).build()

# COMMANDS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users_command))
app.add_handler(CommandHandler("broadcast", broadcast))

# USER MESSAGES
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        forward_messages
    )
)

# ==================================================
# AUTO CHECK YOUTUBE
# ==================================================
job_queue = app.job_queue

job_queue.run_repeating(
    check_youtube,
    interval=60,
    first=10
)

print("🔥 TRSV EDITZ BOT RUNNING 🔥")

# ==================================================
# START BOT
# ==================================================
app.run_polling()
