import sys
import time
from colorama import init, Fore, Style

init()

'''
Decidimos juntar las funciones en el código principal para facilitar la creación del programa ejecutable.
'''


# Formato de encabezados
def encabezados(titulo):
    print(Fore.YELLOW + "-" * 78)
    print(Fore.YELLOW + "|", end="")
    print(Fore.YELLOW + titulo.center(76, " "), end="")
    print(Fore.YELLOW + "|")
    print(Fore.YELLOW + "-" * 78)


# ---- Inician funciones de TABLAS DE VERDAD ----
def validacion():  # funcion principal
    global simbolos, enunciado, lista_en, argumentos, matriz
    simbolos = ["~", "^", "v", ">", "↔", "(", ")"]
    enunciado = str(input("\tEscribe el enunciado proposicional: "))
    enunciado = enunciado.replace(" ", "")  # enunciado sin espacios
    lista_en = list(enunciado)
    lista_en = [q for q in lista_en if q not in simbolos]  # enunciado sin símbolos
    # print(lista_en)
    argumentos = set(lista_en)
    # print(argumentos)
    argumentos = sorted(list(argumentos))  # orden alfabético de proposiciones
    col = len(argumentos)  # no. de columnas x proposición
    matriz = []

    for a in argumentos:
        renglones = 2 ** len(argumentos)  # fórmula 2^n para el no. de proposiciones
        num_iteracion = 2 ** (col - 1)  # total de proposiciones a comparar para iterarlas
        tabla = []
        tabla.append(a)  # las agrega a la tabla
        while renglones > 0:
            for x in range(num_iteracion):
                tabla.append("V")
                renglones -= 1
            for x in range(num_iteracion):
                tabla.append("F")
                renglones -= 1
        matriz.append(tabla)
        col = col - 1


def JuntarParentesisExteriores():
    global posicion, posicion2, tabla_verdad, lista, a, encabezado
    i = encabezado.index(lista[a - 1])
    posicion_argumento.append(i)
    i = encabezado.index(lista[a + 1])
    posicion_argumento.append(i)
    modificacion = lista[a - 1] + lista[a] + lista[a + 1]
    if lista[a - 2] == "(" and lista[a + 2] == ")":
        modificacion = lista[a - 2] + modificacion + lista[a + 2]
        encabezado.append(modificacion)
        lista.insert(a + 3, modificacion)
        del lista[(a - 2):(a + 3)]
    else:
        encabezado.append(modificacion)
        lista.insert(a + 2, modificacion)
        del lista[(a - 1):(a + 2)]
    a = 0
    i = 0
    tabla_verdad = []
    tabla_verdad.append(modificacion)
    posicion = posicion_argumento[i]
    posicion2 = posicion_argumento[i + 1]
    return a, tabla_verdad, posicion, posicion2


