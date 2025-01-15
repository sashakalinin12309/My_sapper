# Импортируем все нужные нам модули.
from tkinter import messagebox
from my_modules.create_files import create_Information_about_shop, create_Information, create_Collection_player

def information_in_Information_about_shop() -> dict:

    """
    Функция возращает информацию из файла Information_about_shop.txt
    в виде словаря {параметр: значение} 

    Параметры:
        нет

    Возращает:
        information - информацию в виде словаря
    """
    
    # Исключение создано для того, чтобы создать файл, если его не будет.
    try:
        
        # Открываем файл Information_about_shop.txt.
        with open("data_about_player//Information_about_shop.txt", "r", encoding="UTF-8") as information_about_shop:

            # Собираем всю информацию из файла в виде словаря
            # {цвет: {окно:0/1, поле:0/1, ячейки:0/1, флажки:0/1}};
            # (0 - не куплен, 1 - куплен). 
            information = {element_shop[0]: {place[0]: place[1] for place in map(lambda x: x.split(":"), element_shop[1:])} for element_shop in map(lambda x: x.split(), information_about_shop.readlines())}

    except FileNotFoundError:  # Файл почему-то не найден.

        create_Information_about_shop()  # Сразу же создаем такой файл.

        # Выводим сообщение об ошибке и сожалении. что весь прогресс утерян.
        messagebox.showerror(title="Ошибка!", message="Файл с твоими цветами для игры почему-то не найден...\nПоэтому все заново!")

        # Однако, всё же открываем файл.
        with open("data_about_player//Information_about_shop.txt", "r", encoding="UTF-8") as information_about_shop:

            # Забираем всю информацию.
            information = {element_shop[0]: {place[0]: place[1] for place in map(lambda x: x.split(":"), element_shop[1:])} for element_shop in map(lambda x: x.split(), information_about_shop.readlines())}

    return information  # Возращаем словарь.

def information_in_Information() -> dict:

    """
    Функция возращает информацию из файла Information.txt
    в виде словаря {параметр: значение} 

    Параметры:
        нет

    Возращает:
        information - информацию в виде словаря
    """
    # Исключение создано для того, чтобы создать файл, если его не будет.
    try:
        
        # Открываем файл Information.txt.
        with open("data_about_player//Information.txt", "r", encoding="UTF-8") as information:

            # Собираем всю информацию в словарь.
            information_about_game = {value[0]: value[1] for value in list(map(lambda x: x.strip("\n").split(":"), information.readlines())) if value != " "}

    except FileNotFoundError:  # Если файл не найден.
        
        create_Information()  # Сразу же создаем файл.

        # Выводим сообщение об ошибке.
        messagebox.showerror(title="Ошибка!", message="Файл с твоей информацией в игре почему-то не найден...\nПоэтому все заново!")

        # Открываем уже созданный файл.
        with open("data_about_player//Information.txt", "r", encoding="UTF-8") as information_about_shop:

            # Собираем всю информацию.
            information = {element_shop[0]: {place[0]: place[1] for place in map(lambda x: x.split(":"), element_shop[1:])} for element_shop in map(lambda x: x.split(), information_about_shop.readlines())}

    # Возращаем нужную информацию в виде словаря.
    return information_about_game

def replace_in_the_Information(*element_and_replacement: list) -> dict:

    """
    Функция создает словарь с информацией и заменяет в нем параметры,
    указанные в списках *element_and_replacement [параметр, новое_значение]

    Параметры:
        *element_and_replacement - списки с новыми значениями параметров в
        в виде [параметр, новое_значение]
    
    Возращает:
        Видоизменненый словарь информации в файле Information.txt для 
        дальнейшей замены в виде переписи файла.
    """
    
    # Исключение вызовется при отсутствии файла.
    try:

        # Открываем файл Information.txt
        with open("data_about_player//Information.txt", 'r', encoding="UTF-8") as information:
            
            # записываем информацию в словарь.
            information_about_game = {value[0]: value[1] for value in list(map(lambda x: x.strip("\n").split(":"), information.readlines())) if value != " "}

    except FileNotFoundError:  # Если файл не обнаружен.

        create_Information()  # Создаем нужный файл.

        # Выводим собщение об ошибке.
        messagebox.showerror(title="Ошибка", message="Почему-то файл с твоей информацией не найден...\nВидимо, все сначала!")

        # Открываем нужный файл.
        with open("data_about_player//Information.txt", 'r', encoding="UTF-8") as information:
            
            # Записываем всю информацию в словарь.
            information_about_game = {value[0]: value[1] for value in list(map(lambda x: x.strip("\n").split(":"), information.readlines())) if value != " "}

    # Перебираем всё содержимое словаря.
    for couple in element_and_replacement:

        information_about_game[couple[0]] = couple[1]  # Производим замену.

    return information_about_game  # Выводим изменённый словарь.

