from aiogram import Dispatcher, types, executor, Bot
from aiogram.types.input_file import InputFile
from config import load_config
from data import dataXlsx, data_by_trek, prepare_data #, data_to_notifications
from connect_psql import user_exists, add_subscriber, update_subscription, subscriber_status, \
    get_lan, add_lan, update_lan, delete_admin, check_admin, create_admin, upload_table, gx_search_sql, trek_search_sql
import keyboards as kb
import asyncio
import logging

from decouple import config


logging.basicConfig(level=logging.INFO)

# Подключаемся к боту
token = config("Token")
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Выберите язык!', reply_markup=kb.greet_kb)


# Обрабатываем стартовое сообщение
@dp.message_handler(commands=['KGZ🇰🇬', 'RU🇷🇺'])
async def lan(message: types.Message):
    if check_admin(message.from_user.id):
        if message.text == '/KGZ🇰🇬':
            if not get_lan(message.from_user.id):
                add_lan(message.from_user.id, 'kgz')
            else:
                update_lan(message.from_user.id, 'kgz')
            await message.answer(text='Здравствуйте!\nДля добавления других админов воспользуйтесь командой '
                                      '/add_admin id '
                                      'пользователя\nДля удаления прав администратора воспользуйтесь командой '
                                      '/remove_admin id пользователя\nЧтобы узнать id можете использовать бота '
                                      '@getmyid_bot\nЧтобы добавить новую таблицу просто отправьте файл\nДля '
                                      'отслеживания '
                                      'ваших товаров введите /info ваш персональный '
                                      'номер\nСтрого в формате GX-0000!!!\nИли же можете воспользоваться командой '
                                      '/info_trek ваш трек\nВы также можете подписаться на '
                                      'уведомления по команде /subscribe GX-0000 и отписаться по команде /unsubscribe '
                                      'GX-0000',
                                 reply_markup=kb.blank_kb)
        elif message.text == '/RU🇷🇺':
            if not get_lan(message.from_user.id):
                add_lan(message.from_user.id, 'ru')
            else:
                update_lan(message.from_user.id, 'ru')
            await message.answer(text='Здравствуйте!\nДля добавления других админов воспользуйтесь командой '
                                      '/add_admin id '
                                      'пользователя\nДля удаления прав администратора воспользуйтесь командой '
                                      '/remove_admin id пользователя\nЧтобы узнать id можете использовать бота '
                                      '@getmyid_bot\nЧтобы добавить новую таблицу просто отправьте файл\nДля '
                                      'отслеживания '
                                      'ваших товаров введите /info ваш персональный '
                                      'номер\nСтрого в формате GX-0000!!!\nИли же можете воспользоваться командой '
                                      '/info_trek ваш трек\nВы также можете подписаться на '
                                      'уведомления по команде /subscribe GX-0000 и отписаться по команде /unsubscribe '
                                      'GX-0000',
                                 reply_markup=kb.blank_kb)

    else:
        if message.text == '/KGZ🇰🇬':
            if not get_lan(message.from_user.id):
                add_lan(message.from_user.id, 'kgz')
            else:
                update_lan(message.from_user.id, 'kgz')
            await message.answer(text='Саламатсызбы!\nТоварларыңызды көзөмөлдөө үчүн жазыңыз /info сиздин жеке '
                                      'номериңиз\nКатуу форматта болуш керек GX-0000!!!\nЖе сиз буйрукту колдоно '
                                      'аласыз /info_trek сиздин трек\nЭгер буюмуңуз жөнүндө '
                                      'эскертмелерди алгыңыз келсе, анда /subscribe GX-0000\nЖана /unsubscribe '
                                      'GX-0000 жазылууну токтотуу',
                                 reply_markup=kb.blank_kb)
        elif message.text == '/RU🇷🇺':
            if not get_lan(message.from_user.id):
                add_lan(message.from_user.id, 'ru')
            else:
                update_lan(message.from_user.id, 'ru')
            await message.answer(text='Здравствуйте!\nДля отслеживания ваших товаров введите /info ваш персональный '
                                      'номер\nСтрого в формате GX-0000!!!\nИли же можете воспользоваться командой '
                                      '/info_trek ваш трек\nЕсли хотите получать '
                                      'уведомления о вашем товар, то /subscribe GX-0000\nИ /unsubscribe GX-0000 чтобы '
                                      'отписаться',
                                 reply_markup=kb.blank_kb)


