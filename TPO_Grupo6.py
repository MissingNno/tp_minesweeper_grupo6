import random
import time
import math

def generate_board(board_size, total_mines):
    '''inicializa la grilla de juego con "0" en todas las celdas. Se eligen de manera aleatoria
    las casillas que poseen una bomba y se añaden a la grilla con el valor "X".'''

    empty_board = [['0' for column in range(board_size)] for row in range(board_size)]
    mines = generate_mines(board_size, total_mines)
    for row, col in mines:
        empty_board[row][col] = 'X'
    final_board = get_numbers(empty_board)
    print(final_board)
    return (final_board, mines)


def generate_mines(board_size, total_mines):
    '''Genera una lista con posiciones aleatorias para las bombas.'''

    mines = []
    for mine in range(total_mines):
        cell = obtain_random_cell(board_size)
        while cell in mines:
            cell = obtain_random_cell(board_size)
        mines.append(cell)
    return mines


def obtain_random_cell(board_size):
    row = random.randint(0, board_size - 1)
    col = random.randint(0, board_size - 1)
    return (row, col)


def get_numbers(board):
    for row_number, row in enumerate(board):
        for col_number, cell in enumerate(row):
            if cell != 'X':
                board[row_number][col_number] = str(len(['X' for x, y in obtain_neighbors(
                    board, row_number, col_number) if board[x][y] == 'X']))
    return board


def obtain_neighbors(board, row_number, col_number):
    max_position = len(board)
    neighbors = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            elif max_position > (row_number + x) > -1 and max_position > (col_number + y) > -1:
                neighbors.append((row_number + x, col_number + y))
    return neighbors


def show_board(board,letters):
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


def save_scoreboard(username,user_time):
    '''Guarda el tiempo que tardo cada usuario en ganar la partida'''
    try:
        arch = open('scoreboard.txt', 'at')
        arch.write(username.capitalize() + ";" + str(user_time) + " segundos" + "\n")

    except OSError as msg:
        print('No se pudo grabar el archivo', msg)
    finally:
        try:
            arch.close()
        except NameError:
            pass


def recover_scoreboard():
    try:
        arch = open('scoreboard.txt', 'rt')
        game_data = arch.readline()
        while game_data:
            splitted_game_data = game_data.split(';')
            splitted_game_data[-1] = splitted_game_data[-1].rstrip("\n")
            username, user_time = splitted_game_data
            print("Usuario: ", username + " - Tiempo: ", user_time)
            game_data = arch.readline()
        return 
    except FileNotFoundError as msg:
        print('Todavia no existe tabla de ganadores, pero puedes ser el primero!')
    except OSError as msg:
        print('No se pudo leer el archivo', msg)
    finally:
        try:
            arch.close()
        except NameError:
            pass


def check_for_bombs(user_input, board, mines,letters):
    row, col = user_input
    game_lost = False

    if user_input in mines:
        print(
            f"Perdiste el juego, la casilla fila: {row}, columna: {col} tenía una bomba \U0001F615 \n")
        show_board(board,letters)
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


def validate_input(data, board_size,letters):
    cell = ()
    flag = False
    try:
        last_char = data[-1].upper()
        first_char = data[0]
        row_number = ""
        assert first_char.isalpha() and (
            first_char.upper() in letters[:board_size])

        if len(data) > 1 and len(data) < 5:
            if last_char == "F":
                row_number = data[1:-1]
                flag = True
            else:
                row_number = data[1:]
            assert int(row_number) >= 1 and int(row_number) <= board_size
        else:
            raise ValueError
        cell = (int(row_number)-1, int(letters.index(first_char.upper())))
    except (ValueError, AssertionError,IndexError):
        print("Casilla inválida.")
    return {"cell": cell, "flag": flag}


def set_difficulty():
    difficulty = input("Seleccione la dificultad (F/M/D): ").upper()
    board_size=0
    total_mines=0
    if difficulty=="F":
        board_size=5
        total_mines=5
    elif difficulty=="M":
        board_size=10
        total_mines=15
    elif difficulty=="D":
        board_size=15
        total_mines = 20
    else: 
        print("Debe ingresar una opcion valida\n")
        set_difficulty()
    return (board_size,total_mines)


print()
print("Buscaminas - Juego Realizado por Grupo 6".center(100, "*"), end="\n\n")
board_size, total_mines = set_difficulty()
print()
real_board, mines_in_board = generate_board(board_size, total_mines)
flags = []
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
start_time = time.time()

last_board = [[' ' for i in range(board_size)] for i in range(board_size)]

show_board(last_board,letters)
message = "Instrucciones:\n" + \
    "> Escriba la columna y luego la fila (ej. c4).\n" + \
    "> Para colocar o quitar una bandera, agrege 'f' a la celda (ej. a5f).\n" + \
    "> Escriba scoreboard para mostrar la tabla de ganadores.\n" + \
    "> Presione Ctrl + c para salir."

print(message)
try:
    view_scoreboard = input("Desea ver la tabla de ganadores? S/N ").upper()
    if view_scoreboard == "S": recover_scoreboard()
    while True:
        mines_left = total_mines - len(flags)
        data = input('Ingresar Celda ({} minas restantes): '.format(mines_left))
        result = validate_input(data, board_size,letters)

        cell = result['cell']


        if cell:
            print('\n\n')
            row, col = cell
            selected_cell = last_board[row][col]
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
                        flags.append(cell)

                else:
                    print('No se puede poner una bandera porque la casilla ya fue revelada.')
                    continue
            elif cell in flags:
                print('No se puede revelar esta casilla porque tiene una bandera')
                continue
            elif check_for_bombs(cell, real_board, mines_in_board,letters):
                break
            else:
                reveal_cells(real_board, last_board, row, col)

            if set(flags) == set(mines_in_board):
                print(
                    'Ganaste!'
                )
                show_board(real_board,letters)
                end_time = time.time()
                elapsed = math.floor(end_time - start_time) 
                save_scoreboard(input("ingrese su nombre: "),str(elapsed))
                break

        show_board(last_board,letters)
        print(message)

except KeyboardInterrupt:
    show_board(real_board,letters)
    print('¡Te rendiste! \U0001F615 ')
