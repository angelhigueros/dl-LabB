# Angel Higueros
# 20460
# Laboratorio B
from automata.automata import Automata,  GenerarAutomata
from herramientas.herramientas import infix_a_postfix


class afn_a_afd:

    def __init__(self, nfa):
        self.construirAFD(nfa)
        self.minimizar()

    def obtener_objeto(self):
        return self.dfa

    def obtener_afd_min(self):
        return self.minDFA

    def construirAFD(self, nfa):
        count = 1
        estado1 = nfa.getEClose(nfa.startstate)
        eclose = {nfa.startstate: estado1}
        dfa = Automata(nfa.language)
        dfa.setstartstate(count)
        estados = [[estado1, count]]
        todos_estados = {count: estado1}
        count += 1
        while estados:
            estado, fromindex = estados.pop()
            for char in dfa.language:
                trstates = nfa.gettransitions(estado, char)
                for s in list(trstates):
                    if s not in eclose:
                        eclose[s] = nfa.getEClose(s)
                        trstates = trstates.union(eclose[s])
                if trstates:
                    if trstates not in todos_estados.values():
                        count += 1
                        estados.append([trstates, count])
                        todos_estados[count] = trstates
                        toindex = count
                    else:
                        toindex = list(todos_estados.keys())[list(todos_estados.values()).index(list(trstates))]
                    dfa.addtransition(fromindex, toindex, char)
        for value, estado in todos_estados.items():
            if nfa.finalstates[0] in estado:
                dfa.addfinalstates(value)
        self.dfa = dfa


    def validar_cadena(automata, cadena):
        estado_actual = automata.startstate
        for simbolo in cadena:
            try:
                estado_actual = automata.gettransition(estado_actual, simbolo)
            except KeyError:
                return False
        return estado_actual in automata.finalstates


    def minimizar(self):
        states = list(self.dfa.states)
        n = len(states)
        char_revisar = {}
        count = 1
        lista = []
        equ = dict(zip(range(len(states)), [{s} for s in states]))
        pos = dict(zip(states,range(len(states))))
        for i in range(n-1):
            for j in range(i+1, n):
                if [states[i], states[j]] not in lista and [
                    states[j],
                    states[i],
                ] not in lista:
                    eq = 1
                    top = []
                    for char in self.dfa.language:
                        s1 = self.dfa.gettransitions(states[i], char)
                        s2 = self.dfa.gettransitions(states[j], char)
                        if len(s1) != len(s2):
                            eq = 0
                            break
                        if len(s1) > 1:
                            raise BaseException("Multiple transitions detected in DFA")
                        elif len(s1) == 0:
                            continue
                        s1 = s1.pop()
                        s2 = s2.pop()
                        if s1 != s2:
                            if [s1, s2] in lista or [s2, s1] in lista:
                                eq = 0
                                break
                            else:
                                top.append([s1, s2, char])
                                eq = -1
                    if eq == -1:
                        s = [states[i], states[j], *top]
                        char_revisar[count] = s
                        count += 1
                    elif eq == 0:
                        lista.append([states[i], states[j]])
                    else:
                        p1 = pos[states[i]]
                        p2 = pos[states[j]]
                        if p1 != p2:
                            st = equ.pop(p2)
                            for s in st:
                                pos[s] = p1
                            equ[p1] = equ[p1].union(st)
        newFound = True
        while newFound and char_revisar:
            newFound = False
            toremove = set()
            for p, pair in char_revisar.copy().items():
                for tr in pair[2:]:
                    if [tr[0], tr[1]] in lista or [tr[1], tr[0]] in lista:
                        char_revisar.pop(p)
                        lista.append([pair[0], pair[1]])
                        newFound = True
                        break
        for pair in char_revisar.values():
            p1 = pos[pair[0]]
            p2 = pos[pair[1]]
            if p1 != p2:
                st = equ.pop(p2)
                for s in st:
                    pos[s] = p1
                equ[p1] = equ[p1].union(st)
        if len(equ) == len(states):
            self.minDFA = self.dfa
        else:
            self.minDFA = self.dfa.newBuildFromequStates(equ, pos)


class crear_afn:

    def __init__(self, regex):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65,91)]
        self.alphabet.extend([chr(i) for i in range(97,123)])
        self.alphabet.extend([chr(i) for i in range(48,58)])
        self.buildNFA()

    def obtener_objeto(self):
        return self.nfa

    def buildNFA(self):
        language = set()
        self.stack = []
        self.automata = []
        predecesor= ':e:'
        infix_a_postfix(self.regex)
        for char in self.regex:
            if char in self.alphabet:
                language.add(char)
                if predecesor != self.dot and (predecesor in self.alphabet or predecesor in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.automata.append(GenerarAutomata.EstructuraBasica(char))
            elif char  ==  self.openingBracket:
                if predecesor != self.dot and (predecesor in self.alphabet or predecesor in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.stack.append(char)
            elif char  ==  self.closingBracket:
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators:
                        self.procesarOperador(o)
            elif char == self.star:
                self.procesarOperador(char)
            elif char in self.operators:
                if (
                    predecesor not in self.operators
                    and predecesor != self.openingBracket
                ):
                    self.addOperatorToStack(char)
            else:
                print("[!] El caracter no es aceptado en el language")
                break
            predecesor = char
        while self.stack:
            op = self.stack.pop()
            self.procesarOperador(op)
        if len(self.automata) > 1:
            print(self.automata)
        self.nfa = self.automata.pop()
        self.nfa.language = language

    def addOperatorToStack(self, char):
        while 1 and len(self.stack) != 0:
            top = self.stack[len(self.stack)-1]
            if top == self.openingBracket:
                break
            if top not in [char, self.dot]:
                break
            op = self.stack.pop()
            self.procesarOperador(op)
        self.stack.append(char)

    def procesarOperador(self, operador):
        if operador == self.star:
            self.automata[-1] = GenerarAutomata.estructuraEstrella(self.automata[-1])
        elif operador == self.plus:
            a, b = self.automata.pop(), self.automata.pop()
            self.automata.append(GenerarAutomata.estructuraMas(b, a))
        elif operador == self.dot:
            a, b = self.automata.pop(), self.automata.pop()
            self.automata.append(GenerarAutomata.estructuraPunto(b, a))