# Обрабатываем по Трек-коду
@dp.message_handler(commands='info_trek')
async def info_trek(message: types.Message):
    # RU
    trek = str(message.text[11:])
    if 'ru' in get_lan(message.from_user.id):
        try:
            await message.answer(text='Подождите минутку...')
            product = trek_search_sql(trek)


            """Отправляем результат"""
            await message.answer(text=prepare_data(product))
        except asyncio.exceptions.TimeoutError:
            await info_trek(message)

    # KGZ
    elif 'kgz' in get_lan(message.from_user.id):
        try:
            await message.answer(text='Бир мүнөт күтөө туруңуз...')
            product = trek_search_sql(trek)

            """Отправляем результат"""
            await message.answer(text=prepare_data(product))
        except asyncio.exceptions.TimeoutError:
            await info_trek(message)


# Обрабатываем поиск по GX коду
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    # RU
    if 'ru' in get_lan(message.from_user.id):
        try:
            id = str(message.text[6:])
            await message.answer(text='Подождите минутку...')
            product = gx_search_sql(id)
            result = prepare_data(product)

            """Отправляем результат"""
            if type(result) is list:
                for i in result:
                    await message.answer(text=i)
            else:
                await message.answer(text=result)
        except asyncio.exceptions.TimeoutError:
            await info(message)
    # KGZ
    elif 'kgz' in get_lan(message.from_user.id):
        try:
            id = message.text[6:]
            await message.answer(text='Бир мүнөт күтөө туруңуз...')
            product = gx_search_sql(id)
            result = prepare_data(product)

            """Отправляем результат"""
            if type(result) is list:
                for i in result:
                    await message.answer(text=i)
            else:
                await message.answer(text=result)
        except asyncio.exceptions.TimeoutError:
            await info(message)


# Обрабатываем активацию подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message):
    if 'ru' in get_lan(message.from_user.id):
        if len((str(message.text))) != 18:
            await message.answer('Запрос должен быть формата /subscribe GX-0000')
        gx = message.text[11:]
        if not user_exists(message.from_user.id, gx):
            """Если пользователя нет в базе данных"""
            add_subscriber(message.from_user.id, gx)
            await message.answer('Вы подписались на уведомления!\nЕсли товар придет, вы сразу же об этом узнаете!')
        elif user_exists(message.from_user.id, gx) and not subscriber_status(message.from_user.id):
            """Если пользователь есть в базе данных и неактивен"""
            update_subscription(message.from_user.id, True)
            await message.answer('Вы снова подписались на уведомления!\nЕсли товар придет, вы сразу же об этом узнаете!')
        else:
            """Если пользователь есть в базе данных и активен"""
            await message.answer('Вы уже подписаны!')

    elif 'kgz' in get_lan(message.from_user.id):
        if len((str(message.text))) != 18:
            await message.answer('Катуу форматта болуш керек /subscribe GX-0000')
        gx = message.text[11:]
        if not user_exists(message.from_user.id, gx):
            """Если пользователя нет в базе данных"""
            add_subscriber(message.from_user.id, gx)
            await message.answer('Сиз эскертмелерге жазылдыңыз!\nЭгерде продукт келсе, сиз бул жөнүндө дароо билесиз!')
        elif user_exists(message.from_user.id, gx) and not subscriber_status(message.from_user.id):
            """Если пользователь есть в базе данных и неактивен"""
            update_subscription(message.from_user.id, True)
            await message.answer('Сиз эскертмелерге жазылдыңыз кайта!\nЭгерде продукт келсе, сиз бул жөнүндө дароо '
                                 'билесиз!')
        else:
            """Если пользователь есть в базе данных и активен"""
            await message.answer('Сиз эскертмелерге уже жазылдыңыз!')


