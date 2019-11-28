# -*- coding: utf-8 -*-

# Subrutinas para la transformacion de una
# formula a su forma clausal

# Subrutina de Tseitin para encontrar la FNC de
# la formula en la pila
# Input: A (cadena) de la forma
#                   p=-q
#                   p=(qYr)
#                   p=(qOr)
#                   p=(q>r)
# Output: B (cadena), equivalente en FNC
def enFNC(A):
    assert(len(A)==4 or len(A)==7), u"Fórmula incorrecta!"
    B = ''
    p = A[0]
    # print('p', p)
    if "-" in A:
        q = A[-1]
        # print('q', q)
        B = "-"+p+"O-"+q+"Y"+p+"O"+q
    elif "Y" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O-"+p+"Y"+r+"O-"+p+"Y-"+q+"O-"+r+"O"+p
    elif "O" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y"+q+"O"+r+"O-"+p
    elif ">" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y-"+q+"O"+r+"O-"+p
    else:
        print(u'Error enENC(): Fórmula incorrecta!')

    return B

# Algoritmo de transformacion de Tseitin
# Input: A (cadena) en notacion inorder
# Output: B (cadena), Tseitin
def Tseitin(A, letrasProposicionalesA, n):
    letrasProposicionalesB = [chr(x) for x in range(256, 256 + ((n*n))**3)]
    assert(not bool(set(letrasProposicionalesA) & set(letrasProposicionalesB))), u"¡Hay letras proposicionales en común!"
    L = []
    Pila = []
    I = -1
    S = A[0]
    while len(A) > 0:
        if (S in letrasProposicionalesA) and (Pila[-1] == "-"):
            I += 1
            Atomo = letrasProposicionalesB[I]
            Pila = Pila[:-1]
            Pila.append(Atomo)
            L.append(Atomo+"="+"-"+S)
            A = A[1:]
            S = A[0]
            if len(A) > 0:
                S = A[0]
        elif S == ')':
            W = Pila[-1]
            O = Pila[-2]
            V = Pila[-3]
            Pila = Pila[:len(Pila)-4]
            I += 1
            Atomo = letrasProposicionalesB[I]
            L.append(Atomo+"="+"("+V+O+W+")")
            S = Atomo
        else:
            Pila.append(S)
            A = A[1:]
            if len(A) > 0:
                S = A[0]
    B = ""
    if I < 0:
        Atomo = Pila[-1]
    else:
        Atomo = letrasProposicionalesB[I]

    for X in L:
        Y = enFNC(X)
        B += "Y"+Y

    B = Atomo + B

    return B

# Subrutina Clausula para obtener lista de literales
# Input: C (cadena) una clausula
# Output: L (lista), lista de literales

def Clausula(C):
    L=[]
    while len(C)>0:
        s=C[0]
        if s=="Y" or s=="O":
            C=C[1:]
        elif s=="-":
            literal=s+C[1]
            L.append(literal)
            C=C[2:]
        else:
            L.append(s)
            C=C[1:]
    return L

# Algoritmo para obtencion de forma clausal
# Input: A (cadena) en notacion inorder en FNC
# Output: L (lista), lista de listas de literales
def formaClausal(A):
    L=[]
    i=0
    while len(A)>0:
        if i==len(A)-1:
            L.append(Clausula(A))
            A=''
        else:
            if A[i]=="Y":
                L.append(Clausula(A[:i]))
                A=A[i+1:]
                i=0
            else:
                i+=1
    return L

def claUnitaria(U):
    flag = False
    posicion = -1
    for i in range(len(U)):
        if(len(U[i]) == 0):
            return (True, False, posicion)
        elif(len(U[i]) == 1):
            flag = True
            posicion = i
            break
    return(False, flag, posicion)

def claUnit(S):
    for i in S:
        if(len(i) == 1):
            return True
    return False

def Compl(l):
    if(l[0] == '-'):
        return l.replace('-', '')
    else:
        return '-' + l

def removeCl(S, l):
    S.remove(l)
    if(len(l) >= 1):
        if(l[0] == '-'):
            L = l.replace('-', '')
        else:
            L = l[0]
        for i in S:
            if L in i:
                S.remove(i)
    return S

def removeCompl(S, l):
    if(len(l) >= 1):
        L = l[0]
        L = Compl(L)
        for i in S:
            if L in i:
                i.remove(L)
    return S

