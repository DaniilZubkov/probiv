import os

import phonenumbers
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram import Bot
from keyboards import main_keyboard, payment_keyboard, payment_keyboard1, network_keyboard, back_command_keyboard
import re
from phonenumbers import geocoder, carrier, timezone
import asyncio
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
import datetime
import time
from db import Database
import json
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder


from dadata import DadataAsync, Dadata


bot = Bot('YOUR BOT TOKEN')
token = 'API DADATA TOKEN'
secret = 'API SECRET KEY'
db = Database('database.db')


dp = Dispatcher(storage=MemoryStorage())
dadata = DadataAsync(token, secret)
dadata_for_inn = Dadata(token)
GROUP_CHAT_ID = 'GROUP CHAT ID'
BOT_NICKNAME = 'YOUR BOT NICKNAME'



USER_AGENTS = [
    'geoapiExercises1',
    'geoapiUserAgent2',
    'geoapiUserAgent3',
    'geoapiClient4',
    'geoapiDemoAgent5'
]


class Renting(StatesGroup):
    rent_time = State()
    send_photo = State()




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


# ВРЕМЕННОЕ ФОТО
async def download_photo(file_id: str, path: str):
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, path)



@dp.message(Command('start'))
async def start_command(message: types.Message):
    # СОЗДАЕМ ТАБЛИЦУ ПЕРЕД СТАРТОМ
    db.create_tables()

    greeting_photo_path = 'fotos/lightning.jpg'
    await message.answer_photo(photo=FSInputFile(greeting_photo_path), caption='Откройте мир возожностей с нами - мы анализируем все, что есть в сети интернет превращая открытые источники в знания для поиска информации\n\n'
                         '<b>Выберите действие:</b>', parse_mode='html', reply_markup=main_keyboard())



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
            await message.answer_photo(photo=FSInputFile(success_photo_path), caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                                                                     f'🎉 <i>Поздравляем</i>', parse_mode='html', reply_markup=back_command_keyboard())
        else:
            success_photo_path = 'fotos/success.jpg'
            time_sub = int(time.time() + days_to_seconds(1))
            db.set_time_sub(user_id, time_sub)
            await message.answer_photo(photo=FSInputFile(success_photo_path),
                                       caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                               f'🎉 <i>Поздравляем</i>', parse_mode='html', reply_markup=back_command_keyboard())
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
                    await message.answer_photo(photo=FSInputFile(success_photo_path),
                                               caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                                       f'🎉 <i>Поздравляем</i>', parse_mode='html', reply_markup=back_command_keyboard())
                else:
                    time_sub = int(time.time() + days_to_seconds(1))
                    db.set_time_sub(user_id, time_sub)
                    await message.answer_photo(photo=FSInputFile(success_photo_path),
                                               caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>\n\n'
                                                       f'🎉 <i>Поздравляем</i>', parse_mode='html', reply_markup=back_command_keyboard())
                try:
                    await bot.send_photo(referrer_id, photo=FSInputFile(success_photo_path),
                                           caption="✅ <b>По вашей ссылке зарегистрировался новый пользователь.</b>\n\n <i>🎉 Вы получили доступ на 10 деней! Поздравляем</i>", parse_mode='html', reply_markup=back_command_keyboard())
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
            await message.answer_photo(photo=FSInputFile(success_photo_path),
                                       caption=f'✅ <b>Есть доступ к боту</b>', parse_mode='html', reply_markup=back_command_keyboard())
        else:
            error_photo_path = 'fotos/error.jpg'
            await message.answer_photo(photo=FSInputFile(error_photo_path),
                caption=f'🚨 <b>Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!</b>\n\n', reply_markup=payment_keyboard1())





