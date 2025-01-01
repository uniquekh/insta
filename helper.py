from pyrogram.client import Client  # Explicit import for Client
from pyrogram import filters
from instaloader import Instaloader, Post
import re
import os
import shutil

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