# Обрабатываем деактивацию подписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message):
    if 'ru' in get_lan(message.from_user.id):
        if len((str(message.text))) != 20:
            await message.answer('Запрос должен быть формата /unsubscribe GX-0000')
        gx = message.text[13:]
        if user_exists(message.from_user.id, gx) and subscriber_status(message.from_user.id):
            """Если пользователь есть в базе данных и активен"""
            update_subscription(message.from_user.id, False)
            await message.answer('Вы успешно отписались от уведомлений!')
        else:
            """Если пользователя нет в базе данных или он неактивен"""
            await message.answer('Вы и так не подписаны!')

    elif 'kgz' in get_lan(message.from_user.id):
        if len((str(message.text))) != 20:
            await message.answer('Катуу форматта болуш керек /unsubscribe GX-0000')
        gx = message.text[13:]
        if user_exists(message.from_user.id, gx) and subscriber_status(message.from_user.id):
            """Если пользователь есть в базе данных и активен"""
            update_subscription(message.from_user.id, False)
            await message.answer('Эскертмелерди ийгиликтүү жокко чыгардыңыз!')
        else:
            """Если пользователя нет в базе данных или он неактивен"""
            await message.answer('Сиз ансыз деле жазылбайсыз!')


# Добавляем нового админа
@dp.message_handler(commands=['add_admin'])
async def add_admin(message):
    if check_admin(message.from_user.id):
        """Проверка на права админа"""
        if len(message.text) < 11:
            await message.answer('Неподходящий id пользователя!')
        else:
            user_id = message.text[11:]
            if check_admin(user_id):
                """Проверяем есть ли админ в базе данных"""
                await message.answer('Пользователь и так является админом!')
            else:
                """Добавляем админа"""
                create_admin(user_id)
                await message.answer('Вы успешно добавили нового админа!')
    else:
        await message.answer('У вас недостаточно прав!')


# Удаляем админа
@dp.message_handler(commands=['remove_admin'])
async def remove_admin(message):
    if check_admin(message.from_user.id):
        """Проверка на права админа"""
        if len(message.text) < 14:
            await message.answer('Неподходящий id пользователя!')
        else:
            user_id = message.text[14:]
            if check_admin(user_id):
                """Проверяем есть ли админ в базе данных и удаляем его"""
                if str(user_id) == str(message.from_user.id):
                    """Не даем пользователю удалить себя"""
                    await message.answer('Вы не можете удалить себя же!')
                else:
                    delete_admin(user_id)
                    await message.answer('Вы успешно удалили админа')
            else:
                """Отправляем ошибочное сообщение"""
                await message.answer('Пользователь и так не является админом!')
    else:
        await message.answer('У вас недостаточно прав!')


# Обрабатываем отправку новой таблицы
@dp.message_handler(content_types=['document'])
async def get_new_table(message):
    if check_admin(message.from_user.id):
        if 'ru' in get_lan(message.from_user.id):
            file = await bot.get_file(message.document.file_id)
            print('bobobo')
            # upload_table(file)
            # print(file.file_path)q
            # print(file.file_path + "/bot/")
            # await message.document.download(destination_dir="", destination_file="data.xlsx",)
            await bot.download_file(file.file_path, 'data.xlsx')
            upload_table('data.xlsx')
            await message.answer('Вы успешно загрузили новую таблицу!')
        elif 'kgz' in get_lan(message.from_user.id):
            file = await bot.get_file(message.document.file_id)
            await bot.download_file(file.file_path, 'data.xlsx')
            upload_table('data.xlsx')
            await message.answer('Жаңы таблицаны ийгиликтүү жүктөдүңүз!')


# Обрабатываем получение таблицы
@dp.message_handler(commands=['send_sheet'])
async def send_sheet(message):
    if check_admin(message.from_user.id):
        with open('data.xlsx', 'rb') as f:
            file = InputFile(f)
            await message.answer('Подождите минутку...')
            await bot.send_document(chat_id=message.from_user.id, document=file.get_file())


