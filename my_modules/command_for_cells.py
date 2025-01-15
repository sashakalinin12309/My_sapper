# Импортируем все нужные модули.
import tkinter as tk
from time import time
import my_modules.work_with_file as work_with_file

from my_modules.commands_win_and_lose import lose, neighbours_cells, win

game_over = False  # Переменная, которая позволяет понять, закончилась ли игра.
flags_counter = 10  # Перемнная с кол-вом неиспользованных флажков.
running_timer = False  # Переменная, определяющая, работает ли таймер.

# Дальше второстепенные функции, которые, по сути, не связаны с ячейками
def new_game() -> None:

    """ Функция позволяет переключить режим с концовки игры на начало."""
    
    global game_over
    game_over = False

def counter_flags(size_field: int) -> int:

    """
    Функция изменяет кол-во флажков для игры в зависимости от размеров поля.
    
    Параметры:
        size_field - размеры_поля (9, 15 или 21)
        
    Возращает:
        Число флажков, которое можно применить к ячейке, отвечающей за флажки.
    """

    global flags_counter

    if size_field == 9:
        flags_counter = 10
    elif size_field == 15:
        flags_counter = 35
    else:
        flags_counter = 99

    return flags_counter

def stop_timer() -> None:

    """Функция прерывает работу таймера."""
    
    global running_timer
    running_timer = False

# А дальше начинаются уже функии для ячеек.
# Вот эта для ЛЕВОЙ кнопки мыши (LEFT mouse button).
def command_for_cell_lmb(btn: tk.Button, coordinates: tuple, timer: tk.Button, money_counter: tk.Label, dict_about_btn: dict, field: tk.Canvas, coords_bombs: list, criterion_for_win: list, event) -> None:

    """
    Функция для ЛКМ, которая уничтожает ячейку и близ лежащие нули и 
    проигрывает результат: бомба или нет.

    Параметры:
    - btn - ячейка, на которую нажал пользователь;
    - coordinates - кортеж типа (x, y) для работы с матрицей-полем;
    - timer - таймер, но будем используем лишь его текст 
    для зафиксирования времени прохождения;
    - money_counter - счетчик монет пользователя для того, чтобы узнать
    кол-во монет;
    - dict_about_btn - словарь типа {
        (размещение_по_х, размещение_по_у): 
        ссылка_на_ячейку,
        значение_матрицы_в_данном_месте(бомба или число),
        [наличие_флага]
        } для дальнейшей работы с ячейками;
    - field - игровое поле, на котором расположены ячейки и написаны
    числа и бомбы;
    - coords_bombs - координаты всех бомб (при проигрыше на этих координатах
    будут отрисованы бомбы);
    - criterion_for_win - список со всеми координатами ячеек
    (в конце проходит проверка: какие ячейки по координатам остались.
    Если среди них остались только координаты бомб, то игра выиграна!)
    
    Возращает:
        Ничего, но ячейка и соседние нули уничтожаются.
    """

    # Импортируем глобальные переменные, которые понадобятся для...
    global game_over  # ...остановки работы данной команды и для ПРАВОЙ кнопки мышки.
    global running_timer  # ...остановки таймера вообще в другой функции.

    meaning = dict_about_btn[coordinates][1]  # Значение данной ячейки (бомба или число).

    if not(str(btn["image"]).isalnum()) and not(game_over):  # Если ячейка не помечена флажком и игра продолжается (не режим game_over).

        running_timer = True  # Сразу же обозначаем, что таймер работает!

        # Если игрок наступил на мину.
        if meaning == "💣":

            # Сразу же выводим на место ячейки текстовый виджет с бомбочкой.
            bomba_activate = tk.Label(field, text="💣", font="Arial 14", width=2, fg="black", bg="red")
            bomba_activate.grid(row=coordinates[0], column=coordinates[1])

            btn.destroy()  # Саму ячейку уничтожаем.

            lose(coords_bombs, dict_about_btn, field, money_counter)  # Запускаем функцию с проигрышем.
            running_timer = False  # Останавливаем таймер.
            game_over = True  # Включаем режим game_over. Конец игры с проигрышем.

        # Если же не наступил на мину.
        else:
            
            # Если вокруг ячейки нет бомб.
            if meaning == " ":

                pressed_buttons: set = set(coordinates)  # Множество с "уничтоженными" ячейками при пустой ячейке.
                neighbours: list = neighbours_cells(coordinates, dict_about_btn)  # Список с соседними ячейками той, на которую нажали.

                while len(neighbours) > 0:  # Пока останутся соседние ячейки

                    coordinates_button = neighbours.pop()  # Удаляем из списка одну из соседних клеток и запоминаем её координаты.
                    
                    # Если та соседняя клетка также останется "пустой".
                    if dict_about_btn[coordinates_button][1] == " ":
                        neighbours.extend(set(neighbours_cells(coordinates_button, dict_about_btn)) - pressed_buttons)  # Расширяем список ячеек соседними соседней ячейки.
                        neighbours = list(set(neighbours))  # Убираем все повторяющиеся ячейки.
                        
                    # Если же она с числом.
                    else:
                        # Если же ячейка не в соседних и на ней нет флажка.
                        if coordinates_button not in neighbours and dict_about_btn[coordinates_button][2] != ["flag"]:

                            dict_about_btn[coordinates_button][0].destroy()  # Удаляем ячейку и показываем число.
                            # Здесь уничтожаются только крайние ячейки той, так скажем, "пустой" зоны.

                            try:
                                delete = criterion_for_win.index(coordinates_button)  # Находим индекс ячейки в списке для проверки на победу.
                                del criterion_for_win[delete]  # Удаляем из списка эту ячейку, тем самым приближаясь к победе.
                            except ValueError:
                                pass
                    
                    # Удаляем все пустые соседние "пустые" ячейки, если они не с флажком.
                    if dict_about_btn[coordinates_button][2] != ['flag']:
                        dict_about_btn[coordinates_button][0].destroy()

                    try:
                        delete = criterion_for_win.index(coordinates_button)  # Находим индекс ячейки в списке для проверки на победу.
                        del criterion_for_win[delete]  # Удаляем из списка эту ячейку, тем самым приближаясь к победе.
                    except ValueError:
                        pass

                    pressed_buttons.add(coordinates_button)  # Добавляем к нажатым кнопкам ту соседнюю клетку.
   
                # Если останутся только ячейки с бомбами (все нажаты для победы).
                if criterion_for_win == list(filter(lambda x: "💣" in dict_about_btn[x], dict_about_btn)):

                    win(timer["text"], money_counter)  # Запускаем функцию победы.

                    running_timer = False  # Выключаем таймер
                    game_over = True  # Режим game_over включаем. Конец игры с выигрышем.
                    
            # Если ячейка не "пустая".        
            else:
                
                btn.destroy()  # Уничтожаем ячейку-кнопку.

                try:
                    delete = criterion_for_win.index(coordinates)  # Находим индекс ячейки в списке для проверки на победу.
                    del criterion_for_win[delete]  # Удаляем из списка эту ячейку, тем самым приближаясь к победе.
                except ValueError:
                    pass
                
                # Если останутся только ячейки с бомбами (все нажаты для победы).
                if criterion_for_win == list(filter(lambda x: "💣" in dict_about_btn[x], dict_about_btn)):

                    win(timer["text"], money_counter)  # Запускаем функцию победы.
                    
                    running_timer = False  # Выключаем таймер
                    game_over = True  # Режим game_over включаем. Конец игры с выигрышем.

