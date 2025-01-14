# Импортируем нужные модули.
import tkinter as tk
from tkinter import messagebox

import my_modules.work_with_file as work_with_file

# Функция, определяющая координаты соседних ячеек.
def neighbours_cells(coordinates: tuple, matrix: dict) -> list:

    """
    Функция определяет координаты соседних ячеек и выводит их в виде списка.

    Параметры:
    - coordinates - координаты в кортеже типа (х, у);
    - matrix - матрица, лежащая в основе игрового поля.

    Возращает:
        Координаты соседних ячеек в виде списка eighbors_buttons_in_list
    """

    neighbors_buttons_in_list: list = []  # Список, в котором будут находится координаты соседних ячеек.

    arithmetic_operations: tuple = ('-1' , '-0', '+1')  # Арифметические операции для упрощения нахождения координат.

    for i in range(3):
        for j in range(3):

            # Нахождение х и у.
            x = int(eval(str(int(coordinates[0])) + arithmetic_operations[i]))
            y = int(eval(str(int(coordinates[1])) + arithmetic_operations[j]))

            # Проверка на возможность существования таких координат.
            # (Чтобы не выходили за границы игрового поля) 
            if int(len(matrix)**0.5) > x >= 0 and int(len(matrix)**0.5) > y >= 0:
                neighbors_buttons_in_list.append((x, y,))
    
    return neighbors_buttons_in_list  # Возращаем список с координатами.

# Функция, активация которой запланирована при проигрыше пользователя.
def lose(coordinates_bombs: tuple, all_buttons: dict, field: tk.Canvas, money: tk.Label) -> None:

    """
    Функция активируется, если пользователь проиграл (нажал на ячейку с миной).
    Выполняет следующие задачи:
    - вычитает определенное кол-во монет у пользователя (зависит от  режима);
    - показывает на поле те места, где находились бомбы;
    - выводит сообщение о проигрыше.

    Параметры:
    - coordinates_bombs - координаты местоположения бомбочек в кортеже;
    - all_buttons - словарь со всеми ячейками для их деактивации при проигрыше;
    - field - поле, где будут отмечаться бомбы;
    - money - текстовый виджет с кол-вом монет у пользователя.
    Нужен для изменения его текста.

    Выводит:
        Ничего, лишь выполняет вышесказанные задачи.
    """

    # Блокируем все кнопки, изменяя статус на disabled.
    for coordinates in all_buttons:

        try:
            all_buttons[coordinates][0].config(state=tk.DISABLED)
        except tk.TclError:
            continue

    # Уничтожаем все кнопки-ячейки с бомбами, заменяем их на тексты-бомбы.
    for coordinates in coordinates_bombs:

        # Само уничтожение.
        button_for_destroy = all_buttons[coordinates][0]
        button_for_destroy.destroy()

        # Замена на текстовый виджет с бомбой.
        bomba_activate = tk.Label(field, text="💣", font="Arial 14", width=2, fg="black", bg="red")
        bomba_activate.grid(row=coordinates[0], column=coordinates[1])

    information_about_game = work_with_file.information_in_Information()  # Получаем информацию, нужную для осуществления дальнейших действий.
    
    # При проигрыше у игрока будут забирать монеты (может даже в минус).
    # А сколько будут забирать - это уже в зависимости от режима.  
    if information_about_game["Размер_поля"] == "9":

        information_about_game["Монеты"] = int(information_about_game["Монеты"]) - 2

    elif information_about_game["Размер_поля"] == "15":

        information_about_game["Монеты"] = int(information_about_game["Монеты"]) - 5

    elif information_about_game["Размер_поля"] == "21":

        information_about_game["Монеты"] = int(information_about_game["Монеты"]) - 7
    

    money["text"] = str(information_about_game["Монеты"])  # Обновляем кол-во монет у пользователя в самом виджете.

    messagebox.showerror(title="Вимание!", message="Ты проиграл!!!")  # Выводим сообщение о проигрыше.

    # Записываем обновленную информацию о достижениях игрока в файл.
    # Это нужно для сохранения информации даже при перезапуске приложения. 
    work_with_file.write_document_Information(information_about_game)

# Эта функция запускается при выигрыше игрока.
def win(timer_counter: str | int, money: tk.Label):

    """
    Функция активируется, если пользователь выиграл (остались только ячейки с минами).
    Выполняет следующие задачи:
    - прибавляет определенное кол-во монет пользователю (зависит от  режима);
    - выводит сообщение о выигрыше + если новый рекорд

    Параметры:
    - timer_counter - число, с которым пользователь прошел игру (для проверки с рекордом);
    - money - текстовый виджет с кол-вом монет у пользователя.
    Нужен для изменения его текста.

    Выводит:
        Ничего, лишь выполняет вышесказанные задачи.
    """

    new_record = False  # Переменная, отвечающая за определение нового рекорда.

    information_about_game = work_with_file.information_in_Information()  # Получаем информацию, нужную для осуществления дальнейших действий.
    
    # Для поощрения игрока, мы будем прибавлять к его сумме несколько монет.
    # Опять же, прибавленная сумма будет зависеть от режима. 
    if information_about_game["Размер_поля"] == "9":

        information_about_game["Монеты"] = int(information_about_game["Монеты"]) + 5  # Для записи в файл

        # Определение нового рекорда.
        if str(information_about_game["Рекорд_9"]) == "нет_результата" or float(information_about_game["Рекорд_9"]) > float(timer_counter):
            information_about_game["Рекорд_9"] =  timer_counter  # Записываем информацию о рекорде в словарь. который запишем в файл.
            new_record = True  # Это для дальнейшей проверки.

            information_about_game["Монеты"] = int(information_about_game["Монеты"]) + 2  # Не забываем изменить кол-во монет на +2 (все же рекорд!).

    # Дальнейшие действия идентичны предыдущим, поэтому пояснять не буду )
    elif information_about_game["Размер_поля"] == "15":

        information_about_game["Монеты"] = int(information_about_game["Монеты"]) + 15

        if str(information_about_game["Рекорд_15"]) == "нет_результата" or float(information_about_game["Рекорд_15"]) > float(timer_counter):
            information_about_game["Рекорд_15"] =  timer_counter
            new_record = True

            information_about_game["Монеты"] = int(information_about_game["Монеты"]) + 4

    elif information_about_game["Размер_поля"] == "21":

        information_about_game["Монеты"] = int(information_about_game["Монеты"]) + 25

        if str(information_about_game["Рекорд_21"]) == "нет_результата" or float(information_about_game["Рекорд_21"]) > float(timer_counter):
            information_about_game["Рекорд_21"] =  timer_counter
            new_record = True

            information_about_game["Монеты"] = int(information_about_game["Монеты"]) + 6
            
    money["text"] = str(information_about_game["Монеты"])  # Изменяем текст виджета, отвечающего за отображение кол-ва монет.

    # Если новый рекод, то пользователь об этом узнает через диалоговое окно.
    if new_record:

        add_money = {"9": 2, "15": 4, "21": 6}
        how_many: int = information_about_game["Размер_поля"]
        messagebox.showinfo(title="Поздравляю!", message=f"Ты выиграл!!! Новый рекорд: {timer_counter}", detail=f"За новый рекорд +{add_money[how_many]} монетки к остальному результату!")
    # Если же нет, то просто объявление о выигрыше.
    else:
        messagebox.showinfo(title="Поздравляю!", message="Ты выиграл!!!")

    work_with_file.write_document_Information(information_about_game)  # Запишем новую информацию в файл.

