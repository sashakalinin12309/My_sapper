# Импортируем все нужные модули.
import tkinter as tk
from tkinter import messagebox
from functools import partial
from random import choice

import my_modules.function_restart as function_restart
import my_modules.work_with_file as work_with_file
import my_modules.functions_collections as functions_collections

# Словарь-переводчик.
dict_colors = {
    'red': 'Красный', 
    'orange': 'Оранжевый', 
    'yellow': 'Желтый', 
    'lightgreen': 'Светло-зеленый', 
    'green': 'Темно-зеленый', 
    'aqua': 'Голубой',  
    'blue': 'Синий', 
    'violet': 'Светло-фиолетовый', 
    'darkviolet': 'Темно-фиолетовый', 
    'pink': 'Розовый',
    'lightgrey': 'Светло-серый(классический)',
    'grey': 'Серый(классический)',
    'white': 'Белый(классический)'
}

def shop(root: tk.Tk, change: str, color: str, menu_for_change: tk.Menu, index_for_change: int, label_money: tk.Label) -> None:

    """
    Функция принимает часть приложения (окно, поле, ячейки, флажки) и 
    видоизменяет их под параметры, которые выбирает пользователь в меню.

    Если коротко - это магазин, где пользователь может поменять цвет окна,
    поля, ячеек или флажков.

    Параметры:
    - root - само окно приложения. Будет либо его цвет изменять, либо будем 
    находить в нем его дочерние элементы: поле, а там и ячейки;
    - change - выбор места, которое будем изменять (окно, поле, ячейки, флажки);
    - color - тот цвет, на который будет заменен старый;
    - menu_for_change - меню, в котором будем изменять компоненты (accelerator напрмер);
    - index_for_change - индекс того элемента меню, которого будем изменять (для entryconfig);
    - label_money - текстовый виджет, который показывает пользователю его кол-во монет.
    Нужен для изменения баланса в случае покупки.

    Возращает: ничего.
    """

    colors = work_with_file.information_in_Information_about_shop()  # Выясняем информацию о наличии цветов у игрока.
    information_about_game = work_with_file.information_in_Information()  # Выясняем общую информацию о игре.
    
    if change == "окно":  # Если пользователь хочет изменить главное окно.

        if bool(int(colors[color]["окно"])):  # Если этот цвет уже приобретен на окно.

            # Вопрос о серьёзности данного решения.
            if messagebox.askokcancel(title="Точно хочешь?", message="Точно хочешь?"):

                root["bg"] = color  # Меняем цвет окна на выбранный.
                label_money["bg"] = color  # Меняем цвет виджета с монетами на выбранный.

                # Записываем о изменении в цвете окна пока что в словарь.
                information_about_game = work_with_file.replace_in_the_Information(["Цвет_окна", color])

        else:  # Если этот цвет у окна не приобретён.
            
            # Запрашиваем подтверждение покупки.
            if messagebox.askokcancel(title="Совершение покупки!", message=f"Точно ли ты хочешь приобрести цвет {dict_colors[color]} для окна за 50 монет?"):

                if int(information_about_game["Монеты"]) < 50:  # Если не будет хватать монет.

                    messagebox.showerror(title="А вот и нет!", message="Недостаточно средств!!!")  # Вывод сообщения о нехватке средств.
                    
                else:  # Если всё же монет хватает.

                    label_money.config(text=int(label_money['text'])-50, bg=color)  # Изменяем кол-во монет на виджете + цвет виджета.

                    information_about_game = work_with_file.replace_in_the_Information(["Цвет_окна", color], ["Монеты", label_money["text"]])  # Заносим изменения в словарь.

                    menu_for_change.entryconfig(index_for_change, accelerator="Приобретено")  # Меняем статус цвета в меню на "Приобретено".

                    colors[color]["окно"] = 1  # Записываем о приобретении цвета.

                    root["bg"] = color  # Меняем цвет у окна.

                    work_with_file.write_document_Information_about_shop(colors)  # Записываем о приобретении цвета в файл.

        work_with_file.write_document_Information(information_about_game)  # Записываем об изменении цвета окна и, при приобретении, изменении монет.

    # Если пользователь захочет изменить цвет флажков.
    elif change == "флажки":

    # Ну, впринципе, здесь такая же история, как и с окном, но:
    # - стоимость флажков равна 25 монет;
    # - не изменяем цвет виджета монет...
    # Ну, и всё!  

        if bool(int(colors[color]["флажки"])):

            if messagebox.askokcancel(title="Точно хочешь?", message="Точно хочешь?"):

                information_about_game = work_with_file.replace_in_the_Information(["Цвет_флага", color])

                work_with_file.write_document_Information(information_about_game)
                
        else:

            if messagebox.askokcancel(title="Совершение покупки!", message=f"Точно ли ты хочешь приобрести флажок цвета {dict_colors[color] if color != 'green' else "Зеленый"} за 25 монет?"):

                if int(information_about_game["Монеты"]) < 25:

                    messagebox.showerror(title="А вот и нет!", message="Недостаточно средств!!!")
                    
                else:

                    label_money["text"] = int(label_money['text']) - 25

                    information_about_game = work_with_file.replace_in_the_Information(["Цвет_флага", color], ["Монеты", label_money["text"]])

                    menu_for_change.entryconfig(index_for_change, accelerator="Приобретено")

                    colors[color]["флажки"] = 1

                    work_with_file.write_document_Information_about_shop(colors)

                    work_with_file.write_document_Information(information_about_game)


    # Тут два варианта - поле или ячейки.
    # Просто они взаимосвязаны. 
    else:

        # Нам в любом случае понадобится игровое поле.
        field = tuple(element for element in root.winfo_children() if type(element) == tk.Canvas)[0]
        
        # Если выбрали поле...
        # Впринципе, изменение поля ничем не отличается от изменения окна.
        # Только здесь не изменяем виджет для монет и всё!  
        if change == "поле":
            
            if bool(int(colors[color]["поле"])):

                if messagebox.askokcancel(title="Точно хочешь?", message="Точно хочешь?"):
    
                    labels = tuple(element for element in field.winfo_children() if type(element) == tk.Label)

                    information_about_game = work_with_file.replace_in_the_Information(["Цвет_поля", color])
                    work_with_file.write_document_Information(information_about_game)

                    for el in labels:

                        element = el
                        element["bg"] = color

            else:

                if messagebox.askokcancel(title="Совершение покупки!", message=f"Точно ли ты хочешь приобрести цвет {dict_colors[color]} для поля за 50 монет?"):
                
                    if int(information_about_game["Монеты"]) < 50:

                        messagebox.showerror(title="А вот и нет!", message="Недостаточно средств!!!")
                        
                    else:

                        label_money['text'] = int(label_money['text']) - 50
                        information_about_game = work_with_file.replace_in_the_Information(["Цвет_поля", color], ["Монеты", label_money['text']])

                        menu_for_change.entryconfig(index_for_change, accelerator="Приобретено")

                        labels = tuple(element for element in field.winfo_children() if type(element) == tk.Label)

                        for el in labels:

                            element = el
                            element["bg"] = color

                        colors[color]["поле"] = 1

                    work_with_file.write_document_Information(information_about_game)
                    work_with_file.write_document_Information_about_shop(colors)

        # Если выбрали ячейки.
        # вот здесь будет кое-что новенькое. 
        elif change == "ячейки":

            if bool(int(colors[color]["ячейки"])):  # Проверка на приобретённость данного цвета.

                if messagebox.askokcancel(title="Точно хочешь?", message="Точно хочешь?"):  # Спрашиваем.
                    
                    # Получаем все кнопки-ячейки из поля как дочерние элементы.
                    buttons = tuple(element for element in field.winfo_children() if type(element) == tk.Button)

                    information_about_game = work_with_file.replace_in_the_Information(["Цвет_ячейки", color])  # Меняем цвет у ячеек в словаре.
                    work_with_file.write_document_Information(information_about_game)  # Записываем данный цвет в файл.

                    for el in buttons:  # Перебираем все эти копки для изменения цвета.

                        element = el
                        final_color = color if color != "random" else choice(("aqua", "blue", "darkviolet", "green", "grey", "lightgreen", "lightgrey", "orange", "pink", "red", "violet", "yellow", 'white'))  # В случае цвета random
                        element.config(bg=final_color, activebackground=final_color)  # Перекрашиваем.

            else:  # Если цвет не приобретён, то его, видимо, хотят купить.
                
                # Запрос на покупку.
                if messagebox.askokcancel(title="Совершение покупки!", message=f"Точно ли ты хочешь приобрести цвет {dict_colors[color] if color != 'random' else "Случайный"} для ячеек за {"50" if color != 'random' else '75'} монет?"):

                    # Если не хватает монет.
                    if (color != "random" and int(information_about_game["Монеты"]) < 50) or (color == "random" and int(information_about_game["Монеты"]) < 75):
                        
                        # Сообщение о нехватке монет.
                        messagebox.showerror(title="А вот и нет!", message="Недостаточно средств!!!")
                        
                    else:  # Если же хватает.

                        label_money['text'] = int(label_money['text']) - 50 if color != "random" else int(label_money['text']) - 75  # Вычитаем нужную сумму монет.
                        information_about_game = work_with_file.replace_in_the_Information(["Цвет_ячейки", color], ["Монеты", label_money["text"]])  # Перезаписываем в словаре про цвет ячейки и кол-во монет.

                        menu_for_change.entryconfig(index=index_for_change, accelerator="Приобретено")  # Меняем статус цвета в меню на "Приобретён".

                        colors[color]["ячейки"] = 1  # Запоминаем о покупке данного цвета для ячеек.

                        # Собиораем все кнопки-ячейки в один список.
                        buttons = tuple(element for element in field.winfo_children() if type(element) == tk.Button)

                        for el in buttons:  # Перебираем кнопки.

                            element = el
                            final_color = color if color != "random" else choice(("aqua", "blue", "darkviolet", "green", "grey", "lightgreen", "lightgrey", "orange", "pink", "red", "violet", "yellow", "white"))  # В случае цвета random.
                            element.config(bg=final_color, activebackground=final_color)  # Меняем цвет.

                    # Записываем всю новую информацию в файлы.
                    work_with_file.write_document_Information(information_about_game)
                    work_with_file.write_document_Information_about_shop(colors)



