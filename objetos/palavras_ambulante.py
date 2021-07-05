class Palavras_ambulante:
    """Tipo uma struct contendo dados necessários para escrever uma palavra no teminal"""
    def __init__(self, texto, linha, coluna, cor):
        self.texto = texto
        self.tamanho_texto = len(texto)
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
        self.letras_coloridas = 0
