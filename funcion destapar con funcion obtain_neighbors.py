
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
