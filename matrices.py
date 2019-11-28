
def matriz(n):     #Crea una matirziz de orden n
    listVars = [chr(x) for x in range(192, 192 + (n*n))]
    matriz = []
    for i in range(n):
        matriz.append([0]*n)
    return matriz

def nameLetProp(mat, n):     #Cambia los valores de la matriz a su respectivo indice
    listVars = [chr(x) for x in range(192, 192 + (n*n))]
    cont = 0
    for i in range(n):
        for j in range(n):
            #mat[i][j] = "a"+str(i+1)+str(j+1)
            mat[i][j] = listVars[cont]
            cont += 1

def atomos(n):
    letProp = [chr(x) for x in range(192, 192 + (n*n))]
    return letProp

def tabAjedrez(n):    #Combina las 2 funciones en una
    mat = matriz(n)
    nameLetProp(mat, n)
    return mat

def printVars(vars):    #Imprime las Varables de forma ordenada
    for i in vars:
        print(i)

def regHor(mat):
    reg = ""
    i=0
    j=0
    h=0
    n = len(mat)
    while i != n:
        if (h == n-1) and (j == n-1):
            i = i+1
            j = 0
            h = 0
        elif j == n-1:
            reg = reg + "("+"-"+mat[i][h]+"O"+"-"+mat[i][j]+")Y"
            j = 0
            h = h+1
        elif mat[i][h] == mat[i][j]:
            j = j+1
        else:
            reg = reg + "("+"-"+mat[i][h]+"O"+"-"+mat[i][j]+")Y"
            j = j+1
    reg = reg[:len(reg) - 1]
    return reg

def regVer(mat):
    reg = ""
    i=0
    j=0
    h=0
    n = len(mat)
    while j != n:
        if (i == n-1) and (h == n-1):
            j = j+1
            h=0
            i=0
        elif h == n-1:
            reg = reg + "(-"+mat[i][j]+"O-"+mat[h][j]+")Y"
            h=0
            i = i+1
        elif mat[i][j] == mat[h][j]:
            h = h+1
        else:
            reg = reg + "(-"+mat[i][j]+"O-"+mat[h][j]+")Y"
            h = h+1
    reg = reg[:len(reg)-1]
    return reg
"""
def newRegHor(mat):
    reg = ""
    i=0
    j=0
    h=0
    f=0
    n = len(mat)
    reg = reg +"(-"+mat[i][j]+"O-"+mat[h][f]+")Y"
"""
