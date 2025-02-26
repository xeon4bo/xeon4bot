# Welcome Telegram  Bot

This bot is a Telegram group welcome bot that greets new users and encourages them to share the group link before they can participate. It also includes a Flask web server to keep the bot alive.

## Features
- Welcomes new members with a sticker and inline buttons.
- Encourages users to share the group link.
- Allows admins to mark users as having shared the link.
- Uses Flask to keep the bot running in hosting environments.

## Environment Variables
Ensure you set up the following environment variables before running the bot:

| Variable   | Description |
|------------|-------------|
| `API_ID`   | Your Telegram API ID |
| `API_HASH` | Your Telegram API Hash |
| `BOT_TOKEN` | The bot token from @BotFather |
| `GROUP_URL` | The invite link to your group |
| `PORT` | The port number for Flask (default: 8080) |
| `GROUP_ID` | Add GROUP ID) |

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/xeon4bo/xeon4bot
   cd xeon4bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the environment variables in a `.env` file:
   ```sh
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   GROUP_URL=your_group_url
   PORT=5000
   GROUP_ID=add_group_id
   ```
4. Run the bot:
   ```sh
   python bot.py
   ```

## License
This project is open-source. Feel free to modify and use it as needed!

