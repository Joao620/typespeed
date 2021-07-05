from objetos.palavras_ambulante import Palavras_ambulante
import curses
from typing import List
from functools import partial
import threading
from time import sleep


class Terminal():
	def __init__(self, screen):
		self.screen = screen
		self.largura_tela = curses.COLS
		self.altura_tela = curses.LINES

		self.barra_superior = self.altura_tela // 2 - 3
		self.barra_inferior = self.altura_tela // 2 + 3
		self.altura_barras = self.barra_inferior - self.barra_superior - 1

		self.desenhar_tela()
		self.window_palavras = self.iniciar_window_palavras()
		self.window_teclas = self.iniciar_window_teclado()
		
		self.windows_pontuacao = self.iniciar_window_pontuacao()
		self.pontuacao = 0

		self.iniciar_cores_terminal()

	def iniciar_cores_terminal(self):
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)

	def iniciar_window_palavras(self):
		cord_y = self.barra_superior + 1
		cord_x = 0

		altura = self.barra_inferior - self.barra_superior - 1
		largura = self.largura_tela

		return curses.newwin(altura, largura, cord_y, cord_x)

	def iniciar_window_teclado(self):
		cord_y = self.altura_tela - 3
		cord_x = 0

		altura = 1
		largura = self.largura_tela

		return curses.newwin(altura, largura, cord_y, cord_x)

	def iniciar_window_pontuacao(self):
		cord_y = max(self.barra_superior - 3, 0)
		cord_x = 0

		altura = 1
		largura = self.largura_tela

		return curses.newwin(altura, largura, cord_y, cord_x)

	def desenhar_tela(self):
		barra = "#" * self.largura_tela

		self.screen.clear()
		self.screen.addstr(self.barra_superior, 0, barra)
		self.screen.addstr(self.barra_inferior, 0, barra)
		self.screen.refresh()

	def update(self, palavras: List[Palavras_ambulante]):
		"""atualização de palavras feita pelo ``gerenciador_palavras``

		Vai atualizar as palavras na tela em relação com o parametro ``palavras``

		Param:
				palavras: lista contendo as novas palavras que vão ser escritas na tela
		"""
		self.window_palavras.clear()
		for palavra in palavras:

			espaco_ocupado_palavra = palavra.coluna + palavra.tamanho_texto
			if espaco_ocupado_palavra > self.largura_tela:
				espaco_maximo = self.largura_tela - espaco_ocupado_palavra
				palavra_escrita = palavra.texto[0:espaco_maximo]
			else:
				palavra_escrita = palavra.texto

			try:
				self.window_palavras.addstr(palavra.linha, palavra.coluna, palavra_escrita)
				
				if palavra.letras_coloridas > 0:
					quantidade_letras_coloridas = min(len(palavra_escrita), palavra.letras_coloridas)
					palavra_colorida = palavra_escrita[:quantidade_letras_coloridas]

					self.window_palavras.addstr(
						palavra.linha, palavra.coluna, palavra_colorida, curses.color_pair(palavra.cor))
					

			except Exception as e:
				# acontece que tem uma espécie de bug que se alguma coisa é printada no canto inferior direito da tela
				# ele causa um erro só por causar, mesmo que seja printado normalmente, por isso esse try está aqui
				pass

		self.window_palavras.refresh()

	def somar_pontuacao(self, soma_pontuacao: int):
		self.pontuacao += soma_pontuacao
		str_pontuacao = str(self.pontuacao)
		metade_tela = self.largura_tela // 2 - len(str_pontuacao) // 2

		self.windows_pontuacao.addstr(0, metade_tela, str_pontuacao)
		self.windows_pontuacao.refresh()

	def atualizar_teclas(self, palavras: List[str]):
		"""Atualiza as teclas digitadas que ficam em baixo da corrida"""
		self.window_teclas.clear()
		metade_tela = self.largura_tela // 2 - len(palavras) // 2

		offset = 0
		for palavra in palavras:
			self.window_teclas.addch(0, metade_tela + offset, palavra)
			offset += 1

		self.window_teclas.refresh()

	def perder(self):
		frase = 'perdeu, jogo reiniciando...'

		metade_tela_frase = self.largura_tela // 2 - len(frase) // 2
		self.window_palavras.addstr(0, metade_tela_frase - 1, ' ' * (len(frase) + 2))
		self.window_palavras.addstr(0, metade_tela_frase, frase)

		frase = 'para sair aperte Ctrl+C'
		metade_tela_frase = self.largura_tela // 2 - len(frase) // 2
		self.window_palavras.addstr(1, metade_tela_frase - 1, ' ' * (len(frase) + 2))
		self.window_palavras.addstr(1, metade_tela_frase, frase)


		tamanho_carregador = 3
		metade_tela_carregador = self.largura_tela // 2 - tamanho_carregador

		self.window_palavras.addstr(2, metade_tela_carregador - tamanho_carregador, '[')
		self.window_palavras.addstr(2, metade_tela_carregador + tamanho_carregador, ']')
		self.window_palavras.refresh()

		index = metade_tela_carregador - tamanho_carregador

		while index < metade_tela_carregador + tamanho_carregador:
			sleep(1)
			index += 1
			self.window_palavras.addstr(2, index, '#')
			self.window_palavras.refresh()

		return

