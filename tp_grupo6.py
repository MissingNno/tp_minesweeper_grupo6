import random
import os


def generate_board(board_size: int, total_mines: int) -> tuple:
    '''inicializa la grilla de juego con "0" en todas las celdas. Se eligen de manera aleatoria
    las casillas que poseen una bomba y se añaden a la grilla con el valor "X".'''

    empty_board = [['0' for column in range(
        board_size)] for row in range(board_size)]
    mines = generate_mines(board_size, total_mines)
    for row, col in mines:
        empty_board[row][col] = 'X'
    final_board = get_numbers(empty_board)
    return (final_board, mines)


def generate_mines(board_size: int, total_mines: int) -> list:
    '''Genera una lista con posiciones aleatorias para las bombas.'''

    mines = []
    for mine in range(total_mines):
        cell = obtain_random_cell(board_size)
        while cell in mines:
            cell = obtain_random_cell(board_size)
        mines.append(cell)
    return mines


def obtain_random_cell(board_size: int) -> tuple:
    row = random.randint(0, board_size - 1)
    col = random.randint(0, board_size - 1)
    return (row, col)


def get_numbers(board: list) -> list:
    for row_number, row in enumerate(board):
        for col_number, cell in enumerate(row):
            if cell != 'X':
                board[row_number][col_number] = str(len(['X' for x, y in obtain_neighbors(
                    board, row_number, col_number) if board[x][y] == 'X']))
    return board


def obtain_neighbors(board: list, row_number: int, col_number: int) -> list:
    max_position = len(board)
    neighbors = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            elif max_position > (row_number + x) > -1 and max_position > (col_number + y) > -1:
                neighbors.append((row_number + x, col_number + y))
    return neighbors


def show_board(board: list) -> None:
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    board_size = len(board)
    top = '    '
    line_h = '    ' + (4 * board_size * '-') + '-'
    for letter in letters[:board_size]:
        top = top + '  ' + letter + ' '
    print(top + '\n' + line_h)
    for index, i in enumerate(board):
        row = '{0:3} |'.format(index + 1)
        for j in i:
            row = row + ' ' + j + ' |'
        print(row + '\n' + line_h)
    print('')


def end_game():
    print('aa')


def checkForBombs(user_input, board):
    row, col = user_input
    if board[row][col] == 'X':
        print(
            f"Perdiste el juego, la casilla fila: {row}, columna: {col} tenía una bomba \U0001F615 \n")
        show_board(board)
        end_game()
    else:
        print('seguimos')
        # funcion de facu que revela casillas


# Programa principal
board_size = 10
total_mines = 20


board, mines = generate_board(board_size, total_mines)
last_board = [[' ' for i in range(board_size)] for i in range(board_size)]

user_input = [0, 1]
user_bomb = [0, 2]

checkForBombs(user_input, board)
