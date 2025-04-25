import phonenumbers
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot
from keyboards import main_keyboard, back_command_keboard, payment_keyboard, payment_keyboard1, network2, network1, network3
import re
from phonenumbers import geocoder, carrier, timezone
import asyncio
import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import datetime
import time
from db import Database
import json

from dadata import DadataAsync, Dadata


bot = Bot('7783210062:AAFC_H7lRdIPdcSrdbII_ETa0PY1pcTM25M')
token = 'e06e442308d4e5f6af20defac93ff1cf2683cd40'
secret = '195254f0af3eb4a629fb543a460bf49418ccdedc'
db = Database('database.db')
cost = 1000000
WALLET = 'YOUR CRYPTO WALLET HERE'

dp = Dispatcher(bot, storage=MemoryStorage())
dadata = DadataAsync(token, secret)
dadata_for_inn = Dadata(token)
GROUP_CHAT_ID = -1002192140565
BOT_NICKNAME = 'ultra_parcer_robot'



USER_AGENTS = [
    'geoapiExercises1',
    'geoapiUserAgent2',
    'geoapiUserAgent3',
    'geoapiClient4',
    'geoapiDemoAgent5'
]


company_keyboard2 = ''


class Renting(StatesGroup):
    rent_time = State()






# Перевод подписки в дни
def days_to_seconds(days):
    return days * 24 * 60 * 60


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", 'дней')
        return dt


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    greeting_photo_path = 'fotos/lightning.jpg'
    await message.answer_photo(photo=open(greeting_photo_path, "rb"), caption='Откройте мир возожностей с нами - мы анализируем все, что есть в сети интернет превращая открытые источники в знания для поиска информации\n\n'
                         '<b>Выберите действие:</b>', parse_mode='html', reply_markup=main_keyboard)



    # Проверка подписки на старте и выдача пробного доступа

    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.username)
        db.set_signup(message.from_user.id, 'done')
        user_id = message.from_user.id
        if db.get_sub_status(user_id):
            success_photo_path = 'fotos/success.jpg'
            time_sub = int(time.time() + days_to_seconds(1)) - int(time.time())
            db.set_time_sub(user_id, time_sub)
            await message.answer_photo(photo=open(success_photo_path, "rb"), caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                                                                     f'🎉 <i>Поздравляем</i>', parse_mode='html')
        else:
            success_photo_path = 'fotos/success.jpg'
            time_sub = int(time.time() + days_to_seconds(1))
            db.set_time_sub(user_id, time_sub)
            await message.answer_photo(photo=open(success_photo_path, "rb"),
                                       caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                               f'🎉 <i>Поздравляем</i>', parse_mode='html')
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user.id):
                db.add_user(message.from_user.id, referrer_id)
                db.set_nickname(message.from_user.id, message.from_user.username)
                db.set_signup(message.from_user.id, 'done')
                user_id = message.from_user.id
                if db.get_sub_status(user_id):
                    time_sub = int(time.time() + days_to_seconds(1)) - int(time.time())
                    db.set_time_sub(user_id, time_sub)
                    await message.answer_photo(photo=open(success_photo_path, "rb"),
                                               caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                                       f'🎉 <i>Поздравляем</i>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(1))
                    db.set_time_sub(user_id, time_sub)
                    await message.answer_photo(photo=open(success_photo_path, "rb"),
                                               caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                                       f'🎉 <i>Поздравляем</i>', parse_mode='html')
                try:
                    await bot.send_photo(referrer_id, photo=open(success_photo_path, "rb"),
                                           caption="✅ <b>По вашей ссылке зарегистрировался новый пользователь.</b>\n\n <i>🎉 Вы получили доступ на 10 деней! Поздравляем</i>", parse_mode='html')
                    if db.get_sub_status(referrer_id):
                        time_sub = int(time.time() + days_to_seconds(10)) - int(time.time())
                        db.set_time_sub(referrer_id, time_sub)
                    else:
                        time_sub = int(time.time() + days_to_seconds(10))
                        db.set_time_sub(referrer_id, time_sub)
                except:
                    pass
            else:
                pass
        else:
            pass
    else:
        if db.get_sub_status(message.from_user.id):
            success_photo_path = 'fotos/success.jpg'
            await message.answer_photo(photo=open(success_photo_path, "rb"),
                                       caption=f'✅ <b>Есть доступ к боту</b>', parse_mode='html')
        else:
            error_photo_path = 'fotos/error.jpg'
            await message.answer_photo(photo=open(error_photo_path, "rb"),
                caption=f'🚨 <b>Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!</b>\n\n', reply_markup=payment_keyboard1)





@dp.callback_query_handler(lambda query: True)
async def callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    global current_time_sub
    global cost
    global WALLET
    # REQUEST COMMANDS

    if callback_query.data == 'requests_commands':
        questions_photo_path = 'fotos/questions.jpg'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await callback_query.message.answer_photo(photo=open(questions_photo_path, "rb"), caption='⬇️ ***Примеры команд для ввода:***\n\n'
                                            '📱 `79999999999` - для поиска по номеру телефона\n'
                                            '📨 `elonmusk@spacex.com` - для поиска по Email\n'
                                            '🏘 `москва, сухонская, 11, 89` - найти ***кадастровый номер*** в таком формате!!!\n\n'
                                            '🏛 `/company Сбербанк` - поиск по компании\n'
                                            '📑 `/inn 123456789123` - поиск по ИНН\n',
                                            parse_mode='MARKDOWN', reply_markup=back_command_keboard)

    # BACK TO MENU
    if callback_query.data == 'back_to_menu':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await callback_query.message.answer(
                'Откройте мир возможностей с нами - мы анализируем все, что есть в сети интернет превращая открытые источники в знания для поиска информации\n\n'
                '<b>Выберите действие:</b>', parse_mode='html', reply_markup=main_keyboard)

    # COMPANY SEARCH
    if callback_query.data.startswith('company_'):
        company_name = callback_query.data.replace('company_', '', 1)
        try:
            result = await dadata.suggest("party", company_name)
            write_inf(result, 'users.json')
            useresult = read_inf('users.json')
            for user in useresult:
                kpp = user['data']['kpp']
                inn = user['data']['inn']
                ogrn = user['data']['ogrn']
                address = user['data']['address']['value']
                country_name = user['data']['address']['data']['country']
                main = user['data']['management']['name']
                post_roll = user['data']['management']['post']
                post_roll_date = datetime.datetime.fromtimestamp(user['data']['management']['start_date'] / 1000)
                post_roll_date_ref = post_roll_date.strftime('%Y-%m-%d %H:%M:%S')
                type_of_company = user['data']['type']
                data_ogrn = datetime.datetime.fromtimestamp(user['data']['ogrn_date'] / 1000)
                data_ogrn_ref = data_ogrn.strftime('%Y-%m-%d %H:%M:%S')
                await callback_query.message.answer(f'🛠️ ***Компания:*** {company_name}\n'
                                                    f'├ ***Адрес предприятия:*** `{address}`\n'
                                                    f'├ ***КПП компании:*** `{kpp}`\n'
                                                    f'├ ***ИНН компании:*** `{inn}`\n'
                                                    f'├ ***ОГРН компании:*** `{ogrn}`\n'
                                                    f'└ ***Тип компании:*** `{type_of_company}`\n\n'
                                                    f'👷🏻‍♂️ ***Управленец:*** {main}\n'
                                                    f'🏆 ***Должность:*** {post_roll}\n'
                                                    f'👑 ***Дата назначения управленца:*** {post_roll_date_ref}\n'
                                                    f'📄 ***Дата огрн:*** {data_ogrn_ref}\n'
                                                    f'🌎 ***Страна:*** {country_name}', parse_mode='MARKDOWN')
        except Exception:
            pass

    # VIEW PROFILE
    if callback_query.data == 'my_acc':
        user_nickname = f'👤 Ваш никнейм: <b>{db.get_nickname(callback_query.from_user.id)}</b>'
        user_sub = time_sub_day(db.get_time_sub(callback_query.from_user.id))
        if user_sub == False:
            user_sub = '❌ На данный момент <b>у вас нет доступа</b>'
        user_sub = f'\n🔋 Подписка: <b>{user_sub}</b>'
        await bot.send_message(callback_query.from_user.id, user_nickname + user_sub, parse_mode='html', reply_markup=payment_keyboard1)


    # REFERAL SISTEM
        # ПОПОЛНЕНИЕ КОШЕЛЬКА
    if callback_query.data == 'pay_the_call':
        bank_photo_path = 'fotos/bank.jpg'
        await callback_query.message.answer_photo(photo=open(bank_photo_path, "rb"),
                                                      caption=f'🤖 Наш тариф:\n1 месяц = 5 USDT\n6 месяцев = 25 USDT\n1 год = 55 USDT\n\n<b>❗ Чтобы пополнить доступ нужно пополнить кошелек. Вы можете вводить промокоды от разработчика.</b>\n\n💵 Кошелек: <b>{db.get_user_wallet(callback_query.from_user.id)} USDT</b>\n\n<i>Выберите тариф:</i>',
                                                      reply_markup=payment_keyboard, parse_mode='html')

    if callback_query.data == 'month':
            success_photo_path = 'fotos/success.jpg'
            fail_photo_path = 'fotos/error.jpg'
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 5:
                db.set_user_wallet_take(callback_query.from_user.id, 5)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(30)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=open(success_photo_path, "rb"), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(30))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=open(success_photo_path, "rb"), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html')
            else:
                await callback_query.message.answer_photo(photo=open(fail_photo_path, "rb"),
                                                          caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                                  f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                          parse_mode='html',
                                                          reply_markup=back_command_keboard)

    if callback_query.data == 'halfyear':
            success_photo_path = 'fotos/success.jpg'
            fail_photo_path = 'fotos/error.jpg'
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 25:
                db.set_user_wallet_take(callback_query.from_user.id, 25)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(180)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=open(success_photo_path, "rb"), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(180))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=open(success_photo_path, "rb"), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html')
            else:
                await callback_query.message.answer_photo(photo=open(fail_photo_path, "rb"),
                                                          caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                                  f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                          parse_mode='html', reply_markup=payment_keyboard1)

    if callback_query.data == 'year':
            success_photo_path = 'fotos/success.jpg'
            fail_photo_path = 'fotos/error.jpg'
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 55:
                db.set_user_wallet_take(callback_query.from_user.id, 55)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(365)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=open(success_photo_path, "rb"), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(365))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=open(success_photo_path, "rb"), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html')
            else:
                await callback_query.message.answer_photo(photo=open(fail_photo_path, "rb"),
                                                          caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                                  f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                          parse_mode='html', reply_markup=payment_keyboard1)

    if callback_query.data == 'bye_loot':
            card_photo_path = 'fotos/bank_cards.jpg'
            await callback_query.message.answer_photo(photo=open(card_photo_path, "rb"),
                                                      caption='🤖 <b>Выбери сеть для оплаты USDT:</b>',
                                                      parse_mode='html',
                                                      reply_markup=network1)

    if callback_query.data == 'TON':
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            card_photo_path = 'fotos/bank_cards.jpg'
            NETWORK = 'TON'
            WALLET = 'UQCZWX_JeVoi9ajcpXKAp1F8soOH2YIv6HitZeGUE16gGVfk'
            db.set_wallet(callback_query.from_user.id, 'UQCZWX_JeVoi9ajcpXKAp1F8soOH2YIv6HitZeGUE16gGVfk')
            db.set_network(callback_query.from_user.id, 'TON')
            await state.set_state(Renting.rent_time)
            await callback_query.message.answer_photo(photo=open(card_photo_path, "rb"),
                                                      caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
                                                      parse_mode='html', reply_markup=back_command_keboard)

    if callback_query.data == 'TRC':
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            card_photo_path = 'fotos/bank_cards.jpg'
            NETWORK = 'TRC'
            WALLET = 'TWBv2DH5cpHP8UgRj9wdCcr2rWkJTgGJoo'
            db.set_wallet(callback_query.from_user.id, 'TWBv2DH5cpHP8UgRj9wdCcr2rWkJTgGJoo')
            db.set_network(callback_query.from_user.id, 'TRC')
            await state.set_state(Renting.rent_time)
            await callback_query.message.answer_photo(photo=open(card_photo_path, "rb"),
                                                      caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
                                                      parse_mode='html', reply_markup=back_command_keboard)

    if callback_query.data == 'ERC':
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            card_photo_path = 'fotos/bank_cards.jpg'
            NETWORK = 'ERC'
            WALLET = '0x4B908f33111e968970bD4c5b1f6CE4014ad4F92E'
            db.set_wallet(callback_query.from_user.id, '0x4B908f33111e968970bD4c5b1f6CE4014ad4F92E')
            db.set_network(callback_query.from_user.id, 'ERC')
            await state.set_state(Renting.rent_time)
            await callback_query.message.answer_photo(photo=open(card_photo_path, "rb"),
                                                      caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
                                                      parse_mode='html', reply_markup=back_command_keboard)



    # проверка оплаты и подтверждение
    try:
            action, user_id = callback_query.data.split(':')
            user_id = int(user_id)
            rent = float(db.get_rent(user_id))
            message_photo_path = 'fotos/message.jpg'
            if action == 'success':
                db.set_user_wallet_make(user_id, rent)
                await bot.send_photo(photo=open(message_photo_path, "rb"), chat_id=user_id,
                                     caption=f'✅ <b>Пополнение на кошелек прошло успешно!</b>\n\n'
                                             f'💵 Кошелек: <b>{db.get_user_wallet(user_id)} USDT</b>', parse_mode='html',
                                     reply_markup=back_command_keboard)

            if action == 'invalid':
                error_photo_path = 'fotos/error.jpg'
                await bot.answer_callback_query(callback_query.id)
                await bot.send_photo(photo=open(error_photo_path, "rb"), chat_id=user_id,
                                     caption='❌ <b>Похоже что-то пошло не так. Возможно возникла проблема с обработкой данных.</b>\n\n'
                                             '<i>Если вы уверены, что все данные верны обратитесь в поддержку: @pump_supporting_bot</i>',
                                     parse_mode='html', reply_markup=back_command_keboard)
    except Exception:
        pass

    # if callback_query.data == callback_query.data:
    #     company_name = callback_query.data
    #     try:
    #         result = await dadata.suggest("party", company_name)
    #         write_inf(result, 'users.json')
    #         useresult = read_inf('users.json')
    #         for user in useresult:
    #             kpp = user['data']['kpp']
    #             inn = user['data']['inn']
    #             ogrn = user['data']['ogrn']
    #             address = user['data']['address']['value']
    #             country_name = user['data']['address']['data']['country']
    #             main = user['data']['management']['name']
    #             post_roll = user['data']['management']['post']
    #             post_roll_date = datetime.datetime.fromtimestamp(user['data']['management']['start_date'] / 1000)
    #             post_roll_date_ref = post_roll_date.strftime('%Y-%m-%d %H:%M:%S')
    #             type_of_company = user['data']['type']
    #             data_ogrn = datetime.datetime.fromtimestamp(user['data']['ogrn_date'] / 1000)
    #             data_ogrn_ref = data_ogrn.strftime('%Y-%m-%d %H:%M:%S')
    #             await callback_query.message.answer(f'🛠️ ***Компания:*** {company_name}\n'
    #                                                 f'├ ***Адрес предприятия:*** `{address}`\n'
    #                                                 f'├ ***КПП компании:*** `{kpp}`\n'
    #                                                 f'├ ***ИНН компании:*** `{inn}`\n'
    #                                                 f'├ ***ОГРН компании:*** `{ogrn}`\n'
    #                                                 f'└ ***Тип компании:*** `{type_of_company}`\n\n'
    #                                                 f'👷🏻‍♂️ ***Управленец:*** {main}\n'
    #                                                 f'🏆 ***Должность:*** {post_roll}\n'
    #                                                 f'👑 ***Дата назначения управленца:*** {post_roll_date_ref}\n'
    #                                                 f'📄 ***Дата огрн:*** {data_ogrn_ref}\n'
    #                                                 f'🌎 ***Страна:*** {country_name}', parse_mode='MARKDOWN')
    #     except Exception:
    #         pass




