from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from modules.welcome import (
    WELCOME_TEXT,
    WELCOME_IMAGE,
    get_welcome_buttons
)

from modules.broadcast import save_user
from modules.analytics import total_users
from modules.auto_reply import AUTO_REPLIES

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN"

ADMINS = [123456789]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    save_user(user_id)

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_welcome_buttons()
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMINS:
        return

    users = total_users()

    await update.message.reply_text(
        f"👥 Total Users: {users}"
    )

async def reply_system(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if text in AUTO_REPLIES:
        await update.message.reply_text(
            AUTO_REPLIES[text]
        )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        reply_system
    )
)

print("🔥 TRSV EDITZ BOT RUNNING")

app.run_polling()