# А эта функция для ячейки, если по ней кликнут правой кнопкой мыши.
def command_for_cell_rmb(btn: tk.Button, button_with_counter_flags: tk.Button, dict_about_btn: dict, coordinates: tuple, event) -> None:

    """
    Функция для ПКМ, которая устанавливает/убирает флажки.

    Параметры:
    - btn - ячейка, на которую нажал пользователь;
    - button_with_counter_flags - ячейка с кол-вом имеющихся флажков
    (менять ее текст будем);
    - dict_about_btn - словарь типа {
        (размещение_по_х, размещение_по_у): 
        ссылка_на_ячейку,
        значение_матрицы_в_данном_месте(бомба или число),
        [наличие_флага]
        } для дальнейшей работы с ячейками;
    - coordinates - кортеж типа (x, y) по размещению ячейки для работы
    с словарем.

    Возращает:
        Ничего, но устанавливает/убирает флажок.
    """
    # Устанавливаем глобальные параметры.
    global flags_counter  # Кол-во флажков.
    global game_over  # Нужна для остановки процесса игры.

    check = str(btn["image"]).isalnum()  # Проверка на то, установлен ли флажок на кнопке.

    # Пока идет процесс игры.
    if not(game_over):

        if check:  # Если флажок был установлен.

            btn.config(image="", width=2, height=1)  # Убираем флажок, изменяем размеры под простую кнопку.
            dict_about_btn[coordinates][2][0] = "no_flag"  # Добавим статус "не под флагом".
            flags_counter += 1  # Раз флаг убрали, то к несипользованным прибавляется ещё один.

        else:  # Если флажок не был установлен.

            if flags_counter != 0:  # Можно добавлять флажки на поле, если их кол-во не равняется нулю (они есть).

                img = tk.PhotoImage(file=f"image//for_use_in_game//flags//{work_with_file.information_in_Information()["Цвет_флага"]}_flags.png")  # Создаем переменную с изображением флажка.
                btn.config(text="", image=img, compound=tk.BOTTOM, width=18, height=20)  # Добавляем изображение на кнопку-ячейку.
                btn.image = img  # Сохраняем ссылку на изображение для кнопки (так надо).

                dict_about_btn[coordinates][2][0] = "flag"  # Установливаем статус "под флажком".
                flags_counter -= 1  # Убавляем кол-во неиспользованных флажков на 1.


    button_with_counter_flags['text'] = flags_counter  # Изменяем текст на кнопке с кол-вом флажков.

# А это работа таймера.
def process_timer(timer: tk.Button) -> None:

    """
    Функция представляет собой работу таймера.

    Параметры:
        timer - таймер, в котором будем менять текст.

    Возращает:
        Ничего, но обновляет таймер, меняя его текст.
    """

    global running_timer  # Глобальная переменная, отвечающая за работа и "отдых" таймера.

    if running_timer:  # Если данная переменная True.

        start_time = time()  # Узнаем текущее время.
        
        # Пока running_timer активен и этот таймер не дошел до 999.9 секунд.
        while running_timer and timer["text"] != 999.9:
            
            timer['text'] = round(time() - start_time, 1)  # Вычисляем время таймера.
            timer.update()  # Обновляем его (точнее, его текст)
