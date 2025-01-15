# Импортируем все нужные нам модули.
import tkinter as tk
from tkinter import messagebox
from functools import partial
from random import choice
import shutil

import my_modules.command_for_cells as command_for_cells

# А дальше идут функции.

def create_root(color_for_root) -> tk.Tk:

    """
    Создание главного окна приложения

    Параметры:
        color_for_root - цвет для будущего окна

    Возращает:
        окно c такими параметрами:
        - размер 300х400;
        - неизменяемое;
        - название 'Сапёр';
        - специальной иконкой;
        - цвета color_for_root.
    """
    
    root = tk.Tk()  # Создаем главное окно.
    root.geometry('300x400')  # Определяем его размер.
    root.title("Сапёр")  # Даем ему название.
    root.iconbitmap("image//icon//icon_for_application.ico")  # Устанавливаем ему иконку.
    root['bg'] = color_for_root  # Придаем ему цвет, который был при прошлом выходе.
    root.resizable(False, False)  # Запрещаем менять размер.
    
    return root  # В итоге возращаем окно.

def create_field(color_for_field: str, color_for_cell: str, money_counter: tk.Label, matrix: tuple, btn_flags: tk.Button, timer: tk.Button, color_for_number: str="black") -> tk.Canvas:

    """
    Создает игровое поле с ячейками для ходов.

    Параметры:
    - color_for_field - цвет для игрового поля;
    - color_for_cell - цвет для ячеек поля;
    - money_counter - текстовый виджет с кол-вом монет для функций вне данной;
    - matrix - структура игрового поля (расположение мин, чисел и т. д.);
    - btn_flags - ячейка с кол-вом доступных флажков. Используется 
    для передачи в другую функцию, где данный виджет будет обрабатываться;
    - timer - ячейка с кол-вом времен, затраченного на прохождение игры.
    Используется для передачи данных с ячейки в другую функцию, где она нужна;
    - color_for_number (по умолчанию - 'black') - цвет для чисел на поле.

    Возращает:
        Игровое поле класса tk.Canvas.
    """
    
    # Создаем игровое поле.
    field = tk.Canvas(
        bg = color_for_field
    )

    coordinates_bombs = []  # Список, в котором будут храниться координаты бомб.
    coordinates_button = {}  # Словарь, в котором будет храниться информация о всех ячейках.
    criterion_for_win = []  # Список с координатами всех ячеек. Будет нужен для определения победы.

    # Места, где будет ставиться крестик - БЕЗОПАСНОЕ начало игры.
    good_buttons = {
        9: (4, 4),
        15: (7, 7),
        21: (10, 10)
    }

    start_button = good_buttons[len(matrix)]  # Определяем БЕЗОПАСНОЕ начало в соответствии с режимом.

    for i in range(len(matrix)):
        for j in range(len(matrix)):

            # Заполняем список с координатами бомб, если ячейка с бомбой.
            if matrix[i][j] == "💣":
                coordinates_bombs.append((i, j))

            # Создаем числа, которые будут помогать определять, где бомбы.
            # Будут находится под кнокпками, придавая форму игровому полю. 
            text = tk.Label(field, text=matrix[i][j], font="Arial 14", width=2, fg=color_for_number, bg=color_for_field)
            text.grid(row = i, column = j)

            # Выбор цвета для кнопок (может попасться цвет random).
            final_color_for_cell = color_for_cell if color_for_cell != "random" else choice(("aqua", "blue", "darkviolet", "green", "grey", "lightgreen", "lightgrey", "orange", "pink", "red", "violet", "yellow", "white"))
            
            cell = tk.Button(field, bg=final_color_for_cell, width=2, activebackground=final_color_for_cell)  # Создание ячейки.
        
            coordinates_button[(i, j)] = (cell, matrix[i][j], [color_for_cell])  # Добавляем информацю о ячейке в словарь.
            criterion_for_win.append((i, j))  # Передаем координаты ячейки в список для проверки на победу.
            command_lmb = partial(command_for_cells.command_for_cell_lmb, cell, (i, j), timer, money_counter, coordinates_button, field, coordinates_bombs, criterion_for_win)  # Функция, которая сработает при нажатии на левую кнопку мыши.
            command_rmb = partial(command_for_cells.command_for_cell_rmb, cell, btn_flags, coordinates_button, (i, j))   # Функция, которая сработает при нажатии на левую кнопку мыши.
            # Передаем все эти функции на обработку кнопке.
            cell.bind("<ButtonPress-1>", command_lmb)
            cell.bind("<ButtonPress-3>", command_rmb)

            if (i, j) == start_button: cell["text"] = "❌"  # Являеся ли кнопка "БЕЗОПАСНЫМ началом", и помечать ли ее крестиком?

            cell.grid(row = i, column = j)  # Размещаем ячейку на игровое поле.

    return field  # Возращаем игровое поле.


def restart(root: tk.Tk, command_for_restart) -> None:

    """
    Создает ячейку с функцие перезапуска игры.

    Параметры:
    - field - окно, где размещается ячейка;
    - command_for_restart - команда перезапуска.

    Возращает: ничего, просто ячейку создает.
    """

    # Создаем кнопку для перезапуска игры.
    restart_button = tk.Button(root, text="⟳", fg="red", width=2, command=command_for_restart)
    restart_button.place(x=140, y=50)

def close_root(root: tk.Tk, stop_running_process) -> None:

    """
    Создает запрос на выход из приложения. Если ответ - да, то останавливается
    таймер, очищается кэш, а приложение закрывается. В ином случае ничего не 
    просиходит.

    Параметры:
    - root - окно приложения, которое закроется при выходе;
    - stop_running_process - команда, останавливающая
    основной цикл программы.

    Возращает: ничего.
    """

    # Спрашиваем пользователя насчет выключения.
    if messagebox.askokcancel(message="Точно хотите выйти?", title="Выйти или не выйти - вот в чем вопрос!"):

        root.destroy()  # Закрываем главное окно.
        
        stop_running_process()  # Останавливаем основной цикл игры.

        try:
            shutil.rmtree('my_modules//__pycache__')  # Удаляем кэш.
        except FileNotFoundError:
            pass  # Если папки с кэшом нет.

        