def OperadoresLogicos():
    global enunciado, posicion, posicion2, tabla_verdad, lista, posicion_argumento, matriz, argumentos, encabezado, a, end, e
    vueltas = 0
    lista = list(enunciado)  # se pone en lista la proposiicon
    simbolos = ["^", "v", ">", "↔"]
    a = 0
    argumentos_negados = []
    encabezado = argumentos + argumentos_negados

    # Identificar posicion de su argumento negativo
    posicion_argumento = []
    for arg in argumentos_negados:
        if arg[1] in argumentos:
            a = argumentos.index(arg[1])
            posicion_argumento.append(a)
    # Hacer tabla de verdad de negacion
    a = 0
    for arg in argumentos_negados:  ##Cada negación se transforma en su inverso
        tabla_verdad = []
        tabla_verdad.append(arg)
        posicion = posicion_argumento[a]
        for x in range(len(matriz[posicion])):
            if matriz[posicion][x] == "V":
                tabla_verdad.append("F")
            if matriz[posicion][x] == "F":
                tabla_verdad.append("V")
        a += 1
        matriz.append(tabla_verdad)  # se añade a la matriz principal que sera la que se va a imprirmirn

    # Operadores Logicos
    e = 1
    end = 0
    while e > 0 and end != 1:
        # Disyuncion
        a = 0
        while a != len(lista):
            posicion_argumento = []
            if lista[a] == "v":  # si en la lista encuentra una disyuncion
                if lista[a + 1] in encabezado and lista[a - 1] in encabezado:
                    JuntarParentesisExteriores()
                    for x in range(len(matriz[posicion])):  # dependera de la longitud
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("V")
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("V")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("V")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("F")
                    matriz.append(tabla_verdad)
                elif lista[a + 1] == "(" and lista[a - 1] == ")":
                    e += 1
                    pass
                elif lista[a - 1] == ")" and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "(":
                    e += 1
                    pass
                elif lista[a + 1] in encabezado and lista[a - 1] == ")":
                    e += 1
                    pass
                else:
                    print("\t[!] DISYUNCIÓN debe ir antes de un argumento o un parentésis")
                    print(lista)
                    end = 1
                    break
            NegarEncabezado()
            a += 1

        # Conjunción
        a = 0
        while a != len(lista):
            posicion_argumento = []
            if lista[a] == "^":
                if lista[a + 1] in encabezado and lista[a - 1] in encabezado:
                    JuntarParentesisExteriores()
                    for x in range(len(matriz[posicion])):
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("V")
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("F")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("F")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("F")
                    matriz.append(tabla_verdad)
                elif lista[a + 1] == "(" and lista[a - 1] == ")":
                    e += 1
                    pass
                elif lista[a - 1] == ")" and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "(":
                    e += 1
                    pass
                elif lista[a + 1] in encabezado and lista[a - 1] == ")":
                    e += 1
                    pass
                else:
                    print("\t[!] CONJUNCIÓN debe ir antes de un argumento o un parentésis")
                    print(lista)
                    end = 1
                    break
            NegarEncabezado()
            a += 1

        # Condicionalidad
        a = 0
        while a != len(lista):
            posicion_argumento = []
            if lista[a] == ">":
                if lista[a + 1] in encabezado and lista[a - 1] in encabezado:
                    JuntarParentesisExteriores()
                    for x in range(len(matriz[posicion])):
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("V")
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("F")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("V")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("V")
                    matriz.append(tabla_verdad)
                elif lista[a + 1] == "(" and lista[a - 1] == ")":
                    e += 1
                    pass
                elif lista[a - 1] == ")" and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "(":
                    e += 1
                    pass
                elif lista[a + 1] in encabezado and lista[a - 1] == ")":
                    e += 1
                    pass
                else:
                    print("\t[!] IMPLICACIÓN debe ir antes de un argumento o un parentésis")
                    print(lista)
                    end = 1
                    break
            NegarEncabezado()
            a += 1

        # Bicondiconalidad
        a = 0
        while a != len(lista):
            posicion_argumento = []
            if lista[a] == "↔":
                if lista[a + 1] in encabezado and lista[a - 1] in encabezado:
                    JuntarParentesisExteriores()
                    for x in range(len(matriz[posicion])):
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("V")
                        if matriz[posicion][x] == "V" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("F")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "V":
                            tabla_verdad.append("F")
                        if matriz[posicion][x] == "F" and matriz[posicion2][x] == "F":
                            tabla_verdad.append("V")
                    matriz.append(tabla_verdad)
                elif lista[a - 1] == ")" and lista[a + 1] == "(":
                    e += 1
                    pass
                elif lista[a - 1] == ")" and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "~":
                    e += 1
                    pass
                elif lista[a - 1] in encabezado and lista[a + 1] == "(":
                    e += 1
                    pass
                elif lista[a + 1] in encabezado and lista[a - 1] == ")":
                    e += 1
                    pass
                else:
                    print("\t[!] BICONDICIONAL debe ir antes de un argumento o un parentésis")
                    print(lista)
                    end = 1
                    break
            NegarEncabezado()
            a += 1
        vueltas += 1
        e -= 1
        a = 0
        # Negaciones de Encabezados
        while a != len(lista):
            posicion_argumento = []
            if lista[a] == "~":
                if lista[a + 1] in encabezado:
                    i = encabezado.index(lista[a + 1])
                    posicion_argumento.append(i)
                    modificacion = lista[a] + lista[a + 1]
                    if lista[a - 1] == "(" and lista[a + 2] == ")":
                        modificacion = lista[a - 1] + modificacion + lista[a + 2]
                        encabezado.append(modificacion)
                        lista.insert(a + 3, modificacion)
                        del lista[(a - 1):(a + 3)]
                    else:
                        encabezado.append(modificacion)
                        lista.insert(a + 2, modificacion)
                        del lista[(a):(a + 2)]
                    a = 0
                    tabla_verdad = []
                    tabla_verdad.append(modificacion)
                    posicion = posicion_argumento[0]
                    for x in range(len(matriz[posicion])):
                        if matriz[posicion][x] == "V":
                            tabla_verdad.append("F")
                        if matriz[posicion][x] == "F":
                            tabla_verdad.append("V")
                    matriz.append(tabla_verdad)
                elif lista[a + 1] == "(" and lista[a - 1] in simbolos:
                    e += 1
                    pass
                elif lista[a + 1] == "(":
                    e += 1
                    pass
                elif lista[a + 1] == "(" and lista[a - 1] == "(":
                    e += 1
                    pass
                elif lista[a + 1] == "(" and lista[a - 1] == ")":
                    e += 1
                    pass
                else:
                    print("\t[!] NEGACIÓN debe ir antes de un argumento o un parentésis")
                    print(lista)
                    end = 1
                    break
            NegarEncabezado()
            a += 1
    if end != 1:
        pass
    else:
        print("\t[!] - ERROR - [!] - Revisa el enunciado - [!]")


