from objetos.palavras_ambulante import Palavras_ambulante
from objetos.gerenciador_palavras import Gerenciador_palavras
from typing import List, Optional, Tuple
from random import shuffle, choice
from time import sleep, time
import threading

class Movedor(threading.Thread):
    def __init__(self, gerenciador_palavras: Gerenciador_palavras, cores: Tuple[int], quantidade_linhas: int, quantidade_colunas: int, somar_pontuacao, perder) -> None:
        super().__init__(daemon=True)

        self.arquivo_palavras = 'palavrasDoFelipe.txt'
        self.codificacao = 'utf-8'

        self.gerenciador_palavras = gerenciador_palavras

        self.cores = cores

        # dimensões do quadrado que vai ficar as palavras
        self.quantidade_linhas = quantidade_linhas
        self.quantidade_colunas = quantidade_colunas

        self.somar_pontuacao = somar_pontuacao
        self.perder = perder

        self.velocidade = 0.5
        self.delay_adicionar_palavra = 2
        self.quantidade_soma_pontuacao = 1

        self.start()

    def run(self):
        lista_palavras = self.abrir_e_separar_csv()
        # esse '- self.delay_adicionar_palavra' é pra começar o jogo já com uma palavra correndo
        ultima_palavra_adicionada = time() - self.delay_adicionar_palavra

        delta_time = time()

        while True:
            # se já está na hora de adicionar uma nova palavra
            if ultima_palavra_adicionada + self.delay_adicionar_palavra < time():
                linha = self.posicao_aleatoria_para_palavra()
                # se não tiver linha disponível, não atualiza a variavel ``ultima_palavra_adicionada``
                # e tenta na proxima movida de palavras
                if linha != None:
                    coluna = self.quantidade_colunas
                    cor = choice(self.cores)
                    texto = choice(lista_palavras)
                    palavra = Palavras_ambulante(texto, linha, coluna, cor)
                    self.gerenciador_palavras.adicionar_palavras(palavra)

                    ultima_palavra_adicionada = time()

            vivo = self.gerenciador_palavras.avancar_palavras()
            if not vivo:
                self.perder()
                break

            self.somar_pontuacao(self.quantidade_soma_pontuacao)

            diff_time = time() - delta_time
            delta_time = time()

            self.velocidade = max(0.1, self.velocidade - (0.01 * diff_time))
            self.delay_adicionar_palavra = max(1, self.delay_adicionar_palavra - (0.005 * diff_time))

            sleep(self.velocidade)

    def abrir_e_separar_csv(self) -> List[str]:
        """vai abrir um arquivo no formato CSV contendo as palavras o jogo vai conter"""
        with open(self.arquivo_palavras, 'r', encoding=self.codificacao) as ioObj:
            palavras = ioObj.read()

        return palavras.split(',')

    def posicao_aleatoria_para_palavra(self) -> Optional[int]:
        """Retorna uma linha valida para posicionar uma palavra

        Return:
            Retorna uma linha valida baseado no atributo ``quantidade_linhas``

            Se não tiver nenhuma posição disponível vai retornar ``None``
        """

        # cuidado essa lista que ela é uma referencia
        lista_palavras = self.gerenciador_palavras.get_ref_lista()

        # vai aleatoriza a ordem das linhas que ele vai testar se está livre
        linhas_aleatorias = list(range(self.quantidade_linhas))
        shuffle(linhas_aleatorias)

        for linha in linhas_aleatorias:
            # vai procurar a primeira palavra nessa linha
            for palavra in reversed(lista_palavras):
                if palavra.linha == linha:
                    palavra_a_frente = palavra
                    break
            else:
                #  quer dizer que não tem nenhuma palavra na frente
                return linha

            # testa se a palavra não está atrapalhando para colocar a minha
            espaco_ocupado = palavra_a_frente.coluna + palavra_a_frente.tamanho_texto
            if self.quantidade_colunas > espaco_ocupado:
                return linha

        # se todas opções falharem retorna None
        return None
