import feedparser
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# BOT TOKEN
TOKEN = "8488142902:AAGL781OPUQoWAe5WwUiFIR8lS-8vG0JFDg"

# YOUTUBE CHANNEL ID
CHANNEL_ID = "UC8JFmTOgcgqHB1bxKnSlIGQ"

# SOCIAL LINKS
CHANNEL_LINKS = """
🔥 JOIN ALL OUR OFFICIAL CHANNELS 🔥

▶ YouTube:
https://youtube.com/@trsv-editz?si=-KSAODamxjPmgJ97

📸 Instagram:
https://www.instagram.com/trsv.editz?igsh=NHJoaWxyNnNpa2g4

💬 WhatsApp Channel:
https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c

📢 Telegram Channel:
https://t.me/trsveditz

📘 Facebook Page:
https://www.facebook.com/share/1CqE63Lf7S/

📩 Email:
trsvofficial66@gmail.com
"""

# USERS
users = set()

# LAST VIDEO
last_video = None

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_chat.id

    users.add(user_id)

    await update.message.reply_text(
        "🔥 WELCOME TO TRSV EDITZ BOT 🔥\n\n"
        "You will automatically receive all new YouTube uploads 🚀\n\n"
        + CHANNEL_LINKS
    )

# CHECK YOUTUBE
async def check_youtube(app):

    global last_video

    while True:

        try:

            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

            feed = feedparser.parse(rss_url)

            if feed.entries:

                latest = feed.entries[0]

                video_id = latest.yt_videoid
                title = latest.title
                link = latest.link

                if last_video is None:

                    last_video = video_id

                elif last_video != video_id:

                    last_video = video_id

                    message = (
                        f"🔥 NEW VIDEO UPLOADED 🔥\n\n"
                        f"🎬 {title}\n\n"
                        f"▶ WATCH NOW:\n{link}\n\n"
                        + CHANNEL_LINKS
                    )

                    for user_id in users:

                        try:

                            await app.bot.send_message(
                                chat_id=user_id,
                                text=message
                            )

                        except:
                            pass

            await asyncio.sleep(60)

        except Exception as e:

            print(e)

            await asyncio.sleep(60)

# MAIN APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

# BACKGROUND TASK
async def post_init(app):

    asyncio.create_task(check_youtube(app))

app.post_init = post_init

print("✅ TRSV BOT RUNNING...")

app.run_polling()