def NegarEncabezado():
    global e, end, a
    # Negación encabezado
    c = 0
    while c != len(lista):
        posicion_argumento = []
        if lista[c] == "~":
            if lista[c + 1] in encabezado:
                i = encabezado.index(lista[c + 1])
                posicion_argumento.append(i)
                modificacion = lista[c] + lista[c + 1]
                if lista[c - 1] == "(" and lista[c + 2] == ")":
                    modificacion = lista[c - 1] + modificacion + lista[c + 2]
                    encabezado.append(modificacion)
                    lista.insert(c + 3, modificacion)
                    del lista[(c - 1):(c + 3)]
                else:
                    encabezado.append(modificacion)
                    lista.insert(c + 2, modificacion)
                    del lista[(c):(c + 2)]
                a = 0
                c = 0
                tabla_verdad = []
                tabla_verdad.append(modificacion)
                posicion = posicion_argumento[0]
                for x in range(len(matriz[posicion])):
                    if matriz[posicion][x] == "V":
                        tabla_verdad.append("F")
                    if matriz[posicion][x] == "F":
                        tabla_verdad.append("V")
                matriz.append(tabla_verdad)
        c += 1


def GuardarTabla(matriz2, encabezados):
    global matriz
    # Guardar tabla final
    for tabla in matriz:
        if tabla == matriz[len(matriz) - 1]:
            matriz2.append(tabla[1:len(tabla)])
            encabezados.append(tabla[0])


def imp_tabla():
    global matriz
    for tabla in matriz:
        print(Fore.BLUE + "\t", tabla[0].center(4, " "))
        StrT = "\t".join(tabla[1:len(tabla)])
        print(Fore.CYAN + StrT)
        print("\n")


# ---- Terminan funciones de TABLAS DE VERDAD ----

