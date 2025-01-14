# Импортируем все нужные модули.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
from random import choice

import my_modules.work_with_file as work_with_file

# Дальше идут два словаря-переводчика.
colors_from_en_to_ru = {
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
    'white': 'Белый(классический)',
    "random": "Случайный"
}
colors_from_ru_to_en = {
    'Красный': 'red', 
    'Оранжевый': 'orange', 
    'Желтый': 'yellow', 
    'Светло-зеленый': 'lightgreen', 
    'Темно-зеленый': 'green', 
    'Голубой': 'aqua', 
    'Синий': 'blue', 
    'Светло-фиолетовый': 'violet', 
    'Темно-фиолетовый': 'darkviolet', 
    'Розовый': 'pink', 
    'Светло-серый(классический)': 'lightgrey', 
    'Серый(классический)': 'grey', 
    'Белый(классический)': 'white', 
    'Случайный': 'random'
}

# Функция по созданию коллекций.
def create_collection(main_root: tk.Tk, menu: tk.Menu, number_element: int, label_money: tk.Label, new_changes: list = None) -> None:

    """
    Функция направлена на создание и изменение коллекции игрока.

    Параметры:
    - main_root - главное окно приложения, к которому будет привязано 'подокно'
    создания или изменения коллекции;
    - menu - меню приложения, в котором находится кнопка с коллекцией. Нужно для
    изменения этой кнопки.
    - number_element - порядковый индекс кнопки в меню;
    - label_money - текстовый виджет, показывающий кол-во монет у пользователя.
    Нужен для переправки информации о нем в функцию aplly_collections;
    - new_changes - список с названием коллекции и ее цветовой гаммы. Используется
    только в том случае, если коллекция изменяется (тогда передается список типа 
    [название коллекции, цвет_окна, цвет_поля, цвет_ячеек, цвет_флажов]. 
    По умолчанию стоит None.

    Возращает:
        Ничего, однако создает и изменяет коллекцию и ее кнопку в меню.
    """

    # Эта второстепенная функция, которая срабатыват, когда пользователь
    # готов создать коллекцию и кликает на кнопку "Готово". 
    def the_end() -> None:

        """Функция активируется при клике кнопки 'Готово' и может создать
        и изменить коллекцию."""

        # У пользователя спрашивают: "Точно готово?", т. к. можно задеть кнопку
        # случайно или увидеть неточность. 
        if messagebox.askokcancel(message="Точно хотите?", title="Точно?"):

            if all(map(lambda x: True if x != "" else False, tuple(combobox.get() for combobox in comboboxes))):  # Проверка на то, что все цвета введены (нет пустых строк).

                if name_collection.get() != "" and (flag or name_collection.get() not in [name for name in work_with_file.information_in_Collection_player()]) and " " not in name_collection.get():  # Проверка на то, что название не пустое, не повторяется и не имеет пробелов.

                    information = work_with_file.information_in_Collection_player()  # Информация о коллекциях.

                    # Добавляем коллекцию к другим.
                    information[name_collection.get()] = {
                        'окно': colors_from_ru_to_en[comboboxes[0].get()], 
                        'поле': colors_from_ru_to_en[comboboxes[1].get()], 
                        "ячейки": colors_from_ru_to_en[comboboxes[2].get()], 
                        "флажки": colors_from_ru_to_en[comboboxes[3].get()]
                    }

                    work_with_file.write_document_Collection_player(information)  # Записываем эту коллекцию в файл.
                    
                    choice_color = tk.Menu(tearoff=False)  # Создаем подменю для данной коллекции.
                    
                    # Создаем названия элементов подменю и их команды.
                    commands_activities = {
                        "Применить": partial(apply_collection, main_root, name_collection.get(), label_money), 
                        "Изменить": partial(create_collection, main_root=main_root, menu=menu, number_element=number_element, label_money=label_money, new_changes=list([name_collection.get()]+[work_with_file.information_in_Collection_player()[name_collection.get()][place] for place in work_with_file.information_in_Collection_player()[name_collection.get()]])),
                        "Информация": partial(information_about_collection, name_collection.get()),
                        "Удалить": partial(delete_collection, menu, number_element, main_root, label_money)
                    }

                    # Добавляем элементы в подменю.
                    for activity in commands_activities:

                        choice_color.add_command(label=activity, command=commands_activities[activity])

                    menu.entryconfig(number_element, label=name_collection.get(), menu=choice_color)  # Создаем в основном меню возможность взаимодействовать с коллекцией.

                    messagebox.showinfo(message="Коллекция успешно задана!", title="...")  # Выводим сообщение об успешном созданиии.

                    exit()  # Удаляем окно создания.

                else:  # Если какие-то проблемы с названием.

                    messagebox.showerror(message="Такое название уже есть, или оно пустое!", title="Ошибка!")

            else:  # Если проблемы с цветами.

                messagebox.showerror(message="Какая-то строка не заполнена!", title="Ошибка!")

    # Функция удаления окна создания коллекции.                
    def exit() -> None:

        """Функция закрывает 'подокно'."""

        root.quit()  # Завершаем действие Tcl в данном окне.
        root.destroy()  # Уничтожаем окно

        # Такая функция позволяет уничтожить "подокно", 
        # не прекращая основной цикл приложения с таймером.

    root = tk.Toplevel(master=main_root)  # Создаем "подокно".
    root.resizable(0, 0)  # Делаем его неизменяемым.

    tk.Label(master=root, text="Регистрация коллекции").pack()  # Создаем текст-название этого окна.
    tk.Label(master=root, text="Название коллекции (без_пробелов):").pack(anchor=tk.W, pady=5)

    flag = True if new_changes != None else False  # Проверка на то, происходит создание(False) или изменение(True) коллекции.
    name_collection = ttk.Entry(master=root)  # Поле ввода названия коллекции.
    if flag: name_collection.insert(0, new_changes[0])  # Если происходит изменение, то название уже будет вписано.
    name_collection.pack()

    places = ["окна", "поля", "ячеек", "флажков"]  # Варианты мест, куда будем запрашивать цвет.
    information = work_with_file.information_in_Information_about_shop()  # Информация о приобретенных цветах.
    variants = [[colors_from_en_to_ru[color] for color in information if color != "random" and int(information[color][place])] if place != "ячейки" else [colors_from_en_to_ru[color] for color in information if int(information[color][place])] for place in ["окно", "поле", "ячейки", "флажки"]]  # Варианты цветов на русском, распределены по спискам от окна до флажков.
    comboboxes = []  # Ответы пользователя насчет цветов.

    # Создание вопроса + поле ответа для него.
    for i in range(len(places)):

        tk.Label(master=root, text=f"Цвет {places[i]}:").pack(anchor=tk.W, pady=5)  # Размещение вопроса.

        choice_color = ttk.Combobox(master=root, values=variants[i])  # Создание поля для ответов.
        choice_color.pack()  # Его размещение.
        if flag: choice_color.insert(0, colors_from_en_to_ru[new_changes[i+1]])  # Если происходит изменение, то поле будет заполено уже выбранным цветом.

        choice_color["state"] = "readonly"  # Статус, позволяющий ТОЛЬКО ВЫБИРАТЬ, а не писать в поле ответов.

        comboboxes.append(choice_color)  # Сохраняем ссылку на Combobox в спец. списке, чтобы потом выяснить ответ.

    end = tk.Button(master=root, text="Готово", command=the_end)  # Кнопка отвечает за сохранение данных коллекции.
    end.pack()


    root.protocol("WM_DELETE_WINDOW", exit)  # При выходе будем выходить из Tcl и уничтожим "подокно".
    

