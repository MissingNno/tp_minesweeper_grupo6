import random
import os

def minesweeper_initial_board(board_size: int, total_mines: int) -> tuple:
    '''inicializa la grilla de juego con "0" en todas las celdas. Se eligen de manera aleatoria
    las casillas que poseen una bomba y se añaden a la grilla con el valor "X".'''

    empty_board = [['0' for column in range(board_size)] for row in range(board_size)]
    mines = generate_mines(empty_board, total_mines)
    for row, col in mines:
        empty_board[row][col] = 'X'
    return (empty_board, mines)

def generate_mines(empty_board: list, total_mines: int) -> list:
    '''Genera una lista con posiciones aleatorias para las bombas.'''
    
    mines = []
    for mine in range(total_mines):
        cell = obtain_random_cell(empty_board)
        while cell in mines:
            cell = obtain_random_cell(empty_board)
        mines.append(cell)
    return mines

def obtain_random_cell(board: list) -> tuple:
    board_size = len(board)
    row = random.randint(0, board_size - 1)
    col = random.randint(0, board_size - 1)
    return (row, col)

def getnumbers(board: list) -> list:
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

board_size = 7
total_mines = 10
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

last_board = [[' ' for i in range(board_size)] for i in range(board_size)]
board = []
flags = []

show_board(last_board,letters)
