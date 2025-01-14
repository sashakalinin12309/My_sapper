def create_Information_about_shop() -> None:

    """Функция создает первоначальный документ Information_about_shop.txt"""

    # Открываем/создаем нужный нам файл.
    with open("data_about_player\\Information_about_shop.txt", "w", encoding="UTF-8") as file:

        # Все возможные цвета, которые предусмотрены в магазине.
        text = (
            "red", "orange", "yellow", 
            "lightgreen", "green", "aqua", 
            "blue", "violet", "darkviolet", 
            "pink", "lightgrey", "grey", 
            "white", "random"
        )
        
        # Перебираем цвета.
        for color in text:

            print(color, file=file, end=" ")  # Записываем в файл сначала цвет.

            # Если цвет из классики, он автоматически приобретен у окна, поля, кнопок.
            if color == "lightgrey" or color == 'grey' or color == "white":

                print("окно:1", file=file, end=" ")
                print("поле:1", file=file, end=" ")
                print("ячейки:1", file=file, end=" ")
                print("флажки:0", file=file)
            
            # Красный же автоматически приобретен у флажков.
            elif color == "red":

                print("окно:0", file=file, end=" ")
                print("поле:0", file=file, end=" ")
                print("ячейки:0", file=file, end=" ")
                print("флажки:1", file=file)

            # А цвет random есть только у кнопок (но его нужно еще купить).
            elif color == "random":

                print("ячейки:0", file=file)

            # А у всех остальных все по 0.
            else:

                print("окно:0", file=file, end=" ")
                print("поле:0", file=file, end=" ")
                print("ячейки:0", file=file, end=" ")
                print("флажки:0", file=file)
            
def create_Information() -> None:

    """Функция создает первоначальный документ Information.txt"""

    # Открываем/создаем нужный нам файл.
    with open("data_about_player\\Information.txt", "w", encoding="UTF-8") as Information:
        
        # Решил, что удобнее записать впринципе уже готовый шаблон,
        # т. к. не вижу здесь какой-либо закономерности. 
        print("Размер_поля:9", file=Information)
        print("Монеты:0", file=Information)
        print("Рекорд_9:нет_результата", file=Information)
        print("Рекорд_15:нет_результата", file=Information)
        print("Рекорд_21:нет_результата", file=Information)
        print("Цвет_окна:lightgrey", file=Information)
        print("Цвет_поля:grey", file=Information)
        print("Цвет_ячейки:lightgrey", file=Information)
        print("Цвет_флага:red", file=Information)

def create_Collection_player() -> None:

    """Функция создает первоначальный документ Collection_player.txt
    P. S. Он должен быть пустым..."""

    # Конечно. открываем файл, но...
    with open("data_about_player\\Collection_player.txt", "w", encoding="UTF-8") as collection_player:

        ...  # ... но, по задумке, он должен быть пустой.