def change_the_size(root: tk.Tk, new_size: int, for_function_restart: list = None) -> None:

    """
    Функция изменяет главное окно приложения под определенные размеры,
    а также перезапускает игровое поле, если команда запускается с меню.

    Параметры:
    - root - главное окно приложения, которое надо изменить;
    - new_size - размер нового игрового поля (9, 15 или 21),
    взаивисимости от которого окно будет изменяться под определенный размер;
    - for_function_restart - список, который включает в себя:
        - btn_flags: Button - ячейка с кол-вом имеющихся флажков;
        - btn_timer: Button - ячейка с таймером;
        - money: Label - текстовый виджет с кол-вом монет пользователя.
        
        Все эти виджеты нужны для изменения текста в них.

        Также эта функция используется для изменения окна в размер 9х9 в начале программы,
        и поэтому по умолчанию for_function_restart стоит как None, чтобы было удобнее
        разбираться, когда эта функция активируется.

    Возращает: ничего.
    """

    # Изменяем размер поля в файле.
    information_about_game = work_with_file.replace_in_the_Information(["Размер_поля", new_size])
    work_with_file.write_document_Information(information_about_game)

    # Выясняем, какой размер главного окна нужен будет для такого поля.
    if new_size == 9: root.geometry("300x400")
    elif new_size == 15: root.geometry("473x556")
    elif new_size == 21: root.geometry('641x725')

    # Если данная функция запущена НЕ ПРИ СОЗДАНИИ главного окна,
    # а при его ИЗМЕНЕНИИ.
    # Т. е. сам игрок хочет изменить игровое поле, а не компьютер использует её.
    if for_function_restart != None:

        btn_flags, btn_timer, money = for_function_restart   # Называем переменные.

        function_restart.restart_game(root, btn_flags, btn_timer, money)  # Запускаем функцию перезапуска.


