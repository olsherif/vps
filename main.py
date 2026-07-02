import asyncio
from pyrogram import Client, filters

# بياناتك الرسمية والصحيحة
BOT_TOKEN = "8732755225:AAE8S3CRPeuO5nZTG8pTGDm61_xMcpjdOsE"
API_ID = 29250880
API_HASH = "efd75c5c849f429cbd0651d74a94da13"
ADMIN_CHAT_ID = 5458291853  # الـ ID الشخصي الجديد بتاعك

# تهيئة البوت
bot = Client("test_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    await message.reply_text("👋 أهلاً بك يا صاحبي! البوت شغال وسامعك ومستني المحاضرة.")

@bot.on_message(filters.private)
async def handle_all_messages(client, message):
    # التحقق من أنك أنت المطور
    if message.chat.id != ADMIN_CHAT_ID:
        await message.reply_text("عذراً، هذا البوت خاص بالمطور فقط.")
        return
        
    # إذا أرسلت رسالة نصية عادية
    if message.text:
        await message.reply_text(f"📥 أنا استلمت رسالتك النصية: {message.text}")
        
    # إذا أرسلت فيديو أو ملف
    elif message.video or message.document:
        media = message.video or message.document
        await message.reply_text(
            f"🎬 **يا مسهل! استلمت الفيديو بنجاح:**\n"
            f"📦 الاسم: {media.file_name}\n"
            f"⚖️ الحجم: {media.file_size / (1024*1024):.2f} ميجابايت.\n\n"
            f"🔄 كود التيست شغال تمام، كدة نقدر نرجع للخطوة الجاية ونصلح كود الرابط العام."
        )

if __name__ == "__main__":
    print("🚀 البوت يبدأ التشغيل الآن كـ Test...")
    bot.run()
