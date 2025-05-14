import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# YouTube/Instagram/TikTok yuklab olish funksiyasi
def download_video(url):
    ydl_opts = {
        "format": "mp4",
        "outtmpl": "video.%(ext)s",
        "quiet": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# /start komandasi
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Salom! YouTube, Instagram yoki TikTok link yuboring, men videoni yuklab beraman.")

# Linkni tutish va video yuborish
@dp.message()
async def download_handler(message: types.Message):
    url = message.text.strip()
    if any(x in url for x in ["youtube.com", "youtu.be", "instagram.com", "tiktok.com"]):
        await message.answer("⏳ Video yuklanmoqda, biroz kuting...")
        try:
            filename = download_video(url)
            with open(filename, "rb") as video:
                await message.reply_video(video)
            os.remove(filename)
        except Exception as e:
            await message.answer("❌ Yuklab bo‘lmadi. Link noto‘g‘ri yoki xatolik yuz berdi.")
            print("Error:", e)
    else:
        await message.answer("Faqat YouTube, Instagram yoki TikTok link yuboring.")

# Botni ishga tushurish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
