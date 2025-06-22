from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from googletrans import Translator
import os

TOKEN = os.environ.get("TOKEN", "zzzzzzzz")
API_ID = int(os.environ.get("API_ID", "8953338"))
API_HASH = os.environ.get("API_HASH", "fe21f223cb02d8f7c1cbda651f553a45")

app = Client("Gtt", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

# Başlanğıc mesajı
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply_text(
        f"Salam **{message.from_user.first_name}**\n\n"
        "__Mən Tərcüməçi Botuyam 🌎\n"
        "Göndərdiyin Mesajı Seçdiyin Dilə Tərcümə Etmək Üçün Proqramlaşdırılmışam.\n"
        "Başlamaq Üçün Mənə 1 Mesaj Göndər.__",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🐾 Owner", url="https://t.me/vusalxw")],
            [InlineKeyboardButton("Yenilik Kanalı 🌎", url="https://t.me/TercumeciBotYenilikler")]
        ])
    )

# Əsas dillər klaviaturası
language_pages = {
    "page1": [
        ["az", "de", "fr"],
        ["ko", "en", "tr"],
        ["el", "be", "ru"],
        ["pt", "bg", "es"],
        ["fa", "hr", "cs"],
        ["da", "it", "uk"]
    ],
    "page2": [
        ["hy", "et", "fi"],
        ["am", "fy", "gl"],
        ["ka", "sq", "eu"],  # eu = Bask dili
        ["gu", "ht", "ha"],
        ["hi", "hu", "is"],
        ["ig", "id", "ga"]
    ]
    # Əlavə səhifələr buraya əlavə edilə bilər...
}

def get_language_keyboard(page):
    buttons = []
    for row in language_pages.get(page, []):
        btn_row = [InlineKeyboardButton(lang.upper(), callback_data=lang) for lang in row]
        buttons.append(btn_row)
    buttons.append([
        InlineKeyboardButton("««« Geri", callback_data="page1") if page != "page1" else InlineKeyboardButton(" ", callback_data="none"),
        InlineKeyboardButton("Növbəti »»»", callback_data="page2" if page == "page1" else "page1")
    ])
    return InlineKeyboardMarkup(buttons)

# İstifadəçi mətn göndərəndə dilləri göstər
@app.on_message(filters.private & filters.text)
async def ask_language(client, message):
    await message.reply_text(
        "👇 Dili Seçin:",
        reply_to_message_id=message.message_id,
        reply_markup=get_language_keyboard("page1")
    )

# Callback Query ilə dilləri dəyiş və ya tərcümə et
@app.on_callback_query()
async def handle_callback(client, callback_query):
    data = callback_query.data
    message = callback_query.message
    reply_text = message.reply_to_message.text if message.reply_to_message else ""

    if data.startswith("page"):
        await message.edit_text("Dili Seçin:", reply_markup=get_language_keyboard(data))
    elif reply_text:
        try:
            translated = Translator().translate(reply_text, dest=data)
            await message.edit_text(f"**Tərcümə:**\n{translated.text}")
        except Exception as e:
            await message.edit_text(f"Xəta baş verdi: {e}")
    else:
        await message.edit_text("Tərcümə üçün zəhmət olmasa bir mesaja cavab verin.")

app.run()
