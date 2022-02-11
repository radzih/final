from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

question_callback = CallbackData("answer", "who_wrote", "pk")


async def make_support_kb(num_quest: int, total_quest: int, user_id, pk: int):
    show_quest_kb = InlineKeyboardMarkup()
    if num_quest == 1:
        if total_quest == 2:
            show_quest_kb.add(InlineKeyboardButton(text='Следующее', callback_data='next'))
    elif num_quest == total_quest:
        show_quest_kb.add(InlineKeyboardButton(text='Предыдущее', callback_data='previous'))
    else:
        show_quest_kb.add(InlineKeyboardButton(text='Предыдущее', callback_data='previous'),
                          InlineKeyboardButton(text='Следующее', callback_data='next'))
    show_quest_kb.add(
        InlineKeyboardButton(text='Ответить', callback_data=question_callback.new(who_wrote=user_id, pk=pk)),
        InlineKeyboardButton(text='Меню', callback_data='back_to_menu'))
    return show_quest_kb


no_questions_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Меню', callback_data='back_to_menu')
        ]
    ]
)
back_to_support_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад у вопросам', callback_data='back_to_support')
        ]
    ]
)

confirm_sending_quest_kb = InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text='Отправить', callback_data='send'),
                                     InlineKeyboardButton(text='Отмена', callback_data='back_to_menu')
                                 ]

                             ]
                         )

confirm_sending_answer_kb = InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text='Отправить', callback_data='send'),
                                     InlineKeyboardButton(text='Отмена', callback_data='back_to_support')
                                 ]

                             ]
)