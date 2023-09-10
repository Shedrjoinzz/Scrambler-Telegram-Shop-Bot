<img src="https://cdn4.iconfinder.com/data/icons/social-media-and-logos-12/32/Logo_telegram_Airplane_Air_plane_paper_airplane-33-256.png" align="right" width="131" />

# Telegram Bot Shop using aiogram-2v

This is a Telegram bot built on aiogram-2v, a powerful and flexible framework for creating Telegram bots in Python.

## Features

- **Functional**: Flexible Admin panel, flexible product and catalog management (Add/Removal/Change). Convenient management by Administrators

- **Payment system**: Pay-Master (TEST) | But you can change the code and make your own changes in the file handlers/topup_handler.py

- **Database**: Automatic creation of all necessary tables

## How to Use

Follow these steps to use the Telegram bot:

Clone this repository to your local computer:

```bash
git clone https://github.com/Shedrjoinzz/Scrambler-Telegram-Shop-Bot.git
```
1. Install the required dependencies using pip:
```bash
cd Scrambler-Telegram-Shop-Bot
pip install -r requirements.txt
```
2. Configure your bot:
  - Open libs/config.py and replace the token with your Telegram bot API token. Also replace the Owner ID of the Bot
  - Create a database.
  - Open data/jsonDataPostgre.py fill in your Database details.

3. Run the bot:
```bash
python main.py
```
