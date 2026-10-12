import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

# Setup logging
logging.basicConfig(level=logging.INFO)

# Mengambil konfigurasi dari Heroku Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Mengambil list kata kunci (diubah menjadi huruf kecil dan dipisahkan dengan koma)
PIN_KEYWORDS = [k.strip().lower() for k in os.environ.get("PIN_KEYWORDS", "").split(",") if k.strip()]
DELETE_KEYWORDS = [k.strip().lower() for k in os.environ.get("DELETE_KEYWORDS", "").split(",") if k.strip()]

# Inisialisasi Bot
app = Client("FilterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
def start_command(client, message: Message):
    message.reply_text("Halo! Saya adalah bot Auto-Pin & Auto-Delete. Masukkan saya ke grup dan jadikan Admin agar saya bisa bekerja.")

@app.on_message(filters.group & ~filters.service)
def filter_messages(client, message: Message):
    if not message.text:
        return

    text_lower = message.text.lower()

    # 1. Modul Auto-Delete (Dahulukan hapus jika kata kunci bentrok)
    for kw in DELETE_KEYWORDS:
        if kw in text_lower:
            try:
                message.delete()
                logging.info(f"Berhasil menghapus pesan berisi: '{kw}' dari user {message.from_user.id if message.from_user else 'Anonim'}")
                return # Stop proses agar tidak lanjut ke auto-pin jika pesan sudah dihapus
            except Exception as e:
                logging.error(f"Gagal menghapus pesan: {e}")

    # 2. Modul Auto-Pin
    for kw in PIN_KEYWORDS:
        if kw in text_lower:
            try:
                message.pin(disable_notification=False)
                logging.info(f"Berhasil menyematkan pesan berisi: '{kw}'")
                break
            except Exception as e:
                logging.error(f"Gagal menyematkan pesan: {e}")

if __name__ == "__main__":
    logging.info("Bot sedang berjalan...")
    app.run()