@dp.callback_query(lambda F: True)
async def callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    # REQUEST COMMANDS

    if callback_query.data == 'requests_commands':
        questions_photo_path = 'fotos/questions.jpg'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await callback_query.message.answer_photo(photo=FSInputFile(questions_photo_path), caption='⬇️ ***Примеры команд для ввода:***\n\n'
                                            '📱 `+79999999999` - для поиска по номеру телефона\n'
                                            '📨 `elonmusk@spacex.com` - для поиска по Email\n'
                                            '🏘 `москва, сухонская, 11, 89` - найти ***кадастровый номер*** в таком формате!!!\n\n'
                                            '🏛 `/company Сбербанк` - поиск по компании\n'
                                            '📑 `/inn 123456789123` - поиск по ИНН\n',
                                            parse_mode='MARKDOWN', reply_markup=back_command_keyboard())

    # BACK TO MENU
    if callback_query.data == 'back_to_menu':
        greeting_photo_path = 'fotos/lightning.jpg'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await callback_query.message.answer_photo(photo=FSInputFile(greeting_photo_path),
                                   caption='Откройте мир возожностей с нами - мы анализируем все, что есть в сети интернет превращая открытые источники в знания для поиска информации\n\n'
                                           '<b>Выберите действие:</b>', parse_mode='html', reply_markup=main_keyboard())

    # COMPANY SEARCH
    if callback_query.data.startswith('company_'):
        company_name = callback_query.data.replace('company_', '', 1)

        error_photo_path = 'fotos/error.jpg'
        company_photo_path = 'fotos/invite.jpg'
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

                def buttons():
                    builder = InlineKeyboardBuilder()
                    builder.add(
                        InlineKeyboardButton(
                            text="🚀 Тг создателя",
                            url=f"https://t.me/+1A9f6ZFMJBgxMjRi"
                        ),
                        InlineKeyboardButton(
                            text="🔙 Назад",
                            callback_data='back_to_menu'
                        )
                    )
                    builder.adjust(1)
                    return builder.as_markup()

                await callback_query.message.answer_photo(photo=FSInputFile(company_photo_path), caption=f'🛠️ ***Компания:*** {company_name}\n'
                                                    f'├ ***Адрес предприятия:*** `{address}`\n'
                                                    f'├ ***КПП компании:*** `{kpp}`\n'
                                                    f'├ ***ИНН компании:*** `{inn}`\n'
                                                    f'├ ***ОГРН компании:*** `{ogrn}`\n'
                                                    f'└ ***Тип компании:*** `{type_of_company}`\n\n'
                                                    f'👷🏻‍♂️ ***Управленец:*** {main}\n'
                                                    f'🏆 ***Должность:*** {post_roll}\n'
                                                    f'👑 ***Дата назначения управленца:*** {post_roll_date_ref}\n'
                                                    f'📄 ***Дата огрн:*** {data_ogrn_ref}\n'
                                                    f'🌎 ***Страна:*** {country_name}', parse_mode='MARKDOWN', reply_markup=buttons())
        except Exception:
            await callback_query.message.answer_photo(
                photo=FSInputFile(error_photo_path),
                caption=f'❗️ ***Произошла ошибка при обработке компании / комания не найдена:***',
                parse_mode='MARKDOWN',
                reply_markup=back_command_keyboard()
            )


    # VIEW PROFILE
    if callback_query.data == 'my_acc':
        user_sub = time_sub_day(db.get_time_sub(callback_query.from_user.id))
        if user_sub == False:
            user_sub = '❌ ***Отсутствует***'
        user_sub = f'***{user_sub}***'

        profile_photo_path = 'fotos/profile.jpg'
        await callback_query.message.answer_photo(photo=FSInputFile(profile_photo_path), caption=f'👨‍💻 ***Ваш кабинет:***\n'
                                                                                        f'• Ваш никнейм: {callback_query.from_user.first_name}\n'
                                                                                        f'• Ваш ID: {callback_query.message.from_user.id}\n\n'
                                                                                        f'📊 ***Статистика:***\n'
                                                                                        f'↳ 👤 Рефералов: ***{db.get_count_refers(callback_query.from_user.id)}***\n'
                                                                                        f'↳ 🔋 Подписка: ***{user_sub}***\n\n'
                                                                                        f'💳 ***Баланс:***\n'
                                                                                        f'↳ 💰 Кошелек: ***{db.get_user_wallet(callback_query.from_user.id)} USDT***\n\n'
                                                                                        f'👤 ***Реферальная ссылка:***\n'
                                                                                        f' ↳ ___За каждого приглашенного человека в бота вы получите 10 Дней Доступа!___\n\n'
                                                                                        f'🚀 Ваша реферальная ссылка: [Ссылка](https://t.me/{BOT_NICKNAME}?start={callback_query.from_user.id})', parse_mode='MARKDOWN', reply_markup=payment_keyboard1())


    if callback_query.data == 'partners_refs':
        refferal_photo_path = 'fotos/invite.jpg'
        await callback_query.message.answer_photo(photo=FSInputFile(refferal_photo_path),
                                                  caption=f'🧑‍🧑‍🧒 <b>Партнёры</b> — это люди, которые перешли по вашей ссылке и начали пользоваться данным ботом.\n\n'
                                                          f'🤖 <b>За каждого приглашенного человека в бота вы получите 10 Дней доступа!</b>\n\n🚀 <b>Ваша реферальная ссылка:</b> https://t.me/{BOT_NICKNAME}?start={callback_query.from_user.id}\n\n'
                                                          f'👥 <b>Вы пригласили партнеров:</b> {db.get_count_refers(callback_query.from_user.id)}\n\n'
                                                          f'<i>Приводи друзей - зарабатывайте вместе!</i>',
                                                  parse_mode='html', reply_markup=back_command_keyboard())


    # REFERAL SISTEM
    # ПОПОЛНЕНИЕ КОШЕЛЬКА
    if callback_query.data == 'pay_the_call':
        bank_photo_path = 'fotos/bank.jpg'
        await callback_query.message.answer_photo(photo=FSInputFile(bank_photo_path),
                                                      caption=f'🤖 Наш тариф:\n1 месяц = 1 USDT\n6 месяцев = 5 USDT\n1 год = 10 USDT\n\n<b>❗ Чтобы пополнить доступ нужно пополнить кошелек. Вы можете вводить промокоды от разработчика.</b>\n\n💵 Кошелек: <b>{db.get_user_wallet(callback_query.from_user.id)} USDT</b>\n\n<i>Выберите тариф:</i>',
                                                      reply_markup=payment_keyboard(), parse_mode='html')

    if callback_query.data == 'month':
            success_photo_path = 'fotos/success.jpg'
            fail_photo_path = 'fotos/error.jpg'
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 1:
                db.set_user_wallet_take(callback_query.from_user.id, 1)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(30)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
                else:
                    time_sub = int(time.time() + days_to_seconds(30))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
            else:
                await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path),
                                                          caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                                  f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                          parse_mode='html',
                                                          reply_markup=payment_keyboard1())

    if callback_query.data == 'halfyear':
            success_photo_path = 'fotos/success.jpg'
            fail_photo_path = 'fotos/error.jpg'
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 5:
                db.set_user_wallet_take(callback_query.from_user.id, 5)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(180)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
                else:
                    time_sub = int(time.time() + days_to_seconds(180))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
            else:
                await callback_query.message.answer_photo(photo=FSInputFile(fail_photo_path),
                                                          caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                                  f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                          parse_mode='html', reply_markup=payment_keyboard1())

    if callback_query.data == 'year':
            success_photo_path = 'fotos/success.jpg'
            fail_photo_path = 'fotos/error.jpg'
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 10:
                db.set_user_wallet_take(callback_query.from_user.id, 10)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(365)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
                else:
                    time_sub = int(time.time() + days_to_seconds(365))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                         caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
            else:
                await callback_query.message.answer_photo(photo=FSInputFile(fail_photo_path),
                                                          caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                                  f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                          parse_mode='html', reply_markup=payment_keyboard1())

    if callback_query.data == 'bye_loot':
            card_photo_path = 'fotos/bank_cards.jpg'
            await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                      caption='🤖 <b>Выбери сеть для оплаты USDT:</b>',
                                                      parse_mode='html',
                                                      reply_markup=network_keyboard())

    if callback_query.data == 'TON':
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            card_photo_path = 'fotos/bank_cards.jpg'
            db.set_wallet(callback_query.from_user.id, 'UQCZWX_JeVoi9ajcpXKAp1F8soOH2YIv6HitZeGUE16gGVfk')
            db.set_network(callback_query.from_user.id, 'TON')
            await state.set_state(Renting.rent_time)
            await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                      caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
                                                      parse_mode='html', reply_markup=back_command_keyboard())

    if callback_query.data == 'TRC':
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            card_photo_path = 'fotos/bank_cards.jpg'
            db.set_wallet(callback_query.from_user.id, 'TWBv2DH5cpHP8UgRj9wdCcr2rWkJTgGJoo')
            db.set_network(callback_query.from_user.id, 'TRC')
            await state.set_state(Renting.rent_time)
            await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                      caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
                                                      parse_mode='html', reply_markup=back_command_keyboard())

    if callback_query.data == 'ERC':
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            card_photo_path = 'fotos/bank_cards.jpg'
            db.set_wallet(callback_query.from_user.id, '0x4B908f33111e968970bD4c5b1f6CE4014ad4F92E')
            db.set_network(callback_query.from_user.id, 'ERC')
            await state.set_state(Renting.rent_time)
            await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                      caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
                                                      parse_mode='html', reply_markup=back_command_keyboard())



    # проверка оплаты и подтверждение
    try:
            action, user_id = callback_query.data.split(':')
            user_id = int(user_id)
            rent = float(db.get_rent(user_id))
            message_photo_path = 'fotos/message.jpg'
            if action == 'success':
                db.set_user_wallet_make(user_id, rent)
                await bot.send_photo(photo=FSInputFile(message_photo_path), chat_id=user_id,
                                     caption=f'✅ <b>Пополнение на кошелек прошло успешно!</b>\n\n'
                                             f'💵 Кошелек: <b>{db.get_user_wallet(user_id)} USDT</b>', parse_mode='html',
                                     reply_markup=back_command_keyboard())

            if action == 'invalid':
                error_photo_path = 'fotos/error.jpg'
                await bot.answer_callback_query(callback_query.id)
                await bot.send_photo(photo=FSInputFile(error_photo_path), chat_id=user_id,
                                     caption='❌ <b>Похоже что-то пошло не так. Возможно возникла проблема с обработкой данных.</b>\n\n'
                                             '<i>Если вы уверены, что все данные верны обратитесь в поддержку: @pump_supporting_bot</i>',
                                     parse_mode='html', reply_markup=back_command_keyboard())
    except Exception:
        pass




