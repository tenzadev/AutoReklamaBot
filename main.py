import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, ADMINS
from keyboards import main_markup, colors, contact, confirm_markup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import AutoInfo
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"], state="*")
async def do_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    try:
        await message.answer(f"Assalomu aleykum {full_name}!\n\nID: {user_id}\nUsername: @{username}", reply_markup=main_markup)
    except Exception as error:
        logging.error(error)


@dp.message_handler(text="🚙 Mashina sotish")
async def sotish(message: types.Message):
    await message.answer("Mashinangizni nomini kiriting", reply_markup=ReplyKeyboardRemove())
    await AutoInfo.title.set()


@dp.message_handler(state=AutoInfo.title)
async def get_auto_title(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data({"title": title})
    await message.answer("Mashinangizning ishlab chiqarilgan yilini kiriting\n\n<b>Masalan: 2021</b>", parse_mode="html")
    await AutoInfo.next()
    

@dp.message_handler(lambda message: message.text.isdigit(), state=AutoInfo.year)
async def get_auto_year(message: types.Message, state: FSMContext):
    year = message.text
    await state.update_data({"year": year})
    await message.answer("Mashinangizning rangini tanlang", reply_markup=colors)
    await AutoInfo.next()

@dp.callback_query_handler(state=AutoInfo.color)
async def get_auto_color(call: types.CallbackQuery, state: FSMContext):
    color = call.data
    await state.update_data({"color": color})
    await call.answer(text=f"{color.title()} rangini tanladingiz")
    await call.message.delete()
    await call.message.answer("Mashinangizni bosib o'tgan masofasini kiriting (km)?")
    await AutoInfo.probeg.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=AutoInfo.probeg)
async def get_auto_probeg(message: types.Message, state: FSMContext):
    probeg = message.text
    await state.update_data({"probeg": probeg})
    await message.answer("Mashinangizning rasmini yuboring")
    await AutoInfo.image.set()


@dp.message_handler(content_types=["photo"], state=AutoInfo.image)
async def get_auto_image(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data({"photo": photo_id})
    await message.answer("Bog'lanish uchun raqamizni yuboring", reply_markup=contact)
    await AutoInfo.next()


@dp.message_handler(state=AutoInfo.phone)
@dp.message_handler(content_types=["contact"], state=AutoInfo.phone)
async def get_auto_phone(message: types.Message, state: FSMContext):
    if message.text:
        phone = message.text
    else:
        phone = message.contact.phone_number
    await state.update_data({"phone": phone})
    await message.answer("Mashinangizni narxini kiriting ($ dagi narxi)", reply_markup=ReplyKeyboardRemove())
    await AutoInfo.price.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=AutoInfo.price)
async def get_auto_price(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data({"price": price})
    data = await state.get_data()
    msg = f"<b>Mashina ma'lumotlari</b>\n\nNomi: {data.get('title')}\nYili: {data.get('year')} - yil\nRangi: {data.get('color')}\nProbeg: {data.get('probeg')} km\nTelefon raqam: {data.get('phone')}\nTelegram: @{message.from_user.username}\n\n<b>Mashina narxi: {data.get('price')}$</b>"
    await message.answer_photo(photo=data.get('photo'), caption=msg, parse_mode="html", reply_markup=confirm_markup)
    await AutoInfo.confirm.set()


@dp.callback_query_handler(state=AutoInfo.confirm, text="no")
async def delete_data(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer("Ma'lumotlar bekor qilindi")
    await call.message.answer("Menyulardan birini tanlang", reply_markup=main_markup)
    await state.finish()


@dp.callback_query_handler(state=AutoInfo.confirm, text="yes")
async def send_to_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer("Adminga jo'natildi", show_alert=True)
    await call.message.send_copy(chat_id=ADMINS[0])
    await call.message.answer("Menyulardan birini tanlang", reply_markup=main_markup)
    await state.finish()


@dp.callback_query_handler(text="yes", chat_id=ADMINS)
async def send_to_channel(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer("Kanalga jo'natildi!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
