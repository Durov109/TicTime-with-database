import PySimpleGUI as sg
import time
from datetime import date
import Class_time as DB

#---------------Определяем месяц и год---------------
dict_month = {1:'Январь', 2:'Февраль', 3:'Март', 4:'Апрель', 5:'Май', 6:'Июнь', 7:'Июль', 8:'Август', 9:'Сентябрь', 10:'Октябрь', 11:'Ноябрь', 12:'Декабрь'}
today = date.today() 
now_year = today.year
now_month = dict_month[today.month]
print(now_year)
print(now_month)
# ---------------------------------------------------

time.sleep(0.6)

def time_as_int():
    return int(round(time.time() * 100))

# ----------------  Создаем графическое окно  ----------------
# что будет внутри окна
# первым описываем кнопку и сразу указываем размер шрифта
layout = [[sg.Button('Старт', enable_events=True, key='-START-STOP-', font='Helvetica 16')],
        # затем делаем текст
        [sg.Text('Время:', size=(25, 1), key='-text_1-', font='Helvetica 16')],
        #[sg.Text('Всего:', size=(25, 1), key='-text_2-', font='Helvetica 16')],
        [sg.Text('Общее время:', size=(25, 1), key='-text_3-', font='Helvetica 16')]]

# рисуем окно
window = sg.Window('Таймер', layout, size=(750,160))

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

#-----------------Переменная для вывода в окно (Всего:)---------------------
out_time = None

if DB.operation.views_total_time() == (None,):
    out_time = 'Нету данных'
else:
    # out_time = DB.operation.views_total_time()
    for i in DB.operation.views_total_time():
        out_time = i
#---------------------------------------------------------------------------

while True:
    # --------- Чтение и обновление окна --------
    if not paused:
        #Обновление значений каждые 10 милисекунд
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time

    else:
        event, values = window.read()   
    
    # --------- Выполнение операций кнопками --------
    if event in (sg.WIN_CLOSED, 'Exit'):
        DB.operation.insert(('{:02d}:{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 3600,(current_time // 100) // 60 % 60,(current_time // 100) % 60, current_time % 100)), now_month, now_year)
        break
    
    elif event == '-START-STOP-':
        paused = not paused

        if paused==True:
            paused_time = time_as_int()
            print(f"Время: {'{:02d}:{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 3600,(current_time // 100) // 60 % 60,(current_time // 100) % 60, current_time % 100)}")

        else:
            start_time = start_time + time_as_int() - paused_time

        # Обновление старта и стопа
        window['-START-STOP-'].update('Старт' if paused else 'Стоп')

    # --------- Вывод времени на дисплей --------
    window['-text_1-'].update(f"Время: {'{:02d}:{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 3600,(current_time // 100) // 60 % 60,(current_time // 100) % 60, current_time % 100)}")
    window['-text_3-'].update(f"Общее время: {out_time}")


window.close()

