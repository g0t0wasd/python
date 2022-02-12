from random import shuffle
from tkinter import Canvas, Tk

BOARD_SIZE = 4
SQUARE_SIZE = 80
EMPTY_SQUARE = BOARD_SIZE ** 2

root = Tk()
root.title("Pythonicway Fifteen")

c = Canvas(root, width=BOARD_SIZE * SQUARE_SIZE,
           height=BOARD_SIZE * SQUARE_SIZE, bg='#808080')
c.pack()


def get_inv_count():
    """ Функция считающая количество перемещений """
    inversions = 0
    inversion_board = board[:]
    inversion_board.remove(EMPTY_SQUARE)
    for i in range(len(inversion_board)):
        first_item = inversion_board[i]
        for j in range(i+1, len(inversion_board)):
            second_item = inversion_board[j]
            if first_item > second_item:
                inversions += 1
    return inversions


def is_solvable():
    """ Функция определяющая имеет ли головоломка рещение """
    num_inversions = get_inv_count()
    if BOARD_SIZE % 2 != 0:
        return num_inversions % 2 == 0
    else:
        empty_square_row = BOARD_SIZE - (board.index(EMPTY_SQUARE) // BOARD_SIZE)
        if empty_square_row % 2 == 0:
            return num_inversions % 2 != 0
        else:
            return num_inversions % 2 == 0


def get_empty_neighbor(index):
    # получаем индекс пустой клетки в списке
    empty_index = board.index(EMPTY_SQUARE)
    # узнаем расстояние от пустой клетки до клетки по которой кликнули
    abs_value = abs(empty_index - index)
    # Если пустая клетка над или под клектой на которую кликнули
    # возвращаем индекс пустой клетки
    if abs_value == BOARD_SIZE:
        return empty_index
    # Если пустая клетка слева или справа
    elif abs_value == 1:
        # Проверяем, чтобы блоки были в одном ряду
        max_index = max(index, empty_index)
        if max_index % BOARD_SIZE != 0:
            return empty_index
    # Рядом с блоком не было пустого поля
    return index


def draw_board():
    # убираем все, что нарисовано на холсте
    c.delete('all')
    # Наша задача сгруппировать пятнашки из списка в квадрат
    # со сторонами BOARD_SIZE x BOARD_SIZE
    # i и j будут координатами для каждой отдельной пятнашки
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # получаем значение, которое мы должны будем нарисовать 
            # на квадрате
            index = str(board[BOARD_SIZE * i + j])
            # если это не клетка которую мы хотим оставить пустой
            if index != str(EMPTY_SQUARE):
                # рисуем квадрат по заданным координатам
                c.create_rectangle(j * SQUARE_SIZE, i * SQUARE_SIZE,
                                   j * SQUARE_SIZE + SQUARE_SIZE,
                                   i * SQUARE_SIZE + SQUARE_SIZE,
                                   fill='#43ABC9',
                                   outline='#FFFFFF')
                # пишем число в центре квадрата
                c.create_text(j * SQUARE_SIZE + SQUARE_SIZE / 2,
                              i * SQUARE_SIZE + SQUARE_SIZE / 2,
                              text=index,
                              font="Arial {} italic".format(int(SQUARE_SIZE / 4)),
                              fill='#FFFFFF')


def show_victory_plate():
    # Рисуем черный квадрат по центру поля
    c.create_rectangle(SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 - 10 * BOARD_SIZE,
                       BOARD_SIZE * SQUARE_SIZE - SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 + 10 * BOARD_SIZE,
                       fill='#000000',
                       outline='#FFFFFF')
    # Пишем красным текст Победа
    c.create_text(SQUARE_SIZE * BOARD_SIZE / 2, SQUARE_SIZE * BOARD_SIZE / 1.9,
                  text="ПОБЕДА!", font="Helvetica {} bold".format(int(10 * BOARD_SIZE)), fill='#DC143C')


def click(event):
    # Получаем координаты клика
    x, y = event.x, event.y
    # Конвертируем координаты из пикселей в клеточки
    x = x // SQUARE_SIZE
    y = y // SQUARE_SIZE
    # Получаем индекс в списке объекта по которому мы нажали
    board_index = x + (y * BOARD_SIZE)
    # Получаем индекс пустой клетки в списке. Эту функцию мы напишем позже
    empty_index = get_empty_neighbor(board_index)
    # Меняем местами пустую клетку и клетку, по которой кликнули
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    # Перерисовываем игровое поле 
    draw_board()
    # Если текущее состояние доски соответствует правильному - рисуем сообщение о победе
    if board == correct_board:
        # Эту функцию мы добавим позже
        show_victory_plate()


c.bind('<Button-1>', click)
c.pack()


board = list(range(1, EMPTY_SQUARE + 1))
correct_board = board[:]
shuffle(board)

while not is_solvable():
    shuffle(board)

draw_board()
root.mainloop()
