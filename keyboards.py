from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔍 Показать команды для поиска', callback_data='requests_commands')],
    [InlineKeyboardButton(text='👤 Мой аккаунт', callback_data='my_acc'), InlineKeyboardButton(text='🤝 Партнерам', callback_data='partners_refs')],
])

back_command_keboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')]
])

payment_keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💳 Оплатить доступ', callback_data='pay_the_call')]
])



payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[(
   InlineKeyboardButton(text='💳1 месяц', callback_data='month'),
    InlineKeyboardButton(text='💳6 месяцев', callback_data='halfyear'),
    InlineKeyboardButton(text='💳1 год', callback_data='year')
)], row_width=1)


network1 = InlineKeyboardMarkup(inline_keyboard=[(
    InlineKeyboardButton(text='TON', callback_data='TON1'),
    InlineKeyboardButton(text='TRC20', callback_data='TRC1'),
    InlineKeyboardButton(text='ERC20', callback_data='ERC1')
)])

network2 = InlineKeyboardMarkup(inline_keyboard=[(
    InlineKeyboardButton(text='TON', callback_data='TON2'),
    InlineKeyboardButton(text='TRC20', callback_data='TRC2'),
    InlineKeyboardButton(text='ERC20', callback_data='ERC2')
)])


network3 = InlineKeyboardMarkup(inline_keyboard=[(
    InlineKeyboardButton(text='TON', callback_data='TON3'),
    InlineKeyboardButton(text='TRC20', callback_data='TRC3'),
    InlineKeyboardButton(text='ERC20', callback_data='ERC3')
)])