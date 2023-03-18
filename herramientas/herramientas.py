
# Angel Higueros
# 20460
# Laboratorio B

def validar_cadena(automata, cadena):
    estado_actual = automata.startstate
    for simbolo in cadena:
        try:
            estado_actual = automata.gettransitions(estado_actual, simbolo)
        except KeyError:
            return False
    return estado_actual in automata.finalstates


def infix_a_postfix(r):
    precedencia = {'(': 0, '|': 1, '.': 2, '*': 3}
    operadores = []
    postfix = []

    infix_stack = list(r)

    validacion = validar_infix(r)

    if validacion is False:
        print("[Error] Expresion r no es correcta, los parentesis no estan balanceados")
        return None
        

    for char in infix_stack:
        if char == '(':
            operadores.append(char)
        elif char == ')':
            while operadores[-1] != '(':
                postfix.append(operadores.pop())
            operadores.pop() 

        elif char in '|.':
            # Si el carácter es un operador, desapilar los operadores con mayor o igual precedencia y agregarlos a la notación postfix
            while operadores and operadores[-1] != '(' and precedencia[char] <= precedencia[operadores[-1]]:
                postfix.append(operadores.pop())
            operadores.append(char) 

        elif char == '*':
            postfix.append(char)

        elif char.isalpha() or char.isdigit():
            postfix.append(char)

        else:
            print("[Error] Expresión infix no válida")
            return None
    

    while operadores:
        postfix.append(operadores.pop())

    return postfix


def validar_infix(r):
    parentesis = 0
    for i in r:
        if i == '(':
            parentesis += 1
        elif i == ')':
            parentesis -= 1

    return parentesis == 0
