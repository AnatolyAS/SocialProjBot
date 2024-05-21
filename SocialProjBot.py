import telebot;
from telebot import types
bot = telebot.TeleBot('6943923153:AAH6C2qAacYQdreF6zP2wy5WL5_uvjtE68s');
import telebot
from telebot import types


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую вас")
    show_main_menu(message)

def show_main_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_order = types.InlineKeyboardButton(text='Сделать заказ', callback_data='order')
    key_histogram = types.InlineKeyboardButton(text='Гистограммы', callback_data='histogram')
    keyboard.add(key_order, key_histogram)
    bot.send_message(message.chat.id, 'Чем могу помочь?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'order')
def send_order_menu(call):
    keyboard = types.InlineKeyboardMarkup()
    projects = {
        'Учебные программы для детей': '1',
        'Экологические инициативы': '2',
        'Помощь местным сообществам': '3',
        'Технологические проекты': '4',
        'Культурные и художественные мероприятия': '5',
        'Спортивные программы': '6'
    }
    for project, code in projects.items():
        key_project = types.InlineKeyboardButton(text=project, callback_data=code)
        keyboard.add(key_project)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(call.message.chat.id, 'Какой проект вам подходит?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3', '4', '5', '6'])
def project_callback(call):
    project_id = call.data
    if project_id == '1':
        handle_project_1(call.message)
    elif project_id == '2':
        handle_project_2(call.message)
    elif project_id == '3':
        handle_project_3(call.message)
    elif project_id == '4':
        handle_project_4(call.message)
    elif project_id == '5':
        handle_project_5(call.message)
    elif project_id == '6':
        handle_project_6(call.message)

# Добавьте функции-обработчики для каждого проекта

def handle_project_1(message):
    bot.send_message(message.chat.id, 'Вы выбрали Учебные программы для детей')

def handle_project_2(message):
    bot.send_message(message.chat.id, 'Вы выбрали Экологические инициативы')

def handle_project_3(message):
    bot.send_message(message.chat.id, 'Вы выбрали Помощь местным сообществам')

def handle_project_4(message):
    bot.send_message(message.chat.id, 'Вы выбрали Технологические проекты')

def handle_project_5(message):
    bot.send_message(message.chat.id, 'Вы выбрали Культурные и художественные мероприятия')

def handle_project_6(message):
    bot.send_message(message.chat.id, 'Вы выбрали Спортивные программы')

bot.polling(none_stop=True, interval=0)