def find_the_records(field_size: int) -> None:

    """
    Функция создает всплывающее окно, в котором будет написан рекорд
    пользователя в выбранном режиме.

    Параметры:
        field_size - режим (9, 15 или 21), в котором пользователь хочет 
        узнать свой рекорд.

    Возращает: ничего.
    """

    information_about_game = work_with_file.information_in_Information()  # Получаем информацию о достижениях игрока.

    if_not_games = "В данном режиме еще не было побед!"  # Это будет отображаться, если в данном режиме нет рекорда.
    title_record = "Какой же у тебя рекорд? Интересно!"  # Название диалогового окна

    # Дальше зависит от режима, рекорд которого хочет узнать игрок.
    if field_size == 9:

        # Если нет результата в данном режиме.
        if information_about_game["Рекорд_9"] == "нет_результата":

            messagebox.showinfo(title=title_record, message=if_not_games)

        else:  # Если же есть, то выводим сообщение с этим рекордом.
            
            messagebox.showinfo(title=title_record, message=f"Рекорд в 9Х9 - {information_about_game['Рекорд_9']} секунд.")

    elif field_size == 15:
        
        if information_about_game["Рекорд_15"] == "нет_результата":

            messagebox.showinfo(title=title_record, message=if_not_games)

        else:

            messagebox.showinfo(title=title_record, message=f"Рекорд в 15Х15 - {information_about_game['Рекорд_15']} секунд.")

    elif field_size == 21:

        if information_about_game["Рекорд_21"] == "нет_результата":

            messagebox.showinfo(title=title_record, message=if_not_games)

        else:

            messagebox.showinfo(title=title_record, message=f"Рекорд в 21Х21 - {information_about_game['Рекорд_21']} секунд.")


