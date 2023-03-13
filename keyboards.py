from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row("🚙 Mashina sotish")

colors = InlineKeyboardMarkup(row_width=1)
colors_lst = [("🟥 Qizil 🟥", "red"), ("⚪️ Oq ⚪️", "white"), ("⚫️ Qora ⚫️", "black"), ("🔵 Moviy 🔵", "blue"), ("🟡 Sariq 🟡", "yellow")]

for color in colors_lst:
    colors.insert(InlineKeyboardButton(text=color[0], callback_data=color[1]))

contact = ReplyKeyboardMarkup(resize_keyboard=True)
contact.add(KeyboardButton(text="📞 Raqamni yuborish", request_contact=True))


confirm_markup = InlineKeyboardMarkup(row_width=2)
confirm_markup.row(InlineKeyboardButton(text="✅ Ha", callback_data="yes"), InlineKeyboardButton(text="❌ Yo'q", callback_data="no"))
