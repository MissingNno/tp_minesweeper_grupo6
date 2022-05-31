import random
import os

def minesweeper_initial_grid(grid_size: int, total_mines: int, start: tuple) -> tuple:
    '''inicializa la grilla de juego con "0" en todas las celdas. Asigna el valor "X" a las casillas
    que poseen una bomba.'''

    empty_grid = [['0' for column in range(grid_size)] for row in range(grid_size)]
    #genera una lista con posiciones aleatorias(tuplas) para las bombas.
    mines = getmines(empty_grid, total_mines, start)
    
    for row, col in mines:
        empty_grid[row][col] = 'X'
    grid = getnumbers(empty_grid)

    return (grid, mines)

def getmines(grid: list, total_mines: int, start: tuple) -> list:
    mines = []
    neighbors = getneighbors(grid, *start)

    for i in range(total_mines):
        cell = getrandomcell(grid)
        while cell == start or cell in mines or cell in neighbors:
            cell = getrandomcell(grid)
        mines.append(cell)

    return mines

def getrandomcell(grid: list) -> tuple:
    grid_size = len(grid)
    row = random.randint(0, grid_size - 1)
    col = random.randint(0, grid_size - 1)

    return (row, col)

def getnumbers(grid: list) -> list:
    for rowno, row in enumerate(grid):
        for colno, cell in enumerate(row):
            if cell != 'X':
                # obtiene los valores de los vecinos
                values = [grid[r][c] for r, c in getneighbors(grid, rowno, colno)]

                # cuenta cuantas son minas
                grid[rowno][colno] = str(values.count('X'))

    return grid

def getneighbors(grid: list, rowno: int, colno: int) -> list:
    gridsize = len(grid)
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                neighbors.append((rowno + i, colno + j))

    return neighbors
