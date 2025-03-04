import random
import asyncio
import logging
from pyrogram import Client, filters
from dotenv import load_dotenv
import os
from threading import Thread
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PORT = int(os.getenv("PORT", 5000))  # Default to port 5000 if not set
GROUP_URL = os.getenv("GROUP_URL")
GROUP_CHAT_ID = int(os.getenv("GROUP_ID"))

# Create a bot instance
app = Client("welcome4u", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Flask server to keep the bot alive
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is running!"

def run_flask():
    logger.info("Starting Flask server...")
    server.run(host="0.0.0.0", port=PORT)

# Dictionary to store user share status
user_shares = {}

# Dictionary to store last welcome message ID per group
last_welcome_messages = {}

@app.on_message(filters.new_chat_members)
async def welcome(client: Client, message: Message):
    chat_id = message.chat.id
    logger.info(f"New member joined chat {chat_id}")
    
    # Delete previous welcome message if it exists
    if chat_id in last_welcome_messages:
        try:
            await client.delete_messages(chat_id, last_welcome_messages[chat_id])
            logger.info(f"Deleted previous welcome message in chat {chat_id}")
        except Exception as e:
            logger.error(f"Error deleting previous message in chat {chat_id}: {e}")
    
    # Prepare new welcome message
    share_url = f"https://t.me/share/url?url={GROUP_URL}"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Share To 5 Friends To Unlock 0/5", url=share_url)],
        [InlineKeyboardButton("Group Link", url="https://t.me/+g-q9tHqBSpkwYmI9")],
        [InlineKeyboardButton("Join", callback_data="check_share")]
    ])
    sticker_id = "CAACAgEAAxkBAAENuT9no6sQKZqBFjjBYd1DAUW_PFv_4gACMQIAAoKgIEQHCzBVrLHGhzYE"
    
    sent_message = await client.send_sticker(chat_id=chat_id, sticker=sticker_id, reply_markup=buttons)
    logger.info(f"Sent welcome message in chat {chat_id}")
    
    # Store new welcome message ID using .id
    last_welcome_messages[chat_id] = sent_message.id

@app.on_callback_query(filters.regex("^check_share"))
async def check_share(client, callback_query):
    user_id = callback_query.from_user.id
    if user_shares.get(user_id, False):
        await callback_query.answer("✅ You have shared the group link!", show_alert=True)
        logger.info(f"User {user_id} has shared the group link")
    else:
        await callback_query.answer("💎 Note: ⏱️ᴡᴀɪᴛ 𝟤𝟦ʜʀ ғᴏʀ ɢʀᴏᴜᴘ ᴠᴀʟɪᴅᴀᴛɪᴏɴ ! \n\n ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜʀ ᴀʀᴇ sʜᴀʀɪɴɢ ɢʀᴏᴜᴘ ʟɪɴᴋ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄᴏʀʀᴇᴄᴛʟʏ ᴍɪɴɪᴍᴜᴍ ᴍᴇᴍʙᴇʀ 𝟣𝟢𝟢!! ", show_alert=True)
        logger.info(f"User {user_id} Note: ⏱️ᴡᴀɪᴛ 𝟤𝟦ʜʀ ғᴏʀ ɢʀᴏᴜᴘ ᴠᴀʟɪᴅᴀᴛɪᴏɴ !! ")

@app.on_message(filters.command("markshared") & filters.group)
async def mark_shared(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_shares[user_id] = True
        await message.reply_text(f"✅ {message.reply_to_message.from_user.mention} has shared the group link!")
        logger.info(f"Marked user {user_id} as having shared the group link")

# Global variable to keep track of the task
random_message_task = None
last_random_message_id = None

async def send_random_message():
    global last_random_message_id  # Declare as global to update the variable
    while True:
        L = [
            "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
            "Shaurya", "Atharv", "Aaryan", "Kabir", "Dhruv", "Ritvik", "Rudra", "Ansh", "Aarush", "Aryan",
            "Arnav", "Advait", "Aaditya", "Aadya", "Aahan", "Aarav", "Aayush", "Abhay", "Abhinav", "Advik",
            "Agastya", "Ahaan", "Ahan", "Akarsh", "Akshaj", "Amay", "Anay", "Anirudh", "Ansh", "Anshul",
            "Arhaan", "Arin", "Arnav", "Arush", "Aryan", "Atharva", "Avyaan", "Ayansh", "Ayush", "Bhavya",
            "Chaitanya", "Darsh", "Dev", "Devansh", "Dhruv", "Divit", "Eshan", "Gaurav", "Harsh", "Hriday",
            "Ishaan", "Ivaan", "Jai", "Jatin", "Jivaan", "Kabir", "Kairav", "Kartik", "Kiaan", "Krish",
            "Laksh", "Lakshay", "Madhav", "Manan", "Moksh", "Nirvaan", "Om", "Parth", "Pranav", "Raghav",
            "Ranbir", "Reyansh", "Rishaan", "Ritvik", "Rudra", "Samar", "Samarth", "Shaan", "Shaurya",
            "Shivansh", "Shrey", "Siddharth", "Sparsh", "Tanish", "Tejas", "Ved", "Vihaan", "Vivaan", "Yash"
        ]
        message = f"{random.choice(L)} has unlocked premium group 🔓"
         # Delete the last random message if it exists
        if last_random_message_id is not None:
            try:
                await app.delete_messages(GROUP_CHAT_ID, last_random_message_id)
                logger.info(f"Deleted previous random message with ID {last_random_message_id}")
            except Exception as e:
                logger.error(f"Error deleting previous random message: {e}")
        
        # Send new random message
        sent_message = await app.send_message(GROUP_CHAT_ID, message)
        logger.info(f"Sent random message: {message}")
        
        # Store the new message ID
        last_random_message_id = sent_message.id
        
        await asyncio.sleep(random.randint(10, 120))

@app.on_message(filters.text)
async def sjsa(c, m):
    global random_message_task
    # Cancel the old task if it exists
    if random_message_task is not None:
        random_message_task.cancel()
        logger.info("Cancelled previous random message task")
    # Start the random message sender
    random_message_task = asyncio.create_task(send_random_message())
    logger.info("Started new random message task")

if __name__ == "__main__":
    # Start Flask in a separate thread
    Thread(target=run_flask, daemon=True).start()
    logger.info("Starting bot...")
    app.run()