# @dp.message_handler(commands=['info'])
# async def info(message: types.Message):
#     if get_lan(message.from_user.id) == 'ru':
#         id = str(message.text[6:])
#         if len(id) == 7 and id[:3] == 'GX-':
#             """Приводим все возможные виды GX кода"""
#             ex1 = id
#             ex2 = id[3:]
#             ex3 = id[4:]
#             ex4 = id[5:]

#             await message.answer(text='Подождите минутку...')
#             print('bebebe1')
#             info_loop = asyncio.get_event_loop()
#             # info_loop.create_task(clear(1))
#             info_loop.create_task(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             await asyncio.sleep(15)
#             print('bebebe2')
#             # info_loop.run_until_complete(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             # info_loop.close()
#             print('bebebe3')
#             # if dataXlsx(ex1, ex2, ex3, ex4) == 1:
#             #     await message.answer(text='Товаров с таким кодом нет!')
#             # else:
#             with open(f'Ваши_товары_{ex1}.xlsx', 'rb') as file:
#                 await message.answer_document(file)
#         elif len(id) == 4:
#             """Приводим все возможные виды GX кода"""
#             ex1 = 'GX-' + id
#             ex2 = id
#             ex3 = id[1:]
#             ex4 = id[2:]

#             await message.answer(text='Подождите минутку...')
#             print('bebebe1')
#             info_loop = asyncio.get_event_loop()
#             # info_loop.create_task(clear(1))
#             info_loop.create_task(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             await asyncio.sleep(15)
#             print('bebebe2')
#             # info_loop.run_until_complete(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             # info_loop.close()
#             print('bebebe3')
#             # if dataXlsx(ex1, ex2, ex3, ex4) == 1:
#             #     await message.answer(text='Товаров с таким кодом нет!')
#             # else:
#             with open(f'Ваши_товары_{ex1}.xlsx', 'rb') as file:
#                 await message.answer_document(file)
#         else:
#             await message.answer(text='Строго в фортмате GX-0000 или 0000!!!')

#     # KGZ
#     elif get_lan(message.from_user.id) == 'kgz':
#         id = message.text[6:]
#         if len(id) == 7 and id[:3] == 'GX-':
#             """Приводим все возможные виды GX кода"""
#             ex1 = id
#             ex2 = id[3:]
#             ex3 = id[4:]
#             ex4 = id[5:]

#             await message.answer(text='Бир мүнөт күтөө туруңуз...')
#             print('bebebe1')
#             info_loop = asyncio.get_event_loop()
#             # info_loop.create_task(clear(1))
#             info_loop.create_task(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             await asyncio.sleep(15)
#             print('bebebe2')
#             # info_loop.run_until_complete(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             # info_loop.close()
#             print('bebebe3')
#             # if dataXlsx(ex1, ex2, ex3, ex4) == 1:
#             #     await message.answer(text='Мындай коду бар товарлар жок!')
#             # else:
#             with open(f'Ваши_товары_{ex1}.xlsx', 'rb') as file:
#                 await message.answer_document(file)
#         elif len(id) == 4:
#             """Приводим все возможные виды GX кода"""
#             ex1 = 'GX-' + id
#             ex2 = id
#             ex3 = id[1:]
#             ex4 = id[2:]

#             await message.answer(text='Бир мүнөт күтөө туруңуз...')
#             print('bebebe1')
#             info_loop = asyncio.get_event_loop()
#             # info_loop.create_task(clear(1))
#             info_loop.create_task(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             await asyncio.sleep(15)
#             print('bebebe2')
#             # info_loop.run_until_complete(dataXlsx(ex1, ex2, ex3, ex4, 1))
#             # info_loop.close()
#             print('bebebe3')
#             # if dataXlsx(ex1, ex2, ex3, ex4) == 1:
#             #     await message.answer(text='Товаров с таким кодом нет!')
#             # else:
#             with open(f'Ваши_товары_{ex1}.xlsx', 'rb') as file:
#                 await message.answer_document(file)
#         else:
#             await message.answer(text='Катуу форматта болуш керек GX-0000 же 0000!!!')


if __name__ == '__main__':
    while True:
      try:
        executor.start_polling(dp)
      except Exception:
        pass