# ---- Inician funciones de CALCULADORA DE CONJUNTOS ----
# Calculadora de conjuntos
def conjuntos():
    A = str(input("\tIntroduzca su conjunto A: "))
    B = str(input("\tIntroduzca su conjunto B: "))
    C = str(input("\tIntroduzca su conjunto C: "))

    conjuntoA = []
    conjuntoB = []
    conjuntoC = []
    conjuntoA = A.split(",")
    conjuntoB = B.split(",")
    conjuntoC = C.split(",")  # Aquí se separan los elementos de la lista cada que se detecta una coma

    # Menú para elegir operación para los conjuntos escritos previamente
    print("\n\tSeleccione el inciso de la operación a realizar:")
    print("\t\ta. Unión (U)\n\t\tb. Intersección (∩)\n\t\tc. Diferencia (-)\n\t\td. Diferencia simétrica (Δ)")
    eleccion = "-"
    while eleccion != "a" or eleccion != "b" or eleccion != "c" or eleccion != "d":
        eleccion = input("\t\t>>> ").lower()
        if eleccion == "a" or eleccion == "b" or eleccion == "c" or eleccion == "d":
            break
    if eleccion == "a":  # Valores para el encabezado de cada cálculo
        t = "UNIÓN (U) DE 'A', 'B' Y 'C'"
    elif eleccion == "b":
        t = "INTERSECCIÓN (∩) DE 'A', 'B' Y 'C'"
    elif eleccion == "c":
        t = "DIFERENCIA (-) DE 'A', 'B' Y 'C'"
    elif eleccion == "d":
        t = "DIFERENCIA SIMÉTRICA (Δ) DE 'A', 'B' Y 'C'"

    encabezados(t)  # Llama a la función encabezados() para imprimir el título de la sección
    # Cardinalidad
    print("    CARDINALIDAD: \t", end="")
    cA = set(sorted(conjuntoA))
    list_cA = list(cA)
    if list_cA[0] == "":  # Si se detecta que el primer índice la lista está vacío, la cardinalidad será 0
        print("   |A| = 0", end="")
    else:
        print("   |A| =", len(cA), end="")

    cB = set(sorted(conjuntoB))
    list_cB = list(cB)
    if list_cB[0] == "":
        print("\t  |B| = 0", end="")
    else:
        print("\t |B| =", len(cB), end="")

    cC = set(sorted(conjuntoC))
    list_cC = list(cC)
    if list_cC[0] == "":
        print("\t  |C| = 0", end="")
    else:
        print("\t |C| =", len(cC), end="")
    print("\n   " + "-" * 72 + "   ")

    if eleccion == "a":
        print("\tUNIÓN:")  # Enlista los valores de los dos conjuntos que se están comparando
        print("\tAUB / BUA : ", sorted(set(conjuntoA + conjuntoB)))
        print("\tAUC / CUA : ", sorted(set(conjuntoA + conjuntoC)))
        print("\tBUC / CUB : ", sorted(set(conjuntoB + conjuntoC)))
        print("\tAU(BUC)   : ", sorted(set(conjuntoA + sorted(set(conjuntoB + conjuntoC)))))

    elif eleccion == "b":
        # Intersección
        print("\tINTERSECCIÓN:")
        AinterseccionB = []
        AinterseccionC = []
        BinterseccionC = []
        interseccionABC = []
        # intersección a y b
        for i in conjuntoA:
            if (i not in AinterseccionB) and (i in conjuntoB):
                AinterseccionB.append(i)  # Añade a la lista los elementos que comparten A y B sin repetirlos
        # intersección a y c
        for i in conjuntoA:
            if (i not in AinterseccionC) and (i in conjuntoC):
                AinterseccionC.append(i)  # Añade a la lista los elementos que comparten A y C sin repetirlos
        # interseccion b y c
        for i in conjuntoB:
            if (i not in BinterseccionC) and (
                    i in conjuntoC):  # Añade a la lista los elementos que comparten C y B sin repetirlos
                BinterseccionC.append(i)

        for i in AinterseccionB:
            if (i not in interseccionABC) and (
                    i in conjuntoC):  # Compara la intersección de A y B con los elementos de C y los añade a la lista
                interseccionABC.append(i)

        print("\tA∩B / B∩A : ", (AinterseccionB))
        print("\tA∩C / C∩A : ", (AinterseccionC))
        print("\tB∩C / C∩B : ", (BinterseccionC))
        print("\tA∩(B∩C)   : ", (interseccionABC))

    elif eleccion == "c":
        print("\tDIFERENCIA:")
        # En cada for se iteran los conjuntos previamente separados en "Cardinalidad" y se compara con otro;
        # si en el segundo no existe el elemento, se agrega a la diferencia de ambos.
        diferenciaAB = []
        for i in cA:
            if (i not in cB):
                diferenciaAB.append(i)
        diferenciaBA = []
        for i in cB:
            if (i not in cA):
                diferenciaBA.append(i)
        diferenciaAC = []
        for i in cA:
            if (i not in cC):
                diferenciaAC.append(i)
        diferenciaCA = []
        for i in cC:
            if (i not in cA):
                diferenciaCA.append(i)
        diferenciaBC = []
        for i in cB:
            if (i not in cC):
                diferenciaBC.append(i)
        diferenciaCB = []
        for i in cC:
            if (i not in cB):
                diferenciaCB.append(i)

        # Se imprime cada lista almacenada en las iteraciones anteriores
        print("\tA-B : ", diferenciaAB)
        print("\tB-A : ", diferenciaBA)
        print("\tA-C : ", diferenciaAC)
        print("\tC-A : ", diferenciaCA)
        print("\tB-C : ", diferenciaBC)
        print("\tC-B : ", diferenciaCB)

    elif eleccion == "d":
        # Se comparan los conjuntos previamente almacenados en "Cardinalidad" con el operador ^ para obtener los elementos que comparten y quitarlos
        print("\tDIFERENCIA SIMÉTRICA:")
        dsAB = sorted(cA ^ cB)
        dsAC = sorted(cA ^ cC)
        dsBC = sorted(cB ^ cC)
        print("\tAΔB / BΔA : ", dsAB)
        print("\tAΔC / CΔA : ", dsAC)
        print("\tBΔC / CΔB : ", dsBC)


