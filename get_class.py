from discord.ext import commands
import os
import discord
from get_class import get_class 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

UPLOAD_FOLDER = r"C:\Kodlar\Kodland\PythonPro\Discord\Ai_bot2\M7L2_ai_bot\M7L2_ai_bot\uploads"
MODEL_PATH = r"C:\Kodlar\Kodland\PythonPro\Discord\Ai_bot2\M7L2_ai_bot\M7L2_ai_bot\keras_model.h5"
LABELS_PATH = r"C:\Kodlar\Kodland\PythonPro\Discord\Ai_bot2\M7L2_ai_bot\M7L2_ai_bot\labels.txt"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

# Açıklamalar sözlüğü
CLASS_DESCRIPTIONS = {
    "Arduino UNO": "Arduino UNO, çok amaçlı ve yaygın kullanılan bir mikrodenetleyici kartıdır. Elektronik projeler için idealdir.",
    "Raspberry Pi": "Raspberry Pi, küçük boyutlu ancak güçlü bir bilgisayardır. Eğitim ve gömülü sistemlerde sıkça kullanılır.",
    "Esp32": "ESP32, Wi-Fi ve Bluetooth destekli bir mikrodenetleyicidir. IoT (Nesnelerin İnterneti) projelerinde çok kullanılır.",
    "Direnç": "Direnç, elektrik akımını sınırlayan temel devre elemanıdır. Neredeyse her devrede bulunur.",
    "Led": "LED (ışık yayan diyot), projelerde ışık göstergesi olarak kullanılır.",
    "Breadboard": "Breadboard, elektronik devreleri lehimsiz olarak kurmak için kullanılır. Deneme devrelerinde idealdir.",
    "Transistör": "Transistör, akımı kontrol eder. Anahtarlama ve yükseltme işlevi görür.",
    "Entegre devre": "Entegre devre (IC), birçok elektronik bileşeni tek bir çipte barındırır.",
    "Motor sürücü": "Motor sürücüler, düşük güçlü sinyallerle motorları çalıştırmaya yarar.",
    "Dc Motor": "DC motor, doğru akımla çalışan, dönme hareketi üreten motordur.",
    "Elektrolitik Kondansatör": "Bu kondansatörler enerji depolar, genelde büyük kapasiteli ve kutupludurlar.",
    "Seramik Kondansatör": "Seramik kondansatör, küçük, kutupsuz ve genellikle filtreleme işlerinde kullanılır.",
    "Servo Motor": "Servo motorlar, belirli bir açıya hassas şekilde dönebilen motorlardır. Robotikte yaygındır.",
    "Ultrasonik Sensör": "Bu sensör ses dalgaları göndererek mesafeyi ölçer. Engel algılamada kullanılır.",
    "OLED / TFT Ekran": "Küçük grafik ekranlardır. Görsel veri sunumunda kullanılır.",
    "RTC Modülü (DS3231)": "Gerçek zamanlı saat modülüdür. Saat ve tarih bilgisini doğru şekilde tutar.",
    "Röle Modülü": "Röle, düşük güçlü bir sinyal ile yüksek güçlü devreyi kontrol etmeye yarar.",
    "LDR": "LDR (ışığa duyarlı direnç), ortam ışığına göre direnci değişen bir sensördür.",
    "IR ALICI": "Kızılötesi alıcı, uzaktan kumandaların gönderdiği IR sinyallerini algılar.",
    "Potansiyometre": "Kullanıcı tarafından ayarlanabilen bir dirençtir. Genellikle analog girişlerde kullanılır."
}

@bot.command(name="yükle")
async def yükle(ctx):
    attachments = ctx.message.attachments

    if not attachments:
        await ctx.send("❌ Görsel bulunamadı. Lütfen bir görsel yükleyin.")
        return

    for attachment in attachments:
        _, ext = os.path.splitext(attachment.filename.lower())
        if ext not in ALLOWED_EXTENSIONS:
            await ctx.send(f"❌ Geçersiz dosya formatı: `{attachment.filename}`. Lütfen PNG, JPG veya JPEG dosyası yükleyin.")
            continue

        file_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
        await attachment.save(file_path)
        await ctx.send(f"✅ {attachment.filename} kaydedildi, model çalıştırılıyor...")

    try:
        result = get_class(MODEL_PATH, LABELS_PATH, file_path)

        if not result or not isinstance(result, str) or result.strip().lower() in ["", "unknown", "none"]:
            await ctx.send("🤖 Üzgünüm, resimde neyin gösterildiğinden emin değilim.")
        else:
            result_clean = result.strip()
            description = CLASS_DESCRIPTIONS.get(result_clean, "Bu bileşen hakkında detaylı bilgi bulunamadı.")
            await ctx.send(f"🤖 Modelin tahmini: **{result_clean}**\nℹ️ {description}")
    except Exception as e:
        await ctx.send(f"❌ Tahmin sırasında hata oluştu: {e}")


# Botu çalıştır
bot.run("TOKEN")
