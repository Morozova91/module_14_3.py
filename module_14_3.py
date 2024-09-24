from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "7413705335:AAHT7sRNGabDStOWFzceRfJ3AObc8aoccBA"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать')
        ],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)

choise_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="Calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="Formulas")]
    ]
)

buy_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Product1", callback_data="product_buying"),
            InlineKeyboardButton(text="Product2", callback_data="product_buying"),
            InlineKeyboardButton(text="Product3", callback_data="product_buying"),
            InlineKeyboardButton(text="Product4", callback_data="product_buying")
        ]
    ]
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f"Привет, {message.from_user.username}! Я бот помогающий твоему здоровью.",
                         reply_markup=start_menu)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('4e8ff6c7ca.jpg', "rb") as product_1:
        await message.answer_photo(product_1, f"Название: Product1 | Описание: OMEGA | Цена: {1 * 100}")
    with open("565a8054188387.5951564646c61.jpg", "rb") as product_2:
        await message.answer_photo(product_2, f"Название: Product2 | Описание: VITAMIN E | Цена: {2 * 100}")
    with open("3398097.jpg", "rb") as product_3:
        await message.answer_photo(product_3, f"Название: Product3 | Описание: BIOSPHIN | Цена: {3 * 100}")
    with open("1023830430.jpg", "rb") as product_4:
        await message.answer_photo(product_4, f"Название: Product4 | Описание: PERSICAPS | Цена: {4 * 100}")
    await message.answer("Выберите продукт для покупки:", reply_markup=buy_menu)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=choise_menu)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Можете рассчитать норму калорий, чтобы выбрать продукт))')
    with open('../module_14/99px_ru_animacii_7234_chernij_kot_tochit_pilochkoj_svoi_kogti.gif', 'rb') as file:
        await message.answer_video(file, choise_menu, reply_markup=choise_menu)



class UserState(StatesGroup):
    sex = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=choise_menu)


@dp.callback_query_handler(text='Formulas')
async def get_formulas(call):
    await call.message.answer(
        'Расчет по формуле Миффлина-Сан Жеора для мужчин = 10 * Вес(в кг) + 6.25 * Рост(в см) - 5 * Возраст + 5,\n '
        'Расчет по формуле Миффлина-Сан Жеора для женщин = 10 * Вес(в кг) + 6.25 * Рост(в см) - 5 * Возраст - 161')
    await call.answer()


@dp.callback_query_handler(text='Calories', state=None)
async def sex_form(call):
    await call.message.answer('Введите свой пол: ')
    await UserState.sex.set()
    await call.answer()


@dp.message_handler(state=UserState.sex)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await message.reply('Введите свой возраст:')
    await UserState.age.set()


# Функция для установки роста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply('Введите свой рост (в см):')
    await UserState.growth.set()


# Функция для установки веса
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.reply('Введите свой вес (в кг):')
    await UserState.weight.set()


# Функция для расчета и отправки нормы калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    sex = str(data['sex'])
    if sex == 'мужской':
        # Расчет по формуле Миффлина-Сан Жеора для мужчин
        calories = int(10 * weight + 6.25 * growth - 5 * age + 5)
    elif sex == 'женский':
        calories = int(10 * weight + 6.25 * growth - 5 * age - 161)

    await message.reply(f"Ваша норма калорий: {calories} ккал в день")
    await state.finish()


@dp.message_handler()  #этот хендлер лучше ставить в самый конец, иначе он будет перехватывать все остальные
async def all_messages(message):
    print('Получено новое сообщение')
    await message.answer('Введите команду \start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