# ---- Terminan funciones de CALCULADORA DE CONJUNTOS ----

# ---- Inician funciones de SUCESIONES E INDUCCIÓN ----
def lista_sucesiones():
    t = encabezados("CALCULAR SUCESIÓN")
    print("\tSeleccione la sucesión a iterar: ")
    print("\t1. Escribir fórmula")
    print("\t2. 1/k         (Armónica)")
    print("\t3. (-1)^k/(k+1)")
    print("\t4. 1/k(k+1)")
    print("\t5. 1+(1/2)^k")
    print("\t6. 1/k^(n-1)   (Zenon)")

    s = input("\t>>> ")
    s = int(s)
    while s < 0 or s > 10:
        s = input("\t>>>")
        s = int(s)
    return s


def op_sucesiones(inf, sup, form):
    t = encabezados(f"{form}")
    print(f"\tm = {inf}    |    n = {sup}\n")
    original = form
    n = sup
    suma = 0
    mult = 1
    for i in range(0, sup - inf + 1):
        k = sup - i
        print(f"\tFórmula: {original} con k = {n}     Resultado: {eval(form)}")
        suma += eval(form)
        mult *= eval(form)
        n -= 1
    print("\t> Sumatoria = ", suma, "\n\t> Multiplicación = ", mult)


def suc2(inf, sup):
    t = encabezados("1/k")
    print(f"\tm = {inf}    |    n = {sup}\n")
    suma = 0
    mult = 1
    for i in range(inf, sup + 1):
        f = 1 / sup
        print(f"\tFórmula: 1/{sup} = {f}")
        suma += 1 / sup
        mult *= 1 / sup
        sup -= 1
    print(f"\t> Sumatoria: {suma}\n\t> Multiplicación: {mult}")


def suc3(inf, sup):
    t = encabezados("(-1)^k/(k+1)")
    print(f"\tm = {inf}    |    n = {sup}\n")
    suma = 0
    mult = 1
    for i in range(inf, sup + 1):
        f = ((-1) ** (sup)) / (sup + 1)
        print(f"\tFórmula: (-1)^{sup}/({sup}+1) = {f}")
        suma += ((-1) ** (sup)) / (sup + 1)
        mult *= ((-1) ** (sup)) / (sup + 1)
        sup -= 1
    print(f"\t> Sumatoria: {suma}\n\t> Multiplicación: {mult}")


def suc4(inf, sup):
    t = encabezados("1/k(k+1)")
    print(f"\tm = {inf}    |    n = {sup}\n")
    suma = 0
    mult = 1
    for i in range(inf, sup + 1):
        f = 1 / (sup * (sup + 1))
        print(f"\tFórmula: 1/{sup}({sup}+1) = {f}")
        suma += 1 / (sup * (sup + 1))
        mult *= 1 / (sup * (sup + 1))
        sup -= 1
    print(f"\t> Sumatoria: {suma}\n\t> Multiplicación: {mult}")


def suc5(inf, sup):
    t = encabezados("1+(1/2)^k")
    print(f"\tm = {inf}    |    n = {sup}\n")
    suma = 0
    mult = 1
    for i in range(inf, sup + 1):
        f = 1 + ((1 / 2) ** sup)
        print(f"\tFórmula: 1+(1/2)^{sup} = {f}")
        suma += 1 + ((1 / 2) ** sup)
        mult *= 1 + ((1 / 2) ** sup)
        sup -= 1
    print(f"\t> Sumatoria: {suma}\n\t> Multiplicación: {mult}")


def suc6(inf, sup):
    t = encabezados("Zenon 1/2^(k-1)")
    print(f"\tm = {inf}    |    n = {sup}\n")
    suma = 0
    mult = 1
    for i in range(inf, sup + 1):
        f = 1 / (2 ** (sup - 1))
        print(f"\tFórmula: 1/{2}^({sup}-1) = {f}")
        suma += 1 / (2 ** (sup - 1))
        mult *= 1 / (2 ** (sup - 1))
        sup -= 1
    print(f"\t> Sumatoria: {suma}\n\t> Multiplicación: {mult}")


