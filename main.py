import os
import asyncio
from contextlib import asynccontextmanager
from pyrogram import Client, filters
from pyrogram.storage import MemoryStorage
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

BOT_TOKEN = "8732755225:AAE8S3CRPeuO5nZTG8pTGDm61_xMcpjdOsE"
API_ID = 29250880
API_HASH = "efd75c5c849f429cbd0651d74a94da13"
ADMIN_CHAT_ID = 5458291853

PORT = int(os.environ.get("PORT", 8000))

# الحل الصحيح: تمرير اسم الجلسة داخل MemoryStorage لمنع الكراش
bot = Client(
    "olmep_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN,
    storage=MemoryStorage("olmep_session")
)

file_db = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ربط البوت بـ Async Loop الخاصة بالسيرفر للتوافق الكامل
    loop = asyncio.get_running_loop()
    bot.loop = loop
    
    await bot.start()
    print("🚀 البوت انطلق بنجاح مئة بالمئة...")
    yield
    try:
        await bot.stop()
    except:
        pass

app = FastAPI(lifespan=lifespan)

@bot.on_message(filters.private & (filters.video | filters.document))
async def handle_video(client, message):
    if message.chat.id != ADMIN_CHAT_ID:
        await message.reply_text("عذراً، هذا البوت خاص بصاحبه فقط.")
        return

    file_id = message.id
    file_db[file_id] = message
    
    domain = os.environ.get("KOYEB_APP_NAME", "localhost")
    public_link = f"https://{domain}.koyeb.app/stream/{file_id}"
    
    await message.reply_text(
        f"✅ **تم توليد الرابط العام بنجاح وبأعلى سرعة!**\n\n"
        f"🔗 **رابط الويب العام:**\n{public_link}\n\n"
        f"🚀 ابعته لزمايلك وهيفتح معاهم أونلاين أو تحميل مباشر."
    )

@bot.on_message(filters.private & filters.text)
async def handle_text(client, message):
    if message.chat.id == ADMIN_CHAT_ID:
        await message.reply_text("👋 البوت مستقر وشغال 100%! حوّل لي فيديو المحاضرة الخاصة الآن وسأعطيك الرابط العام فوراً.")

async def media_streamer(message):
    async for chunk in bot.download_media(message, block=True):
        yield chunk

@app.get("/stream/{file_id}")
async def stream_file(file_id: int):
    if file_id not in file_db:
        return {"error": "الملف غير موجود أو انتهت الجلسة السحابية"}
    
    message = file_db[file_id]
    media = message.video or message.document
    
    return StreamingResponse(
        media_streamer(message),
        media_type=media.mime_type,
        headers={
            "Content-Disposition": f"attachment; filename={media.file_name}",
            "Content-Length": str(media.file_size)
        }
    )

@app.get("/")
async def root():
    return {"status": "Running perfectly with named MemoryStorage"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