def unitPropagate(S, I):
    vacia, unitaria, posicion = claUnitaria(S)
    while(vacia == False and claUnit(S)):
        for i in S:
            S = removeCl(S, i)
            S = removeCompl(S, i)
            if(len(i) == 0):
                return 'Insatisfacible', I
            if(i[0] == '-'):
                I[Compl(i[0])] = 0
            else:
                I[i[0]] = 1
    # print(S, I)
    return S, I

def lDicc(D):
    I = D.copy()
    for i in I:
        if(i[0] == '-'):
            I.pop(i)
            i = Compl(i)
            if(I.get(i) == 0):
                I[i[0]] = 1
            else:
                I[i[0]] = 0
    return I

def DPLL(S, I):
    S, I = unitPropagate(S, I)
    # print(S,I)
    if(S == "Insatisfacible"):
        return 'Insatisfacible', "{}"
    if(len(S) == 0):
        return 'Satisfacible', lDicc(I)
    for i in S:
        if(len(i) == 0):
            return 'Insatisfacible', "{}"
    L = S[0]
    L = Compl(Compl(L[0]))
    Ip = I.copy()
    if(L[0] == '-'):
        Ip[Compl(L[0])] = 0
    else:
        Ip[L[0]] = 1

    Sp = S.copy()
    Sp.append(L[0])

    aux1, aux2 = DPLL(Sp, Ip)
    if(aux1 == 'Satisfacible'):
        return 'Satisfacible', lDicc(Ip)
    else:
        Spp = S.copy()
        Spp.append(Compl(L[0]))
        Ipp = I.copy()
        if(L[0] == '-'):
            Ipp[Compl(L[0])] = 1
        else:
            Ipp[L[0]] = 0
    return DPLL(Spp, Ipp)

def DPLL2(lista, interps):
    lista, interps = unitPropagate2(lista,interps)
    if(len(lista)==0):
        return(lista,interps)
    elif("" in lista):
        return (lista,{})
    else:
        listaTemp = [x for x in lista]
        for l in listaTemp[0]:
            if (len(listaTemp)==0):
                return (listaTemp, interps)
            if (l not in interps.keys() and l!='-'):
                break
        listaTemp.insert(0,l)
        lista2, inter2 = DPLL(listaTemp, interps)
        if inter2 == {}:
            listaTemp = [x for x in lista]
            a =literal_complemento(l)
            listaTemp.insert(0,a)
            lista2, inter2 = DPLL(listaTemp, interps)
        return lista2, inter2

def unitPropagate2(S, I):
    bool = True
    while bool:
        for k in S:
            if len(k) == 0:
                #return "Insatisfacible", {}
                break

        cont = 0
        for i in S:
            if len(i) == 1:
                cont += 1
                lit = i[0]
                if len(lit) == 1:
                    pp = lit
                    compl = "-" + lit
                    valor = 1

                elif(len(lit) == 2):
                    pp = lit[1]
                    compl = lit[1]
                    valor = 0

                for j in S:
                    if j != i:
                        if lit in j:
                            S.remove(j)
                I[pp] = valor
                S.remove(i)
                #print(i)


        if cont == 0:
            bool = False
        else:
            for k in S:
                if compl in k:
                    k.remove(compl)
    return S, I

# Test enFNC()
# Descomente el siguiente código y corra el presente archivo
# formula = "p=(qYr)"
# print(enFNC(formula)) # Debe obtener qO-pYrO-pY-qO-rOp

# Test Tseitin()
# Descomente el siguiente código y corra el presente archivo
# letrasProposicionalesA = ['p','q']
# letrasProposicionalesA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
# formula = "(pYq)"
# formula = "(-aO-b)Y(-aO-c)Y(-bO-a)Y(-bO-c)Y(-dO-e)Y(-dO-f)Y(-eO-f)Y(-gO-h)Y(-gO-i)Y(-hO-i)"
# print(Tseitin(formula,letrasProposicionalesA)) # Debe obtener AYpO-AYqO-AY-pO-qOA (la A tiene una raya encima)

# Test Clausula()
# Descomente el siguiente código y corra el presente archivo
# c = "pO-qOr"
# print(Clausula(c)) # Debe obtener ['p', '-q', 'r']

# Test formaClausal()
# Descomente el siguiente código y corra el presente archivo
# f = "pO-qOrY-sOt"
# print(formaClausal(f)) # Debe obtener [['p', '-q', 'r'], ['-s', 't']]