def tipo2(lista):
    if lista[1] - lista[0] == lista[2] - lista[1]:
        print("\t\t\t\t\t La sucesión es ARITMÉTICA")
    else:
        print("\t\t\t\t\t La sucesión es GEOMÉTRICA")


def determinar_tipo():
    t = encabezados("DETERMINAR EL TIPO DE SUCESIÓN")
    while True:
        try:
            elementos = int(input("\t¿Con cuántos elementos quieres hacer la comprobación? "))
            if (elementos >= 4):
                break
            else:
                print("\t[!] Debes de incluir mínimo 4 términos de la sucesión")
        except ValueError:
            print("\t[!] Debes de incluir mínimo 4 términos de la sucesión")
    S = list([])
    c = 1
    for i in range(elementos):
        print("\t\t>>>Elemento", c, ": ", end="")
        a = int(input())
        c += 1
        S.append(a)
    tipo2(S)


# ---- Terminan funciones de SUCESIONES E INDUCCIÓN ----

# ---- Inician funciones de RELACIONES Y FUNCIONES ----
def tipo_relaciones():
    # Pide cuántos pares separados escribirá el usuario
    cantidad = int(input("\tCantidad de pares ordenados a escribir >>> "))
    pares, x, y = [], 0, 0
    print("\tFormato requerido: x,y\n")

    for i in range(cantidad):
        x, y = input("\tIngresa el %d° par >>> " % (i + 1)).split(",")
        pares.append((x, y))  # Almacena los pares en dos listas distintas

    dominio = []
    codominio = []

    for i, j in pares:  # Itera la lista de los pares para obtener dominio y rango
        if (i not in dominio):
            dominio.append(i)

        if (j not in codominio):
            codominio.append(j)
    print("\n")
    # PARTE REFLEXIVA
    reflexiva = True
    for i in dominio:
        if ((i, i) not in pares):
            reflexiva = False
            break

    if (reflexiva == True):
        print("\tSí es reflexiva")
    else:
        print("\tNo es reflexiva")

    # PARTE SIMÉTRICA
    simetria = True
    for i, j in pares:
        if ((j, i) not in pares):
            simetria = False
            break

    if (reflexiva == True):
        print("\tSí es simétrica")
    else:
        print("\tNo es simétrica")

    # PARTE TRANSITIVA
    transitiva = True
    pares.sort()
    h1, h2, h3 = 0, 0, 0
    for i in range(len(pares)):
        h1 = pares[i][0]
        h2 = pares[i][1]
        for j in range(len(pares)):
            if (pares[j][0] == h2):
                h3 = pares[j][1]
                if ((h1, h3) not in pares):
                    transitiva = False
                    break
        if (transitiva == False):
            break

    if (transitiva == True):
        print("\tSí es transitiva")
    else:
        print("\tNo es transitiva")

    dominio.sort()
    f_dominio = ", ".join(dominio)
    codominio.sort()
    f_codominio = ", ".join(codominio)
    print("\n\tDominio: {" + f_dominio + "}\n\tRango: {" + f_codominio + "}")
    # Imprime el dominio y codominio en forma de string, separados por comas

    # Convierte la lista de pares en un string para quitar los caracteres que no sean numéricos
    pares = str(pares)
    numeros = ' '.join(filter(str.isalnum, pares))
    numeros_lista = numeros.split(" ")  # Convierte en lista dichos números
    longitud = len(numeros_lista)
    x = []
    y = []
    cont_x = 0

    for i in range(0, longitud - 1, 2):  # Obtiene los valores de las abscisas
        if numeros_lista[i] not in x:
            x.append(numeros_lista[i])
        else:
            cont_x += 1  # Suma 1 si una 'x' se repite
    for j in range(1, longitud, 2):  # Obtiene los valores de las ordenadas
        if numeros_lista[j] not in y:
            y.append(numeros_lista[j])
    if cont_x != 0:
        print("\t-> No es una función")
    else:
        print("\t-> Es una función")


# ---- Terminan funciones de RELACIONES Y FUNCIONES ----

