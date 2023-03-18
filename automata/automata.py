# Angel Higueros
# 20460
# Laboratorio B

class Automata:
    def __init__(self, language=None):
        if language is None:
            language = []
        self.states = set()
        self.startstate = None
        self.finalstates = []
        self.transitions = {}
        self.language = language

    @staticmethod
    def epsilon():
        return '$'

    def setstartstate(self, state):
        self.startstate = state
        self.states.add(state)

    def addfinalstates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    def addtransition(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = {inp}
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate : inp}

    def addtransition_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])

    def gettransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    def getEClose(self, findstate):
        allstates = set()
        states = {findstate}
        while states:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates


    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setstartstate(translations[self.startstate])
        rebuild.addfinalstates(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    def newBuildFromEquivalentStates(self, equivalent, pos):
        rebuild = Automata(self.language)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(pos[fromstate], pos[state], tostates[state])
        rebuild.setstartstate(pos[self.startstate])
        for s in self.finalstates:
            rebuild.addfinalstates(pos[s])
        return rebuild

    def getDotFile(self):
        dotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.startstate
            for state in self.states:
                if state in self.finalstates:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    for char in tostates[state]:
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"
        return dotFile

class GenerarAutomata:
    def EstructuraBasica(self):
        estado1 = 1
        estado2 = 2
        basico = Automata()
        basico.setstartstate(estado1)
        basico.addfinalstates(estado2)
        basico.addtransition(1, 2, self)
        return basico

    def estructuraMas(self, b):
        [self, m1] = self.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        estado1 = 1
        estado2 = m2
        plus = Automata()
        plus.setstartstate(estado1)
        plus.addfinalstates(estado2)
        plus.addtransition(plus.startstate, self.startstate, Automata.epsilon())
        plus.addtransition(plus.startstate, b.startstate, Automata.epsilon())
        plus.addtransition(
            self.finalstates[0], plus.finalstates[0], Automata.epsilon()
        )
        plus.addtransition(b.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition_dict(self.transitions)
        plus.addtransition_dict(b.transitions)
        return plus

    def estructuraPunto(self, b):
        [self, m1] = self.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        estado1 = 1
        estado2 = m2-1
        punto = Automata()
        punto.setstartstate(estado1)
        punto.addfinalstates(estado2)
        punto.addtransition(self.finalstates[0], b.startstate, Automata.epsilon())
        punto.addtransition_dict(self.transitions)
        punto.addtransition_dict(b.transitions)
        return punto

    def estructuraEstrella(self):
        [self, m1] = self.newBuildFromNumber(2)
        estado1 = 1
        estado2 = m1
        estrella = Automata()
        estrella.setstartstate(estado1)
        estrella.addfinalstates(estado2)
        estrella.addtransition(
            estrella.startstate, self.startstate, Automata.epsilon()
        )
        estrella.addtransition(estrella.startstate, estrella.finalstates[0], Automata.epsilon())
        estrella.addtransition(
            self.finalstates[0], estrella.finalstates[0], Automata.epsilon()
        )
        estrella.addtransition(
            self.finalstates[0], self.startstate, Automata.epsilon()
        )
        estrella.addtransition_dict(self.transitions)
        return estrella
