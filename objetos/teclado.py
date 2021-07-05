import curses
import curses.ascii
import threading
from typing import Callable, Iterable
from objetos.palavras_ambulante import Palavras_ambulante
from objetos.gerenciador_palavras import Gerenciador_palavras

from threading import Lock
import traceback


class Teclado(threading.Thread):
	def __init__(self, get_input: Callable[[None], str], gerenciador_palavras: Gerenciador_palavras, mostrar_teclas: Callable[[str], None], somar_pontuacao):
		super().__init__(daemon=True)

		self.get_input = get_input
		self.mostrar_teclas = mostrar_teclas

		self.gerenciador_palavras = gerenciador_palavras
		self.lista_palavras = []
		self.lock_lista_palavras = Lock()

		self.somar_pontuacao = somar_pontuacao

		self.start()

	def run(self):

		buffer_letras = []
	
		while True:
			letra = self.get_input()
			# caso seja a tecla apagar ele tira a ultima letra
			if letra == curses.KEY_BACKSPACE:
				if len(buffer_letras) > 0:
					buffer_letras.pop()

			# testa pra se a combinação ctrl + apagar foram apertadas e apaga todo o texto
			elif type(letra) == str and ord(letra) == 8:
				buffer_letras = []

			# se a letra é realmente uma letra acentuada ou não
			elif type(letra) == str and curses.ascii.ismeta(letra) or curses.ascii.isalpha(letra):
				buffer_letras.append(letra)

			palavra = ''.join(buffer_letras)
			if self.gerenciador_palavras.remover_palavra(palavra):
				self.somar_pontuacao(20)
				buffer_letras = []

			self.mostrar_teclas(buffer_letras)
			self.gerenciador_palavras.colorir_palavras(palavra)


	def updade(self, nova_lista_palavras: Iterable[Palavras_ambulante]):
		with self.lock_lista_palavras:
			self.lista_palavras = nova_lista_palavras