# Menú generador de tablas (opción 'a' del inicial)
def tabla_menu():
    t = encabezados("GENERADOR DE TABLAS DE VERDAD")
    print("\t\ta. Instrucciones y operadores\n\t\tb. Generar tabla\n\t\tc. Volver al menú principal")
    eleccion = "-"
    while eleccion != "a" or eleccion != "b" or eleccion != "c":
        eleccion = input("\t\t>>> ").lower()
        if eleccion == "a" or eleccion == "b" or eleccion == "c":
            break
    return eleccion  # devuelve la letra al menú inicial


# Instrucciones - Letra 'a' del menú generador de tablas
def inst():
    t = encabezados("INSTRUCCIONES Y OPERADORES")
    print("\t1. Indicar jerarquía de operaciones con paréntesis ( ), utilizar sólo\n\tlos NECESARIOS.")
    print("\t2. Escribir un único enunciado utilizando las proposiciones: \n\t\tp, q, r, s, t.")
    print("\t3. La tabla se imprimirá verticalmente (se lee de arriba a abajo).")
    print("\tOPERADORES POR JERARQUÍA: ")
    print("\t\tNegación: ~ (alt+126) \n\t\tConjunción: ^ (alt+94)\n\t\tDisyunción: v (letra)")
    print("\t\tImplicación: > (alt+62)\n\t\tBicondicional: ↔ (copiar y pegar)")


# Menú calculadora de tablas de verdad (opción 'b' del inicial)
def calculadora_menu():
    t = encabezados("CALCULADORA DE CONJUNTOS")
    print("\t\ta. Instrucciones\n\t\tb. Calcular conjuntos\n\t\tc. Volver al menú principal")
    eleccion = "-"
    while eleccion != "a" or eleccion != "b" or eleccion != "c":
        eleccion = input("\t\t>>> ").lower()
        if eleccion == "a" or eleccion == "b" or eleccion == "c":
            break
    return eleccion  # devuelve la letra al menú inicial


# Instrucciones de calculadora - Letra 'a' del menú calculadora
def inst_conjuntos():
    t = encabezados("INSTRUCCIONES PARA CONJUNTOS")
    print(
        "\t1. Escribir 3 conjuntos con sus elementos SEPARADOS por una coma SIN\n\tespacio.\n\t\t>>> Ejemplo: a,b,c,d,e")
    print("\t2. Los elementos son alfanuméricos (letras y números enteros). ")
    print("\t3. Elegir una de las 4 operaciones:")
    print(
        "\tOPERACIONES DE CONJUNTOS: \n\t\tUnión (U)\n\t\tIntersección (∩)\n\t\tDiferencia (-)\n\t\tDiferencia simétrica (Δ)")


# Menú Sucesiones - Letra 'c' del menú inicial
def sucesiones_menu():
    t = encabezados("SUCESIONES")
    print(
        "\t\ta. Instrucciones\n\t\tb. Calcular sucesión\n\t\tc. Determinar tipo de sucesión\n\t\td. Volver al menú principal")
    eleccion = "-"
    while eleccion != "a" or eleccion != "b" or eleccion != "c" or eleccion != "d":
        eleccion = input("\t\t>>> ").lower()
        if eleccion == "a" or eleccion == "b" or eleccion == "c" or eleccion == "d":
            break
    return eleccion  # devuelve la letra al menú inicial


# Instrucciones Sucesiones - Letra 'a' del submenú de sucesiones
def inst_sucesiones():
    t = encabezados("INSTRUCCIONES PARA SUCESIONES")
    print("\tPARA CÁLCULO DE SUCESIONES: ")
    print("\t1. Escribir la fórmula en términos de 'k', los operadores son:")
    print("\t\t'**' exponente\t\t'*' multiplicación\n\t\t'/' división\t\t'-' resta\n\t\t'+' suma\t\t\t'()' jerarquía")
    print("\t2. Escribir enteros para los límites superior (n) e inferior (m); m < n.")
    print("\t3. O si se quiere calcular una prestablecida, ingresar opción y límites.")
    print("\n\tPARA DETERMINAR TIPO DE SUCESIÓN: ")
    print("\t1. Introduce el número de elementos que usarás para la comprobación \n\t   (deben de ser mínimo 4).")
    print("\t2. Introduce los elementos de la sucesión, sólo ENTEROS.")


# Menú Relaciones - Letra 'd' del menú inicial
def relaciones_menu():
    t = encabezados("RELACIONES Y FUNCIONES")
    print("\t\ta. Instrucciones\n\t\tb. Determinar relación \n\t\tc. Volver al menú principal")
    eleccion = "-"
    while eleccion != "a" or eleccion != "b" or eleccion != "c":
        eleccion = input("\t\t>>> ").lower()
        if eleccion == "a" or eleccion == "b" or eleccion == "c":
            break
    return eleccion  # devuelve la letra al menú inicial


