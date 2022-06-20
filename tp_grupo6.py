from os import PRIO_PGRP
import random


def generate_board(board_size: int, total_mines: int) -> tuple:
    '''inicializa la grilla de juego con "0" en todas las celdas. Se eligen de manera aleatoria
    las casillas que poseen una bomba y se añaden a la grilla con el valor "X".'''

    empty_board = [['0' for column in range(
        board_size)] for row in range(board_size)]
    mines = [(0, 1), (0, 2), (0, 6)]
    for row, col in mines:
        empty_board[row][col] = 'X'
    final_board = [['2', 'X', 'X', '1', '0', '1', 'X', '2', '0', '1'],
                   ['3', '0', '5', '3', '1', '2', '2', '3', '2', '1'],
                   ['2', '0', '0', '2', '0', '2', '3', '0', '2', '0'],
                   ['1', '3', '3', '4', '2', '4', '0', '0', '2', '0'],
                   ['0', '1', '0', '2', '0', '3', '0', '4', '2', '0'],
                   ['0', '1', '1', '2', '1', '2', '2', '0', '1', '0'],
                   ['0', '0', '0', '0', '1', '2', '3', '3', '2', '1'],
                   ['0', '0', '0', '0', '1', '0', '0', '3', '0', '2'],
                   ['0', '0', '0', '0', '1', '2', '3', '4', '0', '2'],
                   ['0', '0', '0', '0', '0', '0', '1', '0', '2', '1']
                   ]

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


def save_game(board, user_name='user'):
    '''Guarda cada tablero como un registro.'''
    try:
        arch = open(f'{user_name}.txt', 'wt')

        stringyfied_board = ";".join([(str(row)) for row in board])
        arch.write(stringyfied_board + "\n")

    except OSError as msg:
        print('No se pudo grabar el archivo', msg)
    finally:
        try:
            arch.close()
        except NameError:
            pass


def recover_game(user_name, game_number):
    try:
        arch = open(f'{user_name}.txt', 'rt')
        saved_board = arch.readline()
        board_counter = 1

        while saved_board and board_counter != game_number:
            board_counter += 1

        assert saved_board
        new_board = list([list(row) for row in saved_board])
        return new_board

    except FileNotFoundError as msg:
        print('No se pudo abrir el archivo', msg)
    except OSError as msg:
        print('No se pudo leer el archivo', msg)
    except AssertionError:
        print(f'No existe el juego número {game_number} en nuestros registros')
    finally:
        try:
            arch.close()
        except NameError:
            pass


def check_for_bombs(user_input, board, mines):
    row, col = user_input
    game_lost = False

    if user_input in mines:
        print(
            f"Perdiste el juego, la casilla fila: {row}, columna: {col} tenía una bomba \U0001F615 \n")
        show_board(board)
        game_lost = True
    return game_lost


def reveal_cells(full_board, current_board, row, col):
    if current_board[row][col] != ' ':
        return
    current_board[row][col] = full_board[row][col]
    if full_board[row][col] == '0':
        for f, c in obtain_neighbors(full_board, row, col):
            if current_board[f][c] != 'F':
                reveal_cells(full_board, current_board, f, c)


def validate_input(data, board_size):
    cell = ()
    flag = False
    if len(data) > 1 and len(data) <= 4:
        if data[0].upper() in letters[:board_size]:
            if data[1].isnumeric() and 0 < int(data[1]) <= board_size:
                cell = (int(data[1])-1, int(letters.index(data[0].upper())))
                if len(data) == 4:
                    print('entra')
                    cell = (int(data[1] + data[2])-1,
                            int(letters.index(data[0].upper())))
                if data[-1] == 'f':
                    flag = True

    return {"cell": cell, "flag": flag}


board_size = 10
total_mines = 20
get_board, get_mines = generate_board(board_size, total_mines)
flags = []
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

last_board = [[' ' for i in range(board_size)] for i in range(board_size)]

print()
print("Buscaminas - Juego Realizado por Grupo 11".center(100, "*"), end="\n\n")
show_board(last_board)
message = "Instrucciones:\n" + \
    "> Escriba la columna y luego la fila (ej. c4).\n" + \
    "> Para colocar o quitar una bandera, agrege 'f' a la celda (ej. a5f)."
print(message)

while True:
    mines_left = total_mines - len(flags)
    data = input('Ingresar Celda ({} minas restantes): '.format(mines_left))
    result = validate_input(data, board_size)

    cell = result['cell']

    if cell:
        print('\n\n')
        row, col = cell
        print('cell', cell)
        selected_cell = last_board[row][col]
        print('seleted', selected_cell)
        flag = result['flag']
        can_be_flagged = selected_cell == ' ' or selected_cell == 'F'

        if flag:
            if can_be_flagged:
                if cell in flags:
                    remove = input(
                        'Ya existe una bandera en esa casilla, ingrese "si" para quitarla: ')
                    if remove == 'si':
                        last_board[row][col] = ' '
                        flags.remove(cell)

                else:
                    last_board[row][col] = 'F'
                    # unicode for flag \U0001F6A9
                    flags.append(cell)

            else:
                print('No se puede poner una bandera porque la casilla ya fue revelada.')
                continue
        elif cell in flags:
            print('No se puede revelar esta casilla porque tiene una bandera')
            continue
        elif check_for_bombs(cell, get_board, get_mines):
            break
        else:
            reveal_cells(get_board, last_board, row, col)

        if set(flags) == set(get_mines):
            print(
                'Ganaste!'
            )
            show_board(get_board)
            break
            # if playagain():
            # playgame()
            # return

    show_board(last_board)
    print(message)
