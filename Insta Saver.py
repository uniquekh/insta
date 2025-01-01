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

async def linkdownload_and_send(link, chat_id):
    id_pattern = r"(/p/|/reel/)([a-zA-Z0-9_-]+)/"
    match = re.search(id_pattern, link)

    if match:
        post_id = match.group(2)
        post = Post.from_shortcode(L.context, post_id)
        print(f"Downloading post: {post}...")

        caption = post.caption if post.caption else "No caption available"
        print(f"Post caption: {caption}")

        downloading_message = await app.send_message(chat_id, "Downloading... Please wait.")

        os.makedirs("downloads", exist_ok=True)

        try:
            L.download_post(post, target="downloads")
        except Exception as e:
            await app.send_message(chat_id, f"An error occurred while downloading: {e}")
            return

        files = os.listdir("downloads")

        video_files = [file for file in files if file.endswith('.mp4')]
        image_files = [file for file in files if file.endswith('.jpg') or file.endswith('.png')]

        if video_files:
            video_path = os.path.join("downloads", video_files[0])
            await app.send_video(chat_id, video_path, caption=caption)

        elif image_files:
            image_path = os.path.join("downloads", image_files[0])
            await app.send_photo(chat_id, image_path, caption=caption)

        else:
            await app.send_message(chat_id, "Error: No media file found in the download folder.")

        await downloading_message.delete()

        # Clean up the downloads folder
        shutil.rmtree("downloads")

        print("Downloads folder has been cleared.")
        return f"Post downloaded successfully and sent to you!"
    else:
        return "Invalid link! Please provide a valid Instagram post or reel link."

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
