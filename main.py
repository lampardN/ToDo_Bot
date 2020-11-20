import telebot
from db_controller import db_controller
from random import choice


TOKEN = "895097429:AAHa1dYMVgZeHUC4zgZdgDco6Mk2nOla1Rk"

bot = telebot.TeleBot(TOKEN, parse_mode=None)

add_btn = telebot.types.InlineKeyboardButton('👩🏿‍🦽Добавить запись👩🏿‍🦽', callback_data='add')
chg_text_btn = telebot.types.InlineKeyboardButton('🛠Изменить текст записи🛠', callback_data='text')
chg_status_btn = telebot.types.InlineKeyboardButton('🛠Изменить статус записи🛠', callback_data='status')
del_btn = telebot.types.InlineKeyboardButton('🙉Удалить запись🙉', callback_data='del')

markup = telebot.types.InlineKeyboardMarkup(row_width=1)
markup.add(add_btn)

control_btn = telebot.types.InlineKeyboardMarkup(row_width=1)
control_btn.add(add_btn, chg_text_btn, chg_status_btn, del_btn)

user_dict = {}


@bot.message_handler(commands=['start'])
def start(chat_id):
    GIF = open('start.gif', 'rb')
    bot.send_document(chat_id.chat.id, GIF)
    show(chat_id)


def Del(chat_id):
    bot.send_message(chat_id.chat.id, "Сообщение под каким номером вы желаете удалить?")
    bot.register_next_step_handler_by_chat_id(chat_id.chat.id, Del_step2)


def Del_step2(chat_id):
    db_controller().DelItem(chat_id)
    GIF = open(choice(['terminator.gif', 'pepa.gif', 'tomato.gif', 'tenor.gif', 'del.gif', 'o.gif']), 'rb')
    bot.send_document(chat_id.chat.id, GIF)
    show(chat_id)


def ChangeStatus(chat_id):
    bot.send_message(chat_id.chat.id, "Статус сообщения под каким номером вы желаете изменить?")
    bot.register_next_step_handler_by_chat_id(chat_id.chat.id, ChangeStatus_step2)


def ChangeStatus_step2(chat_id):
    db_controller().ChangeStatus(chat_id)
    GIF = open(choice(['patric.gif', 'mussolini.gif']), 'rb')
    bot.send_document(chat_id.chat.id, GIF)
    show(chat_id)


@bot.message_handler(commands=['show'])
def show(chat_id):
    global control_btn
    message = db_controller().showAll(chat_id.from_user.id)
    if message != '':
        bot.send_message(chat_id.chat.id, message, reply_markup=control_btn)
    else:
        bot.send_message(chat_id.chat.id, 'Записей нет', reply_markup=control_btn)


def add_command(chat_id):
    bot.send_message(chat_id.chat.id, 'Введите текст, который хотите запомнить')
    bot.register_next_step_handler_by_chat_id(chat_id.chat.id, add_command_step2)


def add_command_step2(chat_id):
    db_controller().addNote(chat_id.chat.id, chat_id.text, 'active')
    s = chat_id.text
    if s.lower() == 'jesus':
        GIF = open('jesus.gif', 'rb')
    else:
        GIF = open(choice(['printing.gif']), 'rb')
    bot.send_document(chat_id.chat.id, GIF)
    show(chat_id)


def chg_text(chat_id):
    bot.send_message(chat_id.chat.id, 'Запись под каким номером желаете изменить?')
    bot.register_next_step_handler_by_chat_id(chat_id.chat.id, chg_text_step2)


def chg_text_step2(chat_id):
    user_dict[chat_id.chat.id] = chat_id.text
    bot.send_message(chat_id.chat.id, 'Введите новый текст')
    bot.register_next_step_handler_by_chat_id(chat_id.chat.id, chg_text_step3)


def chg_text_step3(chat_id):
    db_controller().ChangeText(user_dict[chat_id.chat.id], chat_id.text, chat_id.chat.id)
    show(chat_id)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'add':
        add_command(call.message)
    elif call.data == 'del':
        Del(call.message)
    elif call.data == 'text':
        chg_text(call.message)
    elif call.data == 'status':
        ChangeStatus(call.message)


@bot.message_handler(commands=['gif'])
def gif(chat_id):
    GIF = open('patric.gif', 'rb')
    bot.send_document(chat_id.chat.id, GIF)


bot.polling()
