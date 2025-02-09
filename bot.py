import os
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_URL = os.getenv("GROUP_URL")
PORT = int(os.getenv("PORT", 8080))

# Initialize bot
app = Client("welcome_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Flask server to keep the bot alive
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is running!"

def run_flask():
    server.run(host="0.0.0.0", port=PORT)

# Start Flask in a separate thread
Thread(target=run_flask, daemon=True).start()

# Dictionary to store user share status
user_shares = {}

# Dictionary to store last welcome message ID per group
last_welcome_messages = {}

@app.on_message(filters.new_chat_members)
async def welcome(client: Client, message: Message):
    chat_id = message.chat.id
    
    # Delete previous welcome message if it exists
    if chat_id in last_welcome_messages:
        try:
            await client.delete_messages(chat_id, last_welcome_messages[chat_id])
        except Exception as e:
            print(f"Error deleting previous message: {e}")
    
    # Prepare new welcome message
    invite_link = f"{GROUP_URL}"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Share Group Link To 0/5", switch_inline_query=invite_link)],
        [InlineKeyboardButton("✅ Check Share Status", callback_data="check_share")]
    ])
    sticker_id = "CAACAgEAAxkBAAENuT9no6sQKZqBFjjBYd1DAUW_PFv_4gACMQIAAoKgIEQHCzBVrLHGhzYE"
    
    sent_message = await client.send_sticker(chat_id=chat_id, sticker=sticker_id, reply_markup=buttons)
    
    # Store new welcome message ID using .id
    last_welcome_messages[chat_id] = sent_message.id

@app.on_callback_query(filters.regex("^check_share"))
async def check_share(client, callback_query):
    user_id = callback_query.from_user.id
    if user_shares.get(user_id, False):
        await callback_query.answer("✅ You have shared the group link!", show_alert=True)
    else:
        await callback_query.answer("❌ You have NOT shared the group link!", show_alert=True)

@app.on_message(filters.command("markshared") & filters.group)
async def mark_shared(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_shares[user_id] = True
        await message.reply_text(f"✅ {message.reply_to_message.from_user.mention} has shared the group link!")

# Run bot
app.run()

