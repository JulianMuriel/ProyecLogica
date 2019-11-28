from matrices import *
from FNC import *
#from tree import *

print("¿De caunto es el tablero de ajedrez?: ")

orden = int(input())

mat = matriz(orden)
nameLetProp(mat, orden)
#print(mat)

#atoms = atomos(orden)
atoms = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
#regla = regHor(mat)#+"Y"+regVer(mat)
regla = "(aY-bY-cY-d)O(-aYbY-cY-d)O(-aY-bYcY-d)O(-aY-bY-cYd)O(eY-fY-gY-h)O(-eYfY-gY-h)O(-eY-fYgY-h)O(-eY-fT-gYh)O(iY-jY-KY-l)O(-iYjY-kY-l)O(-iY-jYkY-l)O(-iY-jY-kYl)O(mY-nY-oY-p)O(-mYnY-oY-p)O(-mY-nYoY-p)O(-mY-nY-oYp)"
print(regla)

regla2 = Tseitin(regla, atoms, 4)
print(regla2)

regla3 = formaClausal(regla2)
print(regla3)

inter = {}
#r, int = unitPropagate2(regla3, inter)
r, int = DPLL2(regla3, inter)
print("Interpretaciones:")
print(int)



#tablero = tabAjedrez(orden)

#letProp = atomos(orden)

#printVars(tablero)

#regla = regla(tablero, orden)

#print(regla)