# БЛОК ОПЛАТЫ
def calculate_sum_from_rubs_to_dollars(num):
    return round(num / 90.00, 2)


@dp.message_handler(state=Renting.rent_time)
async def loot_for_wallet(message: types.Message, state: FSMContext):
    global cost, user_count, sum
    bank_photo_path = 'fotos/bank.jpg'
    if message.text.isdigit():
        sum = float(message.text)
        await state.update_data(rent_time=float(message.text))
        user_count = sum
        await state.finish()
        db.set_rent(message.from_user.id, float(message.text))
        await message.answer_photo(photo=open(bank_photo_path, "rb"), caption=f'🤖 ***Переведите сумму ниже на адрес кошелька:***\n\n'
                             f'`{db.get_wallet(message.from_user.id)}`\n\n'
                             f'❗ ***Потом пришлите пришлите скриншот оплаты. В описании под скриншотом нужно вставить хэш транзакции, иначе бот не засчитает оплату. (сеть {db.get_network(message.from_user.id)})***\n\n'
                             f'💵 К оплате: ***{db.get_rent(message.from_user.id)} USDT***', parse_mode='MARKDOWN', reply_markup=back_command_keboard)







# PHONE NUMBER
@dp.message_handler(regexp=r'^(\+?\d{1,3})?[-\s\.]?\(?(\d{1,3})\)?[-\s\.]?(\d{3,4})[-\s\.]?(\d{4})$')
async def phone_number_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ПО НОМЕРУ ТЕЛЕФОНУ ЧЕРЕЗ DADATA API
    answer = message.text
    result = await dadata.clean("phone", answer)
    cont = InlineKeyboardMarkup(row_width=2)
    wh = InlineKeyboardButton("🟢 WhatsApp", url=f"""wa.me/{result["phone"]}""")
    tg = InlineKeyboardButton("🔵 Telegram", url=f"https://t.me/{result['phone']}")
    creator = InlineKeyboardButton("🚀 Тг создателя", url=f"https://t.me/+1A9f6ZFMJBgxMjRi")
    cont.add(wh, tg, creator)
    parsed_number = phonenumbers.parse(answer, None)
    if phonenumbers.is_valid_number(parsed_number) is True:
        await message.answer(f'📱 (Телефон: {result["number"]})\n'
                             f'├ ***Номер:*** `{answer}`\n'
                             f'├ ***Страна:*** `{result["country"]}`\n'
                             f'├ ***Регион \ Город:*** `{result["region"]}, {result["city"]}`\n'
                             f'├ ***Оператор:*** `{carrier.name_for_number(parsed_number, "ru")}\n'
                             f'└ ***Часовой пояс:*** `{result["timezone"]}`\n\n'
                             , parse_mode='MARKDOWN', reply_markup=cont)

    else:
        await message.answer('❗️ Номер не найден')