def write_document_Information(dict_with_information: dict) -> None:

    """
    Функция записывает в файл Information.txt новую информацию

    Параметры:
        dict_with_Information - словарь {параметр: значение} для записи
        в таком же виде в файле

    Возращает: ничего
    """

    # Открываем файл Information.txt в режиме записи (всё содержимое стёрто).
    # Файл в любом случае будет обнаружен, т. к. такой режим позволяет его 
    # создать при отсутствии. 
    with open("data_about_player//Information.txt", 'w', encoding="UTF-8") as information:

        # Производим запись в файл содержимое переданного в параметре словаря.
        for element in dict_with_information:
            print(f"{element}:{dict_with_information[element]}", file=information)


def write_document_Information_about_shop(dict_with_colors: dict) -> None:

    """
    Функция записывает в файл Information_about_shop.txt новую информацию

    Параметры:
        dict_with_Information - словарь {параметр: значение} для записи типа
        color окно:meaning поле:meaning ячейки:meaning флажки:meaning

    Возращает: ничего
    """

    # Открываем файл Information_about_shop.txt в режиме перезаписи.
    # Файл в любом случае будет обнаружен, т. к. такой режим позволяет его 
    # создать при отсутствии.
    with open("data_about_player//Information_about_shop.txt", "w", encoding="UTF-8") as information_about_shop:
        
        # Произвдим запись.
        for element in dict_with_colors:  # Перебираем все цвета.
            print(element, file=information_about_shop, end=" ")  # Записываем цвет.
            for place in dict_with_colors[element]:  # Перебираем места, куда можно применить цвета.
                print(f"{place}:{dict_with_colors[element][place]}", file=information_about_shop, end=' ' if place != "флажки" else None)  # Записываем так - место:0 (не приобретены) или 1 (приобретены).


def information_in_Collection_player() -> dict:

    """
    Функция возращает информацию из файла Collection_player в 
    виде словаря со значениями {название коллекции: {место: цвет}}.

    В случае отсутствия файла может создать его.
    """

    try:  # Исключение вызывается, если файл отсутствует.

        # Открываем файл collection_player.txt
        with open("data_about_player//Collection_player.txt", "r", encoding="UTF-8") as collection_player:
            
            # Записываем всю информацию в словарь типа
            # {название_коллекции: {окно:цвет, поле:цвет, ячейки:цвет. флажки:цвет}} 

            information = {collection[0]: {place[0]: place[1] for place in map(lambda x: x.split(":"), collection[1:])} for collection in map(lambda x: x.split(), collection_player.readlines())}

    except FileNotFoundError:  # Еслим файл не обнаружен.

        create_Collection_player()  # Создаем нужный файл.

        # Выводим сообщение об ошибке.
        messagebox.showerror(title="Ошибка!", message="Файл с твоими коллекциями для игры почему-то не найден...\nПоэтому все заново!")

        # Открываем уже созданный файл.
        with open("data_about_player//Collection_player.txt", "r", encoding="UTF-8") as collection_player:

            # Записываем всю информацию в словарь типа
            # {название_коллекции: {окно:цвет, поле:цвет, ячейки:цвет. флажки:цвет}} 
            information = {}

    return information  # Возращаем информацию в словаре.

def write_document_Collection_player(dict_with_text) -> None:

    """
    Функция записывает информацию из словаря dict_with_text 
    в файл Collection_player, оставляя только её.

    В случае отсутствия файла может создать его.
    """

    # Открываем файл .txt в режиме перезаписи.
    # Файл в любом случае будет обнаружен, т. к. такой режим позволяет его 
    # создать при отсутствии.
    with open("data_about_player//Collection_player.txt", "w", encoding="UTF-8") as collection_player:
        
        for name_collection in dict_with_text:  # Перебираем все названия коллекций.
            print(name_collection, file=collection_player, end=" ")  # Записываем выбранную коллекцию.
            for place in dict_with_text[name_collection]:  # Перебираем все места, куда могут быть применены цвета коллекции.
                print(f"{place}:{dict_with_text[name_collection][place]}", file=collection_player, end=' ' if place != "флажки" else None)  # Записываем так - место:цвет.

