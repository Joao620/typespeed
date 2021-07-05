from objetos.palavras_ambulante import Palavras_ambulante
from typing import List
from threading import Lock

class Gerenciador_palavras:
    def __init__(self):
        self._lista_palavras: List[Palavras_ambulante] = []
        self.ouvintes: List[object] = set()
        self.lock = Lock()

    def get_ref_lista(self) -> List[Palavras_ambulante]:
        with self.lock:
            return self._lista_palavras

    def avancar_palavras(self) -> bool:
        """avança todas palavras em uma posição, caso a posição seja menor que zero, retorna false"""

        with self.lock:
            for palavra in self._lista_palavras:
                palavra.coluna -= 1 
                if palavra.coluna < 0:
                    return False
                
        self.atualizar_ouvintes()
        return True

    def remover_palavra(self, palavra: Palavras_ambulante) -> bool:
        """remove certa palavra da lista e atualiza os ouvinte se houve remoção"""
        palavras_iguais = list(filter(lambda x: x.texto == palavra, self._lista_palavras))
        
        if len(palavras_iguais) > 0:
            with self.lock:
                self._lista_palavras.remove(palavras_iguais[0])

            self.atualizar_ouvintes()
            return True

        return False

    def adicionar_palavras(self, palavra):
        with self.lock:
            self._lista_palavras.append(palavra)

    def colorir_palavras(self, texto: str):
        for palavra in self._lista_palavras:
            palavra.letras_coloridas = 0

        palavras_colisoes = list(filter(lambda x: x.texto.startswith(texto), self._lista_palavras))

        if len(palavras_colisoes) > 0:
            for palavra in palavras_colisoes:
                palavra.letras_coloridas = len(texto)

        self.atualizar_ouvintes()

    def inscrever(self, quem: object):
        if hasattr(quem, 'update'):
            self.ouvintes.add(quem)

    def _desinscrever(self, quem: object):
        self.ouvintes.discard(quem)

    def atualizar_ouvintes(self):
        for ouvinte in self.ouvintes:
            ouvinte.update(self._lista_palavras.copy())
