def matriz(filas,columnas,caracter):
    tablero = []
    for i in range(0,filas):
        a = [caracter]*columnas
        tablero.append(a)
    return tablero

def obtain_neighbors(board: list, row_number: int, col_number: int) -> list:
    max_position = len(board)
    neighbors = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0: continue
            elif max_position > (row_number + x) > -1 and max_position > (col_number + y) > -1:
                neighbors.append((row_number + x, col_number + y))
    return neighbors

def destapar(lista,fil,col,nuevo):
    nuevo[fil][col] = lista[fil][col]
    vecinos=obtain_neighbors(lista,fil,col)
    if lista[fil][col]==0:
        filas=len(vecinos)
        for f in range(filas):
            if (lista[vecinos[f][0]][vecinos[f][1]]==0) and (nuevo[vecinos[f][0]][vecinos[f][1]]!= 0):
                destapar(lista,vecinos[f][0],vecinos[f][1],nuevo)
            else:
                nuevo[vecinos[f][0]][vecinos[f][1]] = lista[vecinos[f][0]][vecinos[f][1]]

def imprimirmatriz(matriz):
    filas=len(matriz)
    columnas=len(matriz[0])
    for f in range(filas):
        for c in range(columnas):
            print("%3s" %matriz[f][c], end=" ")
        print()



tableroprueba=[[0, 0, 0, 0, 0], [0, 1, 2, 2, 1], [0, 1, True, True, 1], [0, 1, 2, 3, 2], [0, 0, 0, 1, True]]                
nuevooculto=matriz(5,5,".")
imprimirmatriz(nuevooculto)
fila=int(input("ingrese fila a destapar: "))
columna=int(input("ingrese columna a destapar: "))
destapar(tableroprueba,fila,columna,nuevooculto)
print("tablero destapando: ")
imprimirmatriz(nuevooculto)