def apply_collection(root: tk.Tk, name_collection: str, label_money: tk.Label) -> None:

    """
    Функция применяет параметры коллекции на игровое окно.
    
    Параметры:
    - root - главное окно приложения. Его цвет будем менять.
    Также оно нужно для получения поля и ячеек;
    - name_collecion - имя коллекции, параметры которой будем примнять;
    - label_money - текстовый виджет, который показывает кол-во монет пользователя.
    Раз меняется цвет главного окна, то должен поменяться и цвет виджета на нем.
    
    Возращает:
        Ничего, однако видоизменяет игровое окно."""

    info = work_with_file.information_in_Collection_player()[name_collection]  # Информация о выбранной коллекции.

    field = tuple(el for el in root.winfo_children() if type(el) == tk.Canvas)[0]  # Игрове поле приложения.
    buttons = tuple(element for element in field.winfo_children() if type(element) == tk.Button)  # Кнопки-ячейки на игровом поле.
    labels = tuple(element for element in field.winfo_children() if type(element) == tk.Label)  # Цифры на игровом поле. Если их не окрасить, то поле не поменяет цвет.

    root['bg'] = info["окно"]  # Изменяем цвет окна на указанный в коллекции.
    label_money["bg"] = info["окно"]  # Также меняем цвет и у видлжета монет.
    
    for label in labels:  # Изменяем цвет у цифр на поле (они находятся под кнопками).

        element = label
        element["bg"] = info["поле"]

    for button in buttons:  # Изменяем цвет у ячеек.

        element = button

        final_color = info["ячейки"] if info["ячейки"] != "random" else choice(("aqua", "blue", "darkviolet", "green", "grey", "lightgreen", "lightgrey", "orange", "pink", "red", "violet", "yellow", "white"))
        element.config(bg=final_color, activebackground=final_color)

    # Замена и запись в файл новых цветов окна, поля, кнопок и флажков.
    information_about_interface = work_with_file.replace_in_the_Information(["Цвет_окна", info["окно"]], ["Цвет_поля", info["поле"]], ["Цвет_ячейки", info["ячейки"]], ["Цвет_флага", info["флажки"]])
    work_with_file.write_document_Information(information_about_interface)


