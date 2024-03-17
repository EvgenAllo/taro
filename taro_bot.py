from aiogram import Bot, Dispatcher, executor, types
from random import randint
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

API_TOKEN = '5770093719:AAE3dy3XxK3SHY41E8IDEI3UWJOcHFEW33g'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

TARO = {1: ['https://avatars.dzeninfra.ru/get-zen_doc/5236207/pub_63383af93c55cc1557ed0f09_63383afd71a6914e41bd151b/scale_1200',
        'Вы находитесь на пороге неожиданного и захватывающего нового приключения. Это может потребовать от вас совершить слепой прыжок веры.',
        'Дурак'],
        2: ['https://avatars.dzeninfra.ru/get-zen_doc/5097825/pub_63383af93c55cc1557ed0f09_63383afdd64c9a5b9c82c364/scale_1200',
        'Вы можете быть уверены, что у вас есть стремление осуществить свои мечты.',
        'Маг'],
        3: ['https://avatars.dzeninfra.ru/get-zen_doc/5283638/pub_63383af93c55cc1557ed0f09_63383afdb741fb6da17df75e/scale_1200',
        'Вам нужно время для обучения и прислушивания к вашей интуиции, а не для того, чтобы отдавать приоритет вашему интеллекту и сознательному разуму. Вам нужно замедлиться и подумать о том, что вы узнали, и получить еще больше знаний, прежде чем принимать решение или действовать.',
        'Верховная жрица']
}



kb = ReplyKeyboardMarkup(resize_keyboard=True)
bt = KeyboardButton('Получить таро расклад')
kb.add(bt)


vote = InlineKeyboardMarkup(row_width=2)
vote_b1 = InlineKeyboardButton(text='🥰',callback_data='like')
vote_b2 = InlineKeyboardButton(text='Давай еще',callback_data='next')
vote.add(vote_b1,vote_b2)


async def on_startup(_):
   print('Бот запущен')

async def send_taro(message: types.Message):
    a = randint(1,3)
    await bot.send_message(chat_id=message.chat.id,text='Твой расклад на сегодня:')
    await bot.send_photo(chat_id=message.chat.id, 
                        photo=TARO[a][0],
                        caption=TARO[a][2]) 
    await bot.send_message(chat_id=message.chat.id,text=TARO[a][1],
                            reply_markup=vote)
    

kb_taro = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='Карта дня')
b2 = KeyboardButton(text='Главное меню')
kb_taro.add(b1,b2)

@dp.message_handler(Text(equals='Получить таро расклад'))
async def karta(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,text='Чтобы получить таро расклад - нажми на "Карта дня"',)



@dp.message_handler(Text(equals='Главное меню'))
async def menu(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Добро пожаловать в главное меню', 
                           reply_markup=kb)

@dp.message_handler(commands=['start']) 
async def send_welcome(message: types.Message):
   await bot.send_message(chat_id=message.chat.id,text='Готов узнать свою судьбу?',reply_markup=kb)
   await message.delete()


@dp.message_handler(Text(equals='Карта дня'))
async def photo(message: types.Message):
   await send_taro(message)



@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer(text='Рад, что тебе понравилось')
    elif callback.data == 'next':
        await send_taro(message=callback.message)

# @dp.message_handler()
# async def echo(message: types.Message):
#    await bot.send_message(chat_id=message.chat.id, text='hello!')

if __name__ == '__main__':
   executor.start_polling(dp, on_startup=on_startup)
