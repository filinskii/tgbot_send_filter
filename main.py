# hello
import paramiko
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
import io

#Подключение к SSH
host = "host" # IP Host
port = 22 # Port
transport = paramiko.Transport((host, port))
transport.connect(username='login', password='pass') # Login, password
sftp = paramiko.SFTPClient.from_transport(transport)
#Подключение к боту
bot = Bot(token = 'token')
mybot = Dispatcher(bot)


#Период и путь к файлам
station = "path/your/files"
period_station = "_2022 год (январь-декабрь).pdf"


#Пользователи, которым разрешен доступ
filters_stat = {
    'station_1' : ['telegramID', 'telegramID_2'],
    'station_2' : ['telegramID', 'telegramID_5'],
    'station_3': ['telegramID'],
    'station_4': ['telegramID'],

}

#Список
stations = [f"{name}" for name in ['station_1', 'station_2', 'station_3', 'station_4',]]


#Соединяем название файла на сервере, название файла при отправке, проверку на user_id
mapping_stat_path_filter = {
    filters_stat[0]: ('station_1', f"{filters_stat[0]}.pdf", filters_stat[filters_stat[0]]),
    filters_stat[1]: ('station_1', f"{filters_stat[1]}.pdf", filters_stat[filters_stat[1]]),
    filters_stat[2]: ('station_1', f"{filters_stat[2]}.pdf", filters_stat[filters_stat[2]]),
    filters_stat[3]: ('station_1', f"{filters_stat[3]}.pdf", filters_stat[filters_stat[3]]),
}

#start
@mybot.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    narezMES = InlineKeyboardButton(text='Нарезка МЭС', callback_data='Нарезка МЭС')
    narezDOM = InlineKeyboardButton(text='Доминошки', callback_data='Доминошки')
    markup.add(narezMES, narezDOM)
    await message.reply('Выберите просмотр', reply_markup=markup)
#Кнопочки
choose_data = {
    'Кнопка_1': {
        'text': 'Выберите просмотр',
        'options': {
            'Стационар_МЭС': 'Стационар_МЭС',
            'Профиль_МЭС': 'Профиль_МЭС'
        }
    },
    'Кнопка_2': {
        'text': 'Выберите просмотр',
        'options': {
            'Дети_Профиль_МЭС': 'Дети_Профиль_МЭС',
            'Взрослые_Профиль_МЭС': 'Взрослые_Профиль_МЭС'
        }
    }
}
#Вызов кнопочек
@mybot.callback_query_handler(lambda call: call.data in choose_data)
async def handle_callback(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=4)
    for option in choose_data[call.data]['options']:
        markup.add(InlineKeyboardButton(text=option, callback_data=option))
    await call.message.answer(choose_data[call.data]['text'], reply_markup=markup)

#Вызов кнопок Stations
@mybot.callback_query_handler(text='Stations')
async def menu_index(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=4)
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in filters_stat]
    nazad = InlineKeyboardButton(text='Назад', callback_data='Назад')
    buttons.append(nazad)
    markup.add(*buttons)
    await call.message.answer('Выберите', reply_markup=markup)
#Рассылка файлов
@mybot.callback_query_handler(lambda call: call.data in mapping_stat_path_filter)
async def menu_index(call: types.CallbackQuery):
    if call.from_user.id not in mapping_stat_path_filter[call.data][2]:
        return
    path = station + mapping_stat_path_filter[call.data][0] + period_station
    file = InputFile(io.BytesIO(sftp.open(path, 'rb').read()), filename=mapping_stat_path_filter[call.data][1])
    await call.message.answer_document(document=file)

if __name__ == '__main__':
  executor.start_polling(mybot)

