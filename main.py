import discord
from discord.ext import commands
import os
from get_class import get_class  # Model fonksiyonunu içe aktar

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

UPLOAD_FOLDER = r"C:\Kodlar\Kodland\PythonPro\Discord\Ai_bot2\M7L2_ai_bot\M7L2_ai_bot\uploads"
MODEL_PATH = "C:\Kodlar\Kodland\PythonPro\Discord\Ai_bot2\M7L2_ai_bot\M7L2_ai_bot\keras_model.h5"
LABELS_PATH = "C:\Kodlar\Kodland\PythonPro\Discord\Ai_bot2\M7L2_ai_bot\M7L2_ai_bot\labels.txt"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bot.command(name="yükle")
async def yükle(ctx):
    attachments = ctx.message.attachments

    if not attachments:
        await ctx.send("❌ Görsel bulunamadı. Lütfen bir görsel yükleyin.")
        return

    for attachment in attachments:
        file_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
        await attachment.save(file_path)
        await ctx.send(f"✅ `{attachment.filename}` kaydedildi, model çalıştırılıyor...")

        try:
            result = get_class(MODEL_PATH, LABELS_PATH, file_path)
            await ctx.send(f"🤖 Modelin tahmini: **{result}**")
        except Exception as e:
            await ctx.send(f"❌ Tahmin sırasında hata oluştu: `{e}`")

# Botu çalıştır
bot.run("token")
