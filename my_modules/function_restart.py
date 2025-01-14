# Импортируем все нужные модули.
import tkinter as tk

import my_modules.interface as interface
import my_modules.minefield as minefield
import my_modules.command_for_cells as command_for_cells

import my_modules.work_with_file as work_with_file

def restart_game(root: tk.Tk, btn_flags: tk.Button, btn_timer: tk.Button, money: tk.Label) -> None:

    """
    Что делает данная функция:
    - удаляет старое и создает новое игровое поле с ячейками, помещает его на главное окно;
    - устанавливает значения для таймера и кол-ва флажков.
    
    Параметры:
    - root - главное окно приложения, на которое будет расположены игровое поле;
    - btn_flags - кнопка с кол-вом доступных флажков. Установим её текстовое значение равное 0;
    - btn_timer - кнопка, отвечающая за таймер. Сбросим её значение до нуля;
    - money - текстовый виджет, отвечающий за кол-во монет у пользователя. Его 
    мы поместим в параметры другой функции, отвечающей за создание игрового поля.
    
    Что в итоге:
        При перезапуске пользователь получает новое игровое поле и может дальше играть.
    """
        
    information_about_game = work_with_file.information_in_Information()  # Информация об интерфейсе.
    
    # Создаем переменные, в которые будет занесена информация о чём-либо.
    size = int(information_about_game['Размер_поля'])
    
    field_color: str = information_about_game["Цвет_поля"]
    cell_color: str = information_about_game["Цвет_ячейки"]

    last_field: tk.Canvas = [widget for widget in root.winfo_children() if type(widget) == tk.Canvas][0]  # Узнаем ссылку на игровое поле.
    
    last_field.destroy()  # Удаляем старое игровое поле.

    command_for_cells.new_game()  # Переключаем с режима концовки на начало.
    command_for_cells.stop_timer()  # Прерываем таймер, чтобы в новой игре его запустить.
    
    matrix: tuple = minefield.create_minefield(size)  # Создаем матрицы, от которой будет зависеть расположение бомб.
    new_field: tk.Canvas = interface.create_field(field_color, cell_color, money, matrix, btn_flags, btn_timer)  # Создаем игровое поле.
    new_field.place(x=25, y=100)
    btn_flags["text"] = command_for_cells.counter_flags(size)  # Изменяем кол-во флажков.
    btn_timer["text"] = 0  # Изменяем значение таймера.

