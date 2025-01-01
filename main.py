from pyrogram.client import Client  # Explicit import for Client
from pyrogram import filters
from instaloader import Instaloader, Post
import re
import os
import shutil

api_id = '29388606'  
api_hash = 'ddc1032e4e1fd0216362d18b68afd848'
bot_token="7232058622:AAFXlI9rZ5rGl4pE5Y5vAoPtI79Qn7w6JN0" 

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

L = Instaloader()



@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Send me an Instagram link (post or reel) and I'll download it for you.\n\nSend me a direct Instagram link.")

@app.on_message(filters.text)
async def handle_message(client, message):
    link = message.text.strip()
    if "instagram.com" in link:
        response = await linkdownload_and_send(link, message.chat.id)
        await message.reply(response)
    else:
        await message.reply("Please send a valid Instagram link.")

app.run()
