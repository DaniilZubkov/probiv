from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Главная клавиатура
def main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='🔍 Показать команды для поиска',
            callback_data='requests_commands'
        ),
        InlineKeyboardButton(
            text='👤 Мой аккаунт',
            callback_data='my_acc'
        ),
        InlineKeyboardButton(
            text='🤝 Партнерам',
            callback_data='partners_refs'
        )
    )
    builder.adjust(1, 2)
    return builder.as_markup()


# Клавиатура "Назад"
def back_command_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    return builder.as_markup()

# Клавиатура оплаты 1
def payment_keyboard1():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='💳 Оплатить доступ',
            callback_data='pay_the_call'
        ),
        InlineKeyboardButton(
            text='💰 Пополнить Кошелек',
            callback_data='bye_loot'
        ),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(2, 1)
    return builder.as_markup()

# Клавиатура выбора тарифов
def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='💳 1 месяц',
            callback_data='month'
        ),
        InlineKeyboardButton(
            text='💳 6 месяцев',
            callback_data='halfyear'
        ),
        InlineKeyboardButton(
            text='💳 1 год',
            callback_data='year'
        ),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(3, 1)  # Три кнопки в ряд, затем одна
    return builder.as_markup()

# Клавиатура выбора сети
def network_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='TON',
            callback_data='TON'
        ),
        InlineKeyboardButton(
            text='TRC20',
            callback_data='TRC'
        ),
        InlineKeyboardButton(
            text='ERC20',
            callback_data='ERC'
        ),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(3, 1)
    return builder.as_markup()