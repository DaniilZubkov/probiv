from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔍 Показать команды для поиска', callback_data='requests_commands')],
    [InlineKeyboardButton(text='👤 Мой аккаунт', callback_data='my_acc'), InlineKeyboardButton(text='🤝 Партнерам', callback_data='partners_refs')],
])

back_command_keboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')]
])



# ADD BUTTONS FOR PAY-KEYBOARD1
payment_keyboard1 = InlineKeyboardMarkup(row_width=2)

buttons_for_keyboard1 = [
    InlineKeyboardButton(text='💳 Оплатить доступ', callback_data='pay_the_call'),
    InlineKeyboardButton(text='💰 Пополнить Кошелек', callback_data='bye_loot'),
    InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')

]

payment_keyboard1.add(*buttons_for_keyboard1)




# ADD BUTTONS FOR PAY-DATES
payment_buttons = [
    InlineKeyboardButton(text='💳 1 месяц', callback_data='month'),
    InlineKeyboardButton(text='💳 6 месяцев', callback_data='halfyear'),
    InlineKeyboardButton(text='💳 1 год', callback_data='year'),
    InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')
]

payment_keyboard = InlineKeyboardMarkup(row_width=3)

payment_keyboard.add(*payment_buttons)



# ADD BUTTONS FOR NETWORK 1
network1 = InlineKeyboardMarkup(row_width=3)

network1_buttons = [
    InlineKeyboardButton(text='TON', callback_data='TON'),
    InlineKeyboardButton(text='TRC20', callback_data='TRC'),
    InlineKeyboardButton(text='ERC20', callback_data='ERC'),
    InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')
]

network1.add(*network1_buttons)


# network2 = InlineKeyboardMarkup(inline_keyboard=[(
#     InlineKeyboardButton(text='TON', callback_data='TON2'),
#     InlineKeyboardButton(text='TRC20', callback_data='TRC2'),
#     InlineKeyboardButton(text='ERC20', callback_data='ERC2')
# )])
#
#
# network3 = InlineKeyboardMarkup(inline_keyboard=[(
#     InlineKeyboardButton(text='TON', callback_data='TON3'),
#     InlineKeyboardButton(text='TRC20', callback_data='TRC3'),
#     InlineKeyboardButton(text='ERC20', callback_data='ERC3')
# )])