# БЛОК ОПЛАТЫ
def calculate_sum_from_rubs_to_dollars(num):
    return round(num / 90.00, 2)


@dp.message(Renting.rent_time)
async def loot_for_wallet(message: types.Message, state: FSMContext):
    bank_photo_path = 'fotos/bank.jpg'
    if message.text.isdigit():
        await state.update_data(rent_time=float(message.text))
        await state.clear()
        await state.set_state(Renting.send_photo)
        db.set_rent(message.from_user.id, float(message.text))
        await message.answer_photo(photo=FSInputFile(bank_photo_path), caption=f'🤖 ***Переведите сумму ниже на адрес кошелька:***\n\n'
                             f'`{db.get_wallet(message.from_user.id)}`\n\n'
                             f'❗ ***Потом пришлите пришлите скриншот оплаты. В описании под скриншотом нужно вставить хэш транзакции, иначе бот не засчитает оплату. (сеть {db.get_network(message.from_user.id)})***\n\n'
                             f'💵 К оплате: ***{db.get_rent(message.from_user.id)} USDT***', parse_mode='MARKDOWN', reply_markup=back_command_keyboard())



# Остановка state Renting.send_photo
@dp.callback_query(Renting.send_photo)
async def stop_send_photo(callback_query: types.CallbackQuery, state: FSMContext):
    success_photo_path = 'fotos/success.jpg'

    await state.clear()
    await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path),
                                              caption="✅ ***Оплата отменена.*** \n\n"
                                                      "___Нажмите на любую кнопку чтобы продолжить.___",
                                              parse_mode="MARKDOWN", reply_markup=back_command_keyboard())


