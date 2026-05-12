from telegram import InlineKeyboardButton, InlineKeyboardMarkup

WELCOME_TEXT = """
🔥 <b>WELCOME TO TRSV EDITZ BOT</b>

🎬 Auto YouTube Alerts
📢 WhatsApp Channel
📸 Instagram Updates
🚀 Premium Telegram Bot

━━━━━━━━━━━━━━━
"""

WELCOME_IMAGE = "https://i.ibb.co/HDf1gWgm/6060052766098395538.jpg"

def get_welcome_buttons():
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
                "💬 WHATSAPP",
                url="https://whatsapp.com/channel/0029VbCcbE9Au3aYo9SUZ61c"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
