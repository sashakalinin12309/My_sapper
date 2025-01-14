def create_minefield(size: int) -> list:

    """
    Функция создает матрицу size x size (9x9, 15x15 или 21х21), которая будет основой минного
    поля.

    Параметры функции:
        size: int - ширина и длина матрицы.
    
    Возвращает:
        minefield: list - матрица с цифрами и бомбами, само поле.
    """
    
    import random  # Импортируем модуль random

    counter_bombs: int = 0  # Переменная, отвечающая за кол-во бомбочек в поле.

    # Вычисляем те места, где не будет бомб (посередине и соседние).
    # Выясняем кол-во бомб, которое будет зависеть размера поля.
    if size == 9:
        counter_bombs = 10
        not_bombs = ((3, 3), (3, 4), (3, 5),
                     (4, 3), (4, 4), (4, 5),
                     (5, 3), (5, 4), (5, 5))
    elif size == 15:
        counter_bombs = 35
        not_bombs = ((6, 6), (6, 7), (6, 8), 
                     (7, 6), (7, 7), (7, 8),
                     (8, 6), (8, 7), (8, 8),)
    elif size == 21:
        counter_bombs = 99
        not_bombs = ((9, 9), (9, 10), (9, 11), 
                    (10, 9), (10, 10), (10, 11),
                    (11, 9), (11, 10), (11, 11))

    minefield = [[0 for _ in range(size)] for _ in range(size)]  # Создаем основу для поля.
    arithmetic_operations = ('-1' , '-0', '+1')  # Этот кортеж нужен будет для вычисления кол-ва бомб вокруг клетки.

    # В случайном порядке узнаем координаты бомбочек.
    check_list = set(())  # Множество, в котором будут сохранены все НЕПОВТОРЯЮЩИЕСЯ координаты.
    while len(check_list) != counter_bombs:  # Пока число координат бомб не равно кол-ву бомб...
        coordinates = tuple(random.randint(0, size-1) for _ in range(2))  # Кортеж с х и у.
        # Проверка на то, что бомбы не будут расположены в зоне, где начинаем игру.
        if coordinates not in not_bombs:
            check_list.add(coordinates)

    bombs_list = tuple(check_list)  # Для удобства превращаем множество в кортеж.
    # Распологаем бомбочки на матрице.
    for coordinates in bombs_list:
        x, y = coordinates[0], coordinates[1]
        minefield[x][y] = "💣"

    # Создаем в матрице числа для игры.
    for x in range(size):
        for y in range(size):
            if minefield[x][y] != '💣':
                counter = 0  # Счетчик для определения числа в ячейке.
                for i in range(3):
                    for j in range(3):
                        
                        # Выясняем координаты соседних клеток.
                        x_check = int(eval(str(x) + arithmetic_operations[i]))
                        y_check = int(eval(str(y) + arithmetic_operations[j]))
                        
                        # Выясняем, возможны ли такие координаты и сколько бомбочек в этих ячейках.
                        if size > x_check >= 0 and size > y_check >= 0 and minefield[x_check][y_check] == '💣':
                            counter += 1

                if counter == 0:
                    minefield[x][y] = " "  # Как бы пустая ячейка, обозначающая, что вокруг нет бомб.
                else:
                    minefield[x][y] = str(counter)  # А это уже непустая ячейка. Здесь надо быть осторожным игроку!
                
    # В итоге возращаем эту матрицу.
    return minefield