# EMAIL
@dp.message_handler(regexp=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
async def email_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ПО EMAIL ЧЕРЕЗ DADATA API
    # ПРОВЕКА ДОСТУПА
    if db.get_sub_status(message.from_user.id):
        answer = message.text
        result = await dadata.clean("email", answer)
        if result["qc"] == 0:
            await message.answer(f'📨 ***Email:*** `{result["email"]}`\n'
                                 f'├ ***Домен:*** `{result["domain"]}`\n'
                                 f'├ ***Локальная часть адреса:*** `{result["local"]}`\n'
                                 f'└ ***Класс Email:*** `{result["type"]}`', parse_mode='MARKDOWN')
        else:
            await message.answer('❗️ Email не найден или он не действителен')
    else:
        await message.answer(
            f'🚨 Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!\n\n',
            reply_markup=payment_keyboard1)




# (КАДАСТРОВЫЙ НОМЕР)
@dp.message_handler(lambda message: ',' in message.text)
async def kadaster_number_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ПО УЛИЦЕ ЧЕРЕЗ DADATA API
    # ПРОВЕКА ДОСТУПА
    if db.get_sub_status(message.from_user.id):
        answer = message.text
        parts = [part.strip() for part in answer.split(',')]
        parts = ' '.join(parts)
        result = await dadata.clean("address", answer)
        await message.answer(f'├ ***Адрес:*** `{result["result"]}`\n'
                             f'├ ***Улица:*** `{result["street"]}`\n'
                             f'├ ***Дом:*** `{result["house"]}`\n'
                             f'├ ***Квартира:*** `{result["flat"]}`\n'
                             f'├ ***Индекс:*** `{result["postal_code"]}`\n'
                             f'├ ***Область:*** `{result["region"]}`\n'
                             f'└ ***Кадастровый номер:*** `{result["flat_cadnum"]}`', parse_mode='MARKDOWN')
    else:
        await message.answer(
            f'🚨 Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!\n\n',
            reply_markup=payment_keyboard1)


# COMPANY
@dp.message_handler(commands=['company'])
async def company_handler(message: types.Message):
    global company_keyboard2
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ПО КОМПАНИИ ЧЕРЕЗ DADATA API
    # ПРОВЕРКА ДОСТУПА
    if db.get_sub_status(message.from_user.id):
        try:
            comand_parse = message.text.split(maxsplit=1)
            company_keyboard = InlineKeyboardMarkup(row_width=1)
            answer = comand_parse[1]
            result = await dadata.suggest("party", answer)
            write_inf(result, 'users.json')
            useresult = read_inf('users.json')
            result = [user['value'] for user in useresult]
            for i in result:
                button = InlineKeyboardButton(text=i, callback_data=f'company_{i}')
                company_keyboard.add(button)
            back = InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')
            company_keyboard.add(back)
            company_keyboard2 = company_keyboard
            await message.answer('🆔 Найдены организации. Выберите группу компаний:', reply_markup=company_keyboard)
            print(result)
        except Exception:
            pass
    else:
        await message.answer(
            f'🚨 Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!\n\n',
            reply_markup=payment_keyboard1)


# INN SEARCH
@dp.message_handler(commands=['inn'])
async def inn_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ЧЕРЕЗ ИНН КОМПАНИИ
    if db.get_sub_status(message.from_user.id):
        try:
            inn_parse = message.text.split(maxsplit=1)
            answer = inn_parse[1]
            company_keyboard = InlineKeyboardMarkup(row_width=1)
            result = dadata_for_inn.find_by_id("party", answer)
            write_inf(result, 'users.json')
            useresult = read_inf('users.json')
            result = [user['value'] for user in useresult]
            for i in result:
                button = InlineKeyboardButton(text=i, callback_data=i)
                company_keyboard.add(button)
            back = InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')
            company_keyboard.add(back)
            await message.answer('🆔 Найдены организации. Выберите группу компаний:', reply_markup=company_keyboard)
        except Exception:
            pass
    else:
        await message.answer(
            f'🚨 Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!\n\n',
            reply_markup=payment_keyboard1)








# PAYMENT_PART; TON; TRX; eth;
@dp.message_handler(regexp='^0x[a-fA-F0-9]{64}$', content_types=['photo'])
async def handle_transaction_eth(message: types.Message):
    global succes_or_invalid, user_count
    success_photo_path = 'fotos/success.jpg'
    user_id = message.from_user.id
    succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
        InlineKeyboardButton(text='✅ Успешно', callback_data=f'success:{user_id}'),
        InlineKeyboardButton(text='❌ Не успешно', callback_data=f'invalid:{user_id}')
    )])
    pay_k = succes_or_invalid
    await message.forward(chat_id=GROUP_CHAT_ID)
    await message.answer_photo(photo=open(success_photo_path, "rb"), caption='✅ <b>Отлично! Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                         '<i>Если будут вопросы обращайтесь в поддержку: @your_bot</i>', parse_mode='html', reply_markup=back_command_keboard)
    await bot.send_message(GROUP_CHAT_ID, f'ETH {db.get_rent(message.from_user.id)} USDT', reply_markup=pay_k)


@dp.message_handler(regexp='[a-fA-F0-9]{64}$', content_types=['photo'])
async def handle_transaction_tron(message: types.Message):
    global succes_or_invalid, user_count
    success_photo_path = 'fotos/success.jpg'
    user_id = message.from_user.id
    succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
        InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
        InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
    )])
    pay_k = succes_or_invalid
    await message.forward(chat_id=GROUP_CHAT_ID)
    await message.answer_photo(photo=open(success_photo_path, "rb"),
                               caption='✅ <b>Отлично! Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                                       '<i>Если будут вопросы обращайтесь в поддержку: @your_bot</i>', parse_mode='html', reply_markup=back_command_keboard)
    await bot.send_message(GROUP_CHAT_ID, f'TRX {db.get_rent(message.from_user.id)} USDT', reply_markup=pay_k)


@dp.message_handler(regexp='[a-fA-F0-9]{66}$', content_types=['photo'])
async def handle_transaction_ton(message: types.Message):
    global succes_or_invalid, user_count
    success_photo_path = 'fotos/success.jpg'
    user_id = message.from_user.id
    succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
        InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
        InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
    )])
    pay_k = succes_or_invalid
    await message.forward(chat_id=GROUP_CHAT_ID)
    await message.answer_photo(photo=open(success_photo_path, "rb"),
                               caption='✅ <b>Отлично! Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                                       '<i>Если будут вопросы обращайтесь в поддержку: @your_bot</i>', parse_mode='html', reply_markup=back_command_keboard)
    await bot.send_message(GROUP_CHAT_ID, f'TON {db.get_rent(message.from_user.id)}', reply_markup=pay_k)







# TECHNICAL PART
def write_inf(data, file_name):
    data = json.dumps(data)
    data = json.loads(str(data))

    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_inf(file_name):
    with open(file_name, 'r', encoding="utf-8") as file:
        return json.load(file)

def get_data():
    users = read_inf('users.json')
    for user in users['suggestions']:
        print(user.get('value'))
        with open("users.json", "w") as f:
            pass



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)