# PAYMENT_PART; TON; TRX; eth;
@dp.message(F.photo, Renting.send_photo)
async def transaction_handle(message: types.Message, state: FSMContext):
    error_photo_path = 'fotos/error.jpg'

    # ПРОВРКА ХЭША
    try:
        if message.caption is None:
            await message.answer_photo(photo=FSInputFile(error_photo_path),
                                       caption='❗ ***Пожалуйста, вставьте в описание под фото хеш транзакции.***',
                                       parse_mode='MARKDOWN', reply_markup=back_command_keyboard())

        if re.match(r'^0x[a-fA-F0-9]{64}$', message.caption) or re.match(r'^[a-fA-F0-9]{64}$', message.caption) or re.match(r'^[a-fA-F0-9]{66}$', message.caption):
            await state.clear()

            success_photo_path = 'fotos/success.jpg'
            user_id = message.from_user.id
            def succes_or_invalid2():
                builder = InlineKeyboardBuilder()
                builder.add(
                    InlineKeyboardButton(text='✅ Успешно', callback_data=f'success:{user_id}'),
                    InlineKeyboardButton(text='❌ Не успешно', callback_data=f'invalid:{user_id}')
                )
                builder.adjust(2)
                return builder.as_markup()


            # Сохраняем в папку user_photos (временно)
            await download_photo(message.photo[-1].file_id, f"user_photos/{message.photo[-1].file_id}.jpg")


            pay_k = succes_or_invalid2()

            # ОТПРАВКА СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЯ В ГРУППУ
            await message.forward(chat_id=GROUP_CHAT_ID)
            await message.answer_photo(photo=FSInputFile(success_photo_path), caption='✅ <b>Отлично! Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                                     '<i>Если будут вопросы обращайтесь в поддержку: @your_bot</i>', parse_mode='html', reply_markup=back_command_keyboard())
            await bot.send_photo(photo=FSInputFile(f'user_photos/{message.photo[-1].file_id}.jpg'), chat_id=GROUP_CHAT_ID, caption=f'***🔔 Сообщение об оплате:***\n\n NETWORK: ***{db.get_network(message.from_user.id)}***\n PRICE: ***{db.get_rent(message.from_user.id)} USDT***\n HASh: `{message.caption}`', reply_markup=pay_k, parse_mode='MARKDOWN')

            # УДАЛЯЕМ ВРЕМЕННОЕ ФОТО
            os.remove(f'user_photos/{message.photo[-1].file_id}.jpg')
        else:
            await message.answer_photo(photo=FSInputFile(error_photo_path),
                                       caption='❗ ***Пожалуйста, вставьте в описание под фото хеш транзакции.***',
                                       parse_mode='MARKDOWN', reply_markup=back_command_keyboard())
    except Exception:
        await message.answer('ERROR')








# PHONE NUMBER
@dp.message(F.text.regexp(r'^[\+\d\s\-\(\)\.]{1,20}$'))
async def phone_number_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ПО НОМЕРУ ТЕЛЕФОНУ ЧЕРЕЗ DADATA API
    answer = message.text
    person_photo_path = 'fotos/profile.jpg'
    error_photo_path = 'fotos/error.jpg'
    try:
        if answer.isdigit() and len(answer) <= 5:

            await message.answer_photo(photo=FSInputFile(person_photo_path), caption=
                f"📞 ***Экстренный/служебный номер:*** `{answer}`\n\n"
                "⚠️ ___Возможно, это номер экстренной службы (МЧС, полиция, скорая).___",
                parse_mode="MARKDOWN", reply_markup=back_command_keyboard()
            )
            return

        result = await dadata.clean("phone", answer)

        if not result or "phone" not in result:
            await message.answer_photo(photo=FSInputFile(error_photo_path), caption="❗️ ***Не удалось обработать номер***", parse_mode='MARKDOWN', reply_markup=back_command_keyboard())
            return


        def buttons():
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(text="🟢 WhatsApp", url=f"""wa.me/{result["phone"]}"""),
                InlineKeyboardButton(text="🔵 Telegram", url=f"https://t.me/{result['phone']}"),
                InlineKeyboardButton(text="🚀 Тг создателя", url=f"https://t.me/+1A9f6ZFMJBgxMjRi"),
                InlineKeyboardButton(text="🔙 Назад", callback_data='back_to_menu')
            )
            builder.adjust(3, 1)
            return builder.as_markup()


        parsed_number = phonenumbers.parse(answer, None)
        if phonenumbers.is_valid_number(parsed_number) is True:
            await message.answer_photo(photo=FSInputFile(person_photo_path), caption=f'📱 (Телефон: {result["number"]})\n'
                                 f'├ ***Номер:*** `{answer}`\n'
                                 f'├ ***Страна:*** `{result["country"]}`\n'
                                 f'├ ***Регион \ Город:*** `{result["region"]}, {result["city"]}`\n'
                                 f'├ ***Оператор:*** `{carrier.name_for_number(parsed_number, "ru")}`\n'
                                 f'└ ***Часовой пояс:*** `{result["timezone"]}`\n\n'
                                 , parse_mode='MARKDOWN', reply_markup=buttons())

        else:
            await message.answer_photo(photo=FSInputFile(error_photo_path), caption='❗️ Номер не найден', parse_mode='MARKDOWN', reply_markup=back_command_keyboard())
    except Exception:
        await message.answer_photo(photo=FSInputFile(error_photo_path), caption=f'❗️ <b>Произошла ошибка при обработке номера:</b>', parse_mode='html', reply_markup=back_command_keyboard())