# Instrucciones Relaciones - Letra 'a' del submenú de Relaciones
def inst_relaciones():
    t = encabezados("INSTRUCCIONES DE RELACIONES Y FUNCIONES")
    print("\t1. Introducir cantidad de pares a escribir.")
    print("\t2. Escribir cada par ordenado sin paréntesis: ")
    print("\t\tEjemplo del primer par: 0,1")


# Menú inicial
def menu_inicial():
    t = encabezados("MENÚ PRINCIPAL")
    print("\t\ta. Generador de tablas de verdad\n\t\tb. Calculadora de conjuntos\n\t\tc. Sucesiones")
    print("\t\td. Relaciones y funciones\n\t\te. Salir del programa")
    opcion = input("\t\t>>> ").lower()
    return opcion


# -------- INICIA CÓDIGO GLOBAL --------------------------------------------
# Encabezado
if __name__ == '__main__':
    print(Fore.YELLOW + "-" * 78)
    print(Fore.YELLOW + "|" + " " * 76 + "|")
    print(Fore.YELLOW + "|", end="")
    titulo = "FCC TOOLKIT 2021  \"C & V\""
    print(Style.BRIGHT + Fore.YELLOW + titulo.center(76, " "), end="")
    print(Fore.YELLOW + "|")
    print(Fore.YELLOW + "|" + " " * 76 + "|")
    print(Fore.YELLOW + "-" * 78)

    cont = 0
    while cont != 1:
        opcion = menu_inicial()
        cont2 = 0

        if opcion == "a":  # generador tablas de verdad
            while cont2 == 0:
                elec_tabla = tabla_menu()
                if elec_tabla == "a":
                    inst()
                elif elec_tabla == "b":
                    encabezados("GENERAR TABLA")
                    validacion()
                    OperadoresLogicos()
                    imp_tabla()
                elif elec_tabla == "c":
                    cont2 = 1

        elif opcion == "b":  # calculadora de conjuntos
            while cont2 == 0:
                elec_calculadora = calculadora_menu()
                if elec_calculadora == "a":
                    inst_conjuntos()
                elif elec_calculadora == "b":
                    encabezados("CALCULAR CONJUNTOS")
                    conjuntos()
                elif elec_calculadora == "c":
                    cont2 = 1

        elif opcion == "c":  # sucesiones
            while cont2 == 0:
                elec_sucesiones = sucesiones_menu()
                if elec_sucesiones == "a":
                    inst_sucesiones()
                elif elec_sucesiones == "b":
                    S = lista_sucesiones()
                    m = int(input("\tIntroduzca límite inferior (n): "))
                    while m < 0:
                        m = int(input("\tIntroduzca límite inferior (n): "))
                    n = int(input("\tIntroduzca límite superior (m): "))
                    while n < m or m < 0:
                        n = int(input("\tIntroduzca límite superior (m): "))

                    if S == 1:
                        form = str(input("\tEscriba la fórmula en función de 'k': ")).lower()
                        op_sucesiones(m, n, form)
                    elif S == 2:
                        suc2(m, n)
                    elif S == 3:
                        suc3(m, n)
                    elif S == 4:
                        suc4(m, n)
                    elif S == 5:
                        suc5(m, n)
                    elif S == 6:
                        suc6(m, n)

                elif elec_sucesiones == "c":
                    determinar_tipo()

                elif elec_sucesiones == "d":
                    cont2 = 1

        elif opcion == "d":  # relaciones
            while cont2 == 0:
                elec_relaciones = relaciones_menu()
                if elec_relaciones == "a":
                    inst_relaciones()
                elif elec_relaciones == "b":
                    encabezados("DETERMINAR RELACIÓN")
                    tipo_relaciones()

                elif elec_relaciones == "c":
                    cont2 = 1

        elif opcion == "e":  # salir
            cont = 1
            print("\n\t\t\t¡Gracias por usar el programa!\n\t\t\t\t\t Cerrando Toolkit", end="")
            for i in range(3):
                print(".", end="")
                time.sleep(1)
            sys.exit()

# ----- TERMINA CÓDIGO GLOBAL ---------------------------------------