def create_menu(root: tk.Tk, money: tk.Label, btn_flags: tk.Button, btn_timer: tk.Button, images_flags: dict, colors_interface: dict) -> tk.Menu:

    """
    Функция создает меню, которое может изменять размеры поля, показазывать рекорды,
    имеет целый магазин, позволяющий устанавливать цвета элементов окна.

    Параметры:
    - root - окно, в котором будут изменения;
    - money - текстовый виджет с кол-вом монет у пользователя. В дальнейшем
    будем изменять это кол-во;
    - btn_flags - ячейка с кол-вом имеющихся флажков. В дальнейшем будем 
    изменять это кол-во;
    - btn_timer - ячейка-таймер. Также будем изменять ее текст;
    - images_flags - словарь типа {цвет: картинка_флажка} с флажками;
    - colors_interface - словарь типа {цвет: картинка цвета} для наглядного 
    изображения цвета.

    Возращает:
        Готовое меню для приложения.
    """

    size_root = (9, 15, 21)  # Возможные размеры игрового поля.

    game_menu = tk.Menu()  # Самое главное меню, в которое мы заключим остальные подменю.
    settings_menu = tk.Menu(tearoff=False)  # Меню с возможными функциями для игрока (смена режима, магазин и т. п.).

    values = ("Режим", "Узнать рекорд", "Магазин")  # Название функций.
    values_of_the_value = (["9x9", "15x15", "21x21"], ["9x9", "15x15", "21x21"], ["Окно", "Поле", "Ячейки", "Флажки", "Собственные_коллекции"])  # Варианты, которые будут предложены каждой функции сответственно.
    commands = ([partial(change_the_size, root, size, [btn_flags, btn_timer, money]) for size in size_root], [partial(find_the_records, size) for size in size_root])  # Почти все команды для каждого варианта (без магазина).

    for i in range(len(values_of_the_value)):

        for j in range(len(values_of_the_value[i])):

            # Функцию выбора цветов "Магазин" выносим отдельно, 
            # т. к. её варианты также будут иметь свои подменю.
            if values[i] == "Магазин":

                colors_menu = tk.Menu(tearoff=False)  # Создаем подменю для одного из вариантов

                index = 1  # Индекс, по которому будем искать данный элемент в меню.
                place = tk.StringVar(value=values_of_the_value[i][j])  # Место, к которому прикреплены цвета (для работы с Radiobuttons).

                # "Флажки" и "Собственные коллекции" выносим на отдельный план,
                # т. к. первое отличается изображением, которое будем добавлять элементу,
                # а второе - изображением (его не будет) и дополнительным подменю. 
                if values_of_the_value[i][j] not in ["Флажки", "Собственные_коллекции"]:

                    colors_menu.add_cascade(label="Платно (за игровую валюту)", state='disabled')  # Создавая такой элемент, отделяем бесплатные цвета от платных.
                    colors_menu.add_separator()  # Добавляем линию, отделяющую текст о платности цветов и название цветов.

                    # Получается (схематично):
                    # Платно (за игровую валюту)
                    # ---------
                    # Красный  # первый цвет   

                    for color in dict_colors:  # Перебираем все цвета.

                        index += 1  # изменяем индекс на нужный.

                        # Перед светло-серым цветом должны поставить 
                        # обозначение о бесплатности последующих цветов, а именно:
                        # светло-серого, серого и белого (так скажем, классических).    
                        if color == "lightgrey":

                            # Однако, если рассматриваем ячейки, 
                            # то к платным должны добавить цвет random.
                            if values_of_the_value[i][j] == "Ячейки":

                                command_color = partial(shop, root=root, change=values_of_the_value[i][j].lower(), color="random", menu_for_change=colors_menu, index_for_change=index, label_money=money)  # Создаем команду для данной ячейки.
                                colors_menu.add_radiobutton(label="Случайный_цвет_у_всех_ячейок", image=colors_interface["random"], compound=tk.LEFT, command=command_color, accelerator="Приобретено" if int(work_with_file.information_in_Information_about_shop()["random"][values_of_the_value[i][j].lower()]) else "Купить за 75 монет!", variable=place)  # Добавляем цвет random к ячейкам как платный.

                            colors_menu.add_separator()  # Добавляем линию, открывая...
                            colors_menu.add_cascade(label="Бесплатно", state='disabled')  # ...текст о том, что следующие цвета бесплатные, и...
                            colors_menu.add_separator()  # ...и добавляем линию, закрывая текст.

                            # Получается (схематично):
                            # random  # (если ячейки)
                            # -------------
                            # Бесплатно
                            # -------------
                            # Светло-серый (классический).    
                        
                        command_color = partial(shop, root=root, change=values_of_the_value[i][j].lower(), color=color, menu_for_change=colors_menu, index_for_change=index, label_money=money)  # Создаем команду для данной ячейки с цветом.
                        colors_menu.add_radiobutton(label=dict_colors[color], image=colors_interface[color], compound=tk.LEFT, command=command_color, accelerator="Приобретено" if int(work_with_file.information_in_Information_about_shop()[color][values_of_the_value[i][j].lower()]) else "Купить за 50 монет!", variable=place)  # Добавляем ячейку с цветом в меню.

                        # Здесь изображение - кружок с нужным цветом.

                elif values_of_the_value[i][j] == "Собственные_коллекции":  # Если сейчас создаем коллекции.

                    index = 0  # Нумерация элементов.

                    # Создание подменю для созданных коллекций.
                    for name_collection in work_with_file.information_in_Collection_player():
                        
                        # Создание словаря с названием элемента подменю и его командой.
                        commands_activities = {
                            "Применить": partial(functions_collections.apply_collection, root, name_collection, money), 
                            "Изменить": partial(functions_collections.create_collection, main_root=root, menu=colors_menu, number_element=index, label_money=money, new_changes=list([name_collection]+[work_with_file.information_in_Collection_player()[name_collection][place] for place in work_with_file.information_in_Collection_player()[name_collection]])),
                            "Информация": partial(functions_collections.information_about_collection, name_collection),
                            "Удалить": partial(functions_collections.delete_collection, colors_menu, index, root, money)
                        }

                        choice_activities = tk.Menu(tearoff=False)  # Создание подменю как объекта.

                        # Заполнение подменю.
                        for activity in commands_activities:

                            choice_activities.add_command(label=activity, command=commands_activities[activity])

                        colors_menu.add_cascade(label=name_collection, menu=choice_activities)   # Создание коллекции с её подменю в меню с коллекциями.

                        index += 1   # Изменяем индекс для будущих элементов.

                    # Всего возможно создание и хранение только 6 коллекций.
                    while index != 6:  # Это создание "пустых" элементов для содания коллекций.

                        choice_activities = tk.Menu(tearoff=False)  # Создаем подменю...
                        choice_activities.add_command(label="Создать...", command=partial(functions_collections.create_collection, main_root=root, menu=colors_menu, number_element=index, label_money=money))  # ...в котором будет всего лишь одна команда создания коллекции.

                        colors_menu.add_cascade(label="Создать...", menu=choice_activities)  # Создаем элемент коллекции с её подменю в меню с коллекциями.

                        index += 1  # Изменяем индекс для будущих коллекций.

                else:  # Если создаем подменю с флажками.

                    # Опять обозначаем, что цвета платные.
                    colors_menu.add_cascade(label="Платно (за игровую валюту)", state='disabled')
                    colors_menu.add_separator()

                    for color in dict_colors:
                        
                        # Вот только здесь берём не все, а несколько цветов.
                        if color in ["aqua", "blue", "green", "orange", "pink", "violet", "yellow"]:

                            index += 1  # Индекс для вычисления местоположения в меню.
                            
                            # Создаем элемент с цветом флажка.
                            # Здесь изображение - флажок нужного цвета. 
                            command_color = partial(shop, root=root, change=values_of_the_value[i][j].lower(), color=color, menu_for_change=colors_menu, index_for_change=index, label_money=money)
                            colors_menu.add_radiobutton(label=dict_colors[color] if color != "green" else "Зеленый", image=images_flags[color], compound="left", command=command_color, accelerator="Приобретено" if int(work_with_file.information_in_Information_about_shop()[color][values_of_the_value[i][j].lower()]) else "Купить за 25 монет!", variable=place)

                    index += 1  # Индекс для красного флажка

                    # Отделяем платные цвета от бесплатного красного.
                    colors_menu.add_separator()
                    colors_menu.add_cascade(label="Бесплатно", state='disabled')
                    colors_menu.add_separator()
                    
                    # Создаем элемент с красным флажком.
                    command_color = partial(shop, root=root, change=values_of_the_value[i][j].lower(), color="red", menu_for_change=colors_menu, index_for_change=index, label_money=money)
                    colors_menu.add_radiobutton(label='Красный', image=images_flags['red'], compound="left", command=command_color, accelerator="Приобретено", variable=place)
                    
                settings_menu.add_cascade(label=values_of_the_value[i][j], menu=colors_menu)  # Добавляем готовое подменю элементов магазина.

            else:  # Если выбраны "Режим" или "Рекорд".
                
                # Создаем простенькое подменю.
                settings_menu.add_command(label=values_of_the_value[i][j], command=commands[i][j])

        game_menu.add_cascade(label=values[i], menu=settings_menu)  # Добавляем меню с подменю в главное меню.

        settings_menu = tk.Menu(tearoff=False)  # Создаем новое подменю для дальнейшего использования.

    return game_menu  # Возращаем готовое меню для приложения.

