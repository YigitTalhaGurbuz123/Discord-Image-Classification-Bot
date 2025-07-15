import discord
from discord.ext import commands
from ultralytics import YOLO
import os

UPLOAD_FOLDER = "uploads"
MODEL_PATH = "yolov5s.pt"  # Küçük ve hızlı model
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# YOLO modelini yükle
model = YOLO(MODEL_PATH)

@bot.command(name="tahmin")
async def tahmin(ctx):
    attachments = ctx.message.attachments

    if not attachments:
        await ctx.send("❌ Lütfen bir görsel yükleyin.")
        return

    for attachment in attachments:
        file_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
        await attachment.save(file_path)
        await ctx.send(f"✅ `{attachment.filename}` kaydedildi. Model çalışıyor...")

        try:
            results = model(file_path)
            # Çıktıyı kaydet
            output_image = file_path.replace(".", "_result.")
            results[0].save(filename=output_image)

            # Discord'a gönder
            await ctx.send("📸 İşte algılanan nesneler:", file=discord.File(output_image))

        except Exception as e:
            await ctx.send(f"❌ Tahmin sırasında hata oluştu: {str(e)}")

bot.run("Token Buraya")
