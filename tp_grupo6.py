import random
import time
import os

def generate_board(board_size: int, total_mines: int) -> tuple:
    '''inicializa la grilla de juego con "0" en todas las celdas. Se eligen de manera aleatoria
    las casillas que poseen una bomba y se añaden a la grilla con el valor "X".'''

    empty_board = [['0' for column in range(board_size)] for row in range(board_size)]
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
                board[row_number][col_number] = str(len(['X' for x,y in obtain_neighbors(board, row_number, col_number) if board[x][y] == 'X' ]))
    return board

def obtain_neighbors(board: list, row_number: int, col_number: int) -> list:
    max_position = len(board)
    neighbors = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0: continue
            elif max_position > (row_number + x) > -1 and max_position > (col_number + y) > -1:
                neighbors.append((row_number + x, col_number + y))
    return neighbors

def show_board(board: list, letters: list) -> None:
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

def reveal_cells(full_board,current_board,row,col):
    if current_board[row][col] != ' ': return
    current_board[row][col] = full_board[row][col]
    if full_board[row][col]=='0':
        for f,c in obtain_neighbors(full_board,row,col):
            if current_board[f][c] != 'F':
                reveal_cells(full_board,current_board,f,c)

def validate_input(data,board_size):
    cell = ()
    flag = False
    if len(data) >= 1 and len(data) <= 3:
        if data[0].upper() in letters[:board_size]:
            if data[1].isnumeric() and 0 < int(data[1]) <= board_size:
                cell = (int(letters.index(data[0].upper())),int(data[1])-1)
                if len(data) == 3:
                    if data[2].upper() == 'F':
                        flag = True
    
    return {"cell": cell,"flag":flag}


board_size = 10
total_mines = 20
get_board, get_mines = generate_board(board_size,total_mines)
flags = []
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

last_board = [[' ' for i in range(board_size)] for i in range(board_size)]

print()
print("Buscaminas - Juego Realizado por Grupo 11".center(100,"*"),end="\n\n")
show_board(last_board,letters)
message = "Instrucciones:\n" + "> Escriba la columna y luego la fila (ej. c4).\n" + "> Para colocar o quitar una bandera, agrege 'f' a la celda (ej. a5f)."
print(message)

while True:
        mines_left = total_mines - len(flags)
        data = input('Ingresar Celda ({} minas restantes): '.format(mines_left))
        result = validate_input(data, board_size)

        cell = result['cell']
        print(cell)

        if cell:
            print('\n\n')
            col, row = cell
            selected_cell = last_board[row][col]
            flag = result['flag']

            if flag:
                if selected_cell == ' ':
                    last_board[row][col] = 'F'
                    flags.append(cell)
                elif selected_cell == 'F':
                    last_board[row][col] = ' '
                    flags.remove(cell)
                else:
                    message = 'No se puede colocar una bandera aqui'

            # If there is a flag there, show a message
            elif cell in flags:
                message = 'Ya existe una bandera en esa casilla'

            elif get_board[row][col] == 'X':
                print('Has Perdido!\n')
                show_board(get_board,letters)
                #if playagain():
                    #playgame()
                #return

            elif selected_cell == ' ':
                reveal_cells(get_board, last_board, row, col)

            else:
                message = "Esta celda ya ha sido revelada!"

            if set(flags) == set(get_mines):
                print(
                    'Ganaste!'
                    #'It took you {} minutes and {} seconds.\n'.format(minutes,seconds)
                    )
                show_board(get_board,letters)
                #if playagain():
                    #playgame()
                #return

        show_board(last_board,letters)
        print(message)