def information_about_collection(name_collection: str) -> None:

    """Функция показывается информацию о цветовой гамме коллекции.
    
    Параметр: name_collection - имя коллекции, чью информацию функция предоставляет.
    
    Выводит:
        Всплывающее окно, в котором рассказано о всех цветах."""

    info: dict = work_with_file.information_in_Collection_player()[name_collection]  # Словарь со всей информацией о цветах выбранной коллекции.

    messagebox.showinfo(title="А откуда информейшион? А?", message=f"Информация о коллекции:\n- окно - {colors_from_en_to_ru[info["окно"]]};\n- поле - {colors_from_en_to_ru[info["поле"]]};\n- ячейки - {colors_from_en_to_ru[info["ячейки"]]};\n- флажки - {colors_from_en_to_ru[info["флажки"]]}.")  # Выводим сообщение со всей информацией.


def delete_collection(menu: tk.Menu, number_element: int, main_root: tk.Tk, label_money: tk.Label) -> None:

    """
    Функция удаляет коллекцию, ставя на ее место кнопку по созданию новой.
    
    Параметры:
    - menu - меню, где находится кнопка с коллекцией. Ее будем видоизменять;
    - number_element - порядковый индекс кнопки с коллекцией в меню;
    - main_root - главное окно приложения. Нужно для передачи в 
    функцию creat_collection;
    - label_money - текстовый виджет, показывающий кол-во монет у пользователя.
    Нужен для передачи в функцию create_collection.
    
    Выводит:
        Удаляет данные о коллекции name_collection, убирает ее из меню 'собственных коллекций"."""

    # Сначала спрашиваем пользователя о серьёзности данного решения.
    if messagebox.askokcancel(title="Точно?", message=f'Ты точно хочешь удалить коллекцию {menu.entrycget(number_element, 'label')}'):

        choice_color = tk.Menu(tearoff=False)  # Создаем новое подменю для данной коллекции.
        choice_color.add_command(label="Создать...", command=partial(create_collection, main_root, menu, number_element, label_money))  # Создадим элемент с возможностью создания коллекции.

        info = work_with_file.information_in_Collection_player()  # Информация обо всех коллекциях.
        del info[menu.entrycget(number_element, 'label')]  # Удаляем из файла информацию о данной коллекции.
        work_with_file.write_document_Collection_player(info)  # Записываем все коллекции кроме выбранной в файл.

        menu.entryconfig(index=number_element, label="Создать...", menu=choice_color)  # Изменяем элемент меню для создания новой коллекции.

