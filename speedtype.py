from objetos.teclado import Teclado
from objetos.terminal import Terminal
from objetos.movedor import Movedor
from objetos.gerenciador_palavras import Gerenciador_palavras
import curses
from time import sleep

def iniciar_teclado(stdscr, gp, terminal):
    teclado = Teclado(stdscr.get_wch, gp, terminal.atualizar_teclas, terminal.somar_pontuacao)
    return teclado

def iniciar_movedor(gp, terminal):
    if curses.has_colors():
        cores_disponivel = (1, 2, 3, 4, 5, 6)
    else:
        cores_disponivel = (0)

    movedor = Movedor(gp, cores_disponivel, terminal.altura_barras, curses.COLS, terminal.somar_pontuacao, terminal.perder)
    return movedor

def main(stdscr):
    while True:
        curses.curs_set(0)  #deixa o cursos invisivel
        gp = Gerenciador_palavras()
        terminal = Terminal(stdscr)

        teclado = iniciar_teclado(stdscr, gp, terminal)
        movedor = iniciar_movedor(gp, terminal)
        
        gp.inscrever(terminal)
        
        movedor.join()


if __name__ == '__main__':
    curses.wrapper(main)