
# Angel Higueros
# 20460
# Laboratorio B

from grafos.grafos import mostrar_afn
from automata.transformaciones import *
from herramientas.herramientas import *

def main():
    r = "(ab**)"
    w = "aab"

    afn = crear_afn(r).obtener_objeto()
    afd =  afn_a_afd(afn).obtener_objeto()
    minAfd = afn_a_afd(afn).obtener_afd_min()


    existe_en_afd = "si" if validar_cadena(afd, w) else "no"
    existe_en_afn = "si" if validar_cadena(afn, w) else "no"
    print(f"AFD: {w} {existe_en_afd} existe en r ")
    print(f"AFN: {w} {existe_en_afn} existe en r ")


    mostrar_afn(afd, "dfa")
    mostrar_afn(afn, "nfa")
    mostrar_afn(minAfd, "mdfa")

if __name__ == '__main__':
    main()
