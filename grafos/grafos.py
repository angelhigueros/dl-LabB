# Angel Higueros
# 20460
# Laboratorio B

from os import popen

def mostrar_afn(automata, file=""):  # sourcery skip: raise-specific-error
    try:
        with popen(f"dot -Tpng -o {file}.png", 'w') as f:
            f.write(automata.getDotFile())
    except:
        raise BaseException("[! No se pudo crear el grafico]")