# EMAIL
@dp.message(F.text.regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'))
async def email_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ПО EMAIL ЧЕРЕЗ DADATA API
    # ПРОВЕКА ДОСТУПА
    error_photo_path = 'fotos/error.jpg'

    if db.get_sub_status(message.from_user.id):
        answer = message.text
        try:
            result = await dadata.clean("email", answer)

            def buttons():
                builder = InlineKeyboardBuilder()
                builder.add(
                    InlineKeyboardButton(
                        text="🚀 Тг создателя",
                        url=f"https://t.me/+1A9f6ZFMJBgxMjRi"
                    ),
                    InlineKeyboardButton(
                        text="🔙 Назад",
                        callback_data='back_to_menu'
                    )
                )
                return builder.as_markup()

            if result["qc"] == 0:
                await message.answer(f'📨 ***Email:*** `{result["email"]}`\n'
                                     f'├ ***Домен:*** `{result["domain"]}`\n'
                                     f'├ ***Локальная часть адреса:*** `{result["local"]}`\n'
                                     f'└ ***Класс Email:*** `{result["type"]}`', parse_mode='MARKDOWN', reply_markup=buttons())
            else:
                await message.answer_photo(photo=FSInputFile(error_photo_path), caption='❗️ ***Email не найден или он не действителен***', parse_mode='MARKDOWN', reply_markup=back_command_keyboard())

        except Exception:
            await message.answer_photo(FSInputFile(error_photo_path),
                                       caption=f'❗️ ***Произошла ошибка при обработке email:***',
                                       parse_mode='MARKDOWN', reply_markup=back_command_keyboard())
    else:
        await message.answer_photo(photo=FSInputFile(error_photo_path), caption=
            f'🚨 ***Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!***', parse_mode='MARKDOWN',
            reply_markup=payment_keyboard1())





# (КАДАСТРОВЫЙ НОМЕР)
@dp.message(lambda message: ',' in message.text)
async def kadaster_number_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ПО УЛИЦЕ ЧЕРЕЗ DADATA API
    # ПРОВЕКА ДОСТУПА
    error_photo_path = 'fotos/error.jpg'

    if db.get_sub_status(message.from_user.id):
        answer = message.text
        try:

            def buttons():
                builder = InlineKeyboardBuilder()
                builder.add(
                    InlineKeyboardButton(
                        text="🚀 Тг создателя",
                        url=f"https://t.me/+1A9f6ZFMJBgxMjRi"
                    ),
                    InlineKeyboardButton(
                        text="🔙 Назад",
                        callback_data='back_to_menu'
                    )
                )
                return builder.as_markup()


            parts = [part.strip() for part in answer.split(',')]
            parts = ' '.join(parts)
            result = await dadata.clean("address", answer)
            await message.answer(f'├ ***Адрес:*** `{result["result"]}`\n'
                                 f'├ ***Улица:*** `{result["street"]}`\n'
                                 f'├ ***Дом:*** `{result["house"]}`\n'
                                 f'├ ***Квартира:*** `{result["flat"]}`\n'
                                 f'├ ***Индекс:*** `{result["postal_code"]}`\n'
                                 f'├ ***Область:*** `{result["region"]}`\n'
                                 f'└ ***Кадастровый номер:*** `{result["flat_cadnum"]}`', parse_mode='MARKDOWN', reply_markup=buttons())
        except Exception:
            await message.answer_photo(FSInputFile(error_photo_path),
                                       caption=f'❗️ ***Произошла ошибка при обработке адреса:***',
                                       parse_mode='MARKDOWN', reply_markup=back_command_keyboard())

    else:
        await message.answer_photo(photo=FSInputFile(error_photo_path), caption=
        f'🚨 ***Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!***', parse_mode='MARKDOWN',
                                   reply_markup=payment_keyboard1())


# COMPANY
@dp.message(Command('company'))
async def company_handler(message: types.Message):
    error_photo_path = 'fotos/error.jpg'
    message_photo_path = 'fotos/message.jpg'

    if not db.get_sub_status(message.from_user.id):
        await message.answer_photo(photo=FSInputFile(error_photo_path), caption=
                f'🚨 ***Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!***', parse_mode='MARKDOWN',
                                           reply_markup=payment_keyboard1())
        return

    # Проверка, есть ли аргумент после /company
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.answer_photo(photo=FSInputFile(error_photo_path), caption="❗️ ***Укажите название компании после команды*** /company", parse_mode='MARKDOWN', reply_markup=back_command_keyboard())
        return

    try:
        company_name = command_parts[1]
        result = await dadata.suggest("party", company_name)
        companies = [item['value'] for item in result]

        company_keyboard = InlineKeyboardBuilder()
        for company in companies:
            short_company = company[:10]
            company_keyboard.add(InlineKeyboardButton(
                text=company,
                callback_data=f'company_{short_company}'
            ))
        company_keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'))
        company_keyboard.adjust(1)

        await message.answer_photo(
                photo=FSInputFile(message_photo_path),
                caption='🆔 Найдены организации. Выберите группу компаний:',
                reply_markup=company_keyboard.as_markup(),
            )

    except Exception:
        await message.answer_photo(
                photo=FSInputFile(error_photo_path),
                caption=f'❗️ ***Произошла ошибка при обработке компании:***',
                parse_mode='MARKDOWN',
                reply_markup=back_command_keyboard()
            )




# INN SEARCH
@dp.message(Command('inn'))
async def inn_handler(message: types.Message):
    # ПОЛУЧЕНИЕ ИНФОРМАЦИИ ЧЕРЕЗ ИНН КОМПАНИИ

    error_photo_path = 'fotos/error.jpg'
    message_photo_path = 'fotos/message.jpg'
    if db.get_sub_status(message.from_user.id):
        try:
            inn_parse = message.text.split(maxsplit=1)
            answer = inn_parse[1]
            company_keyboard = InlineKeyboardBuilder()
            result = dadata_for_inn.find_by_id("party", answer)
            write_inf(result, 'users.json')
            useresult = read_inf('users.json')
            result = [user['value'] for user in useresult]

            for i in result:
                short_company = i[:10]
                button = InlineKeyboardButton(text=i, callback_data=f'company_{short_company}')
                company_keyboard.add(button)

            back = InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')
            company_keyboard.add(back)
            company_keyboard.adjust(1)
            await message.answer_photo(photo=FSInputFile(message_photo_path), caption='🆔 Найдены организации. Выберите группу компаний:', reply_markup=company_keyboard.as_markup())

        except Exception:
            await message.answer_photo(
                photo=FSInputFile(error_photo_path),
                caption=f'❗️ ***Произошла ошибка при обработке компании/инн:***',
                parse_mode='MARKDOWN',
                reply_markup=back_command_keyboard()
            )
    else:
        await message.answer_photo(photo=FSInputFile(error_photo_path), caption=
        f'🚨 ***Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!***', parse_mode='MARKDOWN',
                                   reply_markup=payment_keyboard1())






# TECHNICAL PART (JSON)
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



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


    # dp.start_polling(bot, skip_updates=True)
