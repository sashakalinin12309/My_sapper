# Импортируем модули
import tkinter as tk
from functools import partial
from time import time

# Импортируем созданные модули
import my_modules.interface as interface
import my_modules.minefield as minefield
import my_modules.function_restart as function_restart
from my_modules.command_for_cells import counter_flags, process_timer
from my_modules.menu import create_menu, change_the_size
from my_modules.work_with_file import information_in_Information

# Узнаем все те цвета, которые были применены к окну и его элементам 
# перед выходом.
information_about_game: dict = information_in_Information()
    
bg_color = information_about_game["Цвет_окна"]
field_color = information_about_game["Цвет_поля"]
cell_color = information_about_game["Цвет_ячейки"]
    
# Специальная команда, которая сможет прервать основной цикл приложения.
def stop_running_process() -> None:

    """
    Останавливает цикл приложения, изменяя переменную running.
    """
    global running
    running = False

size = 9  # Начальный размер игрового поля.

window = interface.create_root(bg_color)  # Главное окно приложения.
change_the_size(window, size)  # Изменение основоного окна под размеры 9Х9.

# Словарь с изображениями флажков.
images_flags = {
    "aqua": tk.PhotoImage(file="image//for_use_in_game//flags//aqua_flags.png"), 
    "blue": tk.PhotoImage(file="image//for_use_in_game//flags//blue_flags.png"),
    "green": tk.PhotoImage(file="image//for_use_in_game//flags//green_flags.png"),
    "orange": tk.PhotoImage(file="image//for_use_in_game//flags//orange_flags.png"),
    "pink": tk.PhotoImage(file="image//for_use_in_game//flags//pink_flags.png"),
    "violet": tk.PhotoImage(file="image//for_use_in_game//flags//violet_flags.png"),
    "yellow": tk.PhotoImage(file="image//for_use_in_game//flags//yellow_flags.png"),
    "red": tk.PhotoImage(file="image//for_use_in_game//flags//red_flags.png")
}

# Словарь с изображениями цветов в виде кружков.
interface_colors = {
    'red': tk.PhotoImage(file='image//for_use_in_game//interface_colors//red_color.png'), 
    'orange': tk.PhotoImage(file='image//for_use_in_game//interface_colors//orange_color.png'), 
    'yellow': tk.PhotoImage(file='image//for_use_in_game//interface_colors//yellow_color.png'), 
    'lightgreen': tk.PhotoImage(file='image//for_use_in_game//interface_colors//lightgreen_color.png'), 
    'green': tk.PhotoImage(file='image//for_use_in_game//interface_colors//green_color.png'), 
    'aqua': tk.PhotoImage(file='image//for_use_in_game//interface_colors//aqua_color.png'),  
    'blue': tk.PhotoImage(file='image//for_use_in_game//interface_colors//blue_color.png'), 
    'violet': tk.PhotoImage(file='image//for_use_in_game//interface_colors//violet_color.png'), 
    'darkviolet': tk.PhotoImage(file='image//for_use_in_game//interface_colors//darkviolet_color.png'), 
    'pink': tk.PhotoImage(file='image//for_use_in_game//interface_colors//pink_color.png'),
    'lightgrey': tk.PhotoImage(file='image//for_use_in_game//interface_colors//lightgrey_color.png'),
    'grey': tk.PhotoImage(file='image//for_use_in_game//interface_colors//grey_color.png'),
    'white': tk.PhotoImage(file='image//for_use_in_game//interface_colors//white_color.png'),
    "random": tk.PhotoImage(file='image//for_use_in_game//interface_colors//random_color.png')
}

# Создадим изображение монеты для использования его в текстовом виджете.
money_currency = tk.PhotoImage(file='image//for_use_in_game//sapper`s_currency.png')
money_currency = money_currency.subsample(12, 12)

matrix = minefield.create_minefield(size)  # Создадим матрицу, значения которой будут лежать в основе игрового поля.
    
# Создадим текстовый виджет, показывающий, сколько у пользователя монет.
money = tk.Label(text=f"{information_about_game["Монеты"]}", font="Arial 14", image=money_currency, compound=tk.LEFT, bg=bg_color)
money.pack(anchor=tk.NE)

# Создадим кнопку, текст которой будет отображать значение таймера.
# По сути это - кнопка-таймер.
btn_timer = tk.Button(window, text=0, font="TkDefaultFont", bg="black", fg="red", width=10, activebackground="black", activeforeground="red")
btn_timer.place(x=25, y=50)

# Создадим кнопку, текст которой будет отображать кол-во оставшихся флажков.
btn_flags = tk.Button(text=counter_flags(size), font="TkDefaultFont", bg="black", fg="red", width=10, activebackground="black", activeforeground="red")
btn_flags.place(x=195, y=50)

# Почему я использовал кнопки, а не текстовые виджеты?
# Просто захотелось! Хотелось бы, чтобы при нажатии они прожимались.

# Создаем игровое поле с ячейками, среди которых надо будет искать бомбы.
field = interface.create_field(field_color, cell_color, money, matrix, btn_flags, btn_timer)
field.place(x=25, y=100)

# Создаем специальную кнопку-рестарт, которая отвечает за перезапуск игры.
interface.restart(window, partial(function_restart.restart_game, window, btn_flags, btn_timer, money))

# Создаем меню, в котором пользователь может выбрать разные опции:
# - смена режимов;
# - возможность узнать рекорд в определенном режиме;
# - выбирать цвета доля окна, поля, ячеек, флажков и создавать коллекции.
game_menu = create_menu(window, money, btn_flags, btn_timer, images_flags, interface_colors)
window["menu"] = game_menu

running = True  # Переменная, отвечающая за основной цикл приложения.

# Основной цикл так называется, т. к. он ждет момента, когда пользователь
# нажмет на одну из ячеек. Если это случится, то цикл запустит таймер,
# что делает игру увлекательной - соревнование в прохождении на время.

# При выключении спрашиваем: "А точно ли хотите выйти?", 
# и если ответ положительный, то завершаем основной цикл приложения,
# установив running = False (иначе программа не завершится), а затем и
# окно закрываем.
window.protocol("WM_DELETE_WINDOW", partial(interface.close_root, window, stop_running_process))

# А вот и основной цикл приложения.
while running:

    # Конструкция исключения нужна в том случае, если пользователь 
    # выйдет из приложения во время активной игры.
    try:
        process_timer(btn_timer)  # Запуск таймера
    except tk.TclError:  
        ...
        # Объяснение ошибки:
        # когда игрок выключает игру активной, то функция таймера работает,
        # и не видит кнопку таймера, из-за чего и возращется ошибка.  

    btn_timer.update()  # Обновляем кнопку-таймер, т. к. изменяем её текст.

