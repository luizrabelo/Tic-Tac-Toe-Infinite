import os
import random

class JogoDaVelhaDinamico:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.historico = {'X': [], 'O': []}  # Histórico separado por jogador

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela (Windows ou Linux/Mac)

    def mostrar_tabuleiro(self):
        print("     1   2   3")  # Cabeçalho das colunas
        print("   +---+---+---+")
        for i, linha in enumerate(self.tabuleiro, start=1):
            print(f" {i} | " + " | ".join(linha) + " |")  # Linhas com numeração
            print("   +---+---+---+")

    def jogada(self, jogador, linha, coluna):
        if self.tabuleiro[linha - 1][coluna - 1] == ' ':  # Índices ajustados para começar em 1
            self.tabuleiro[linha - 1][coluna - 1] = jogador
            self.historico[jogador].append((linha - 1, coluna - 1))  # Salva a jogada no histórico do jogador
            if len(self.historico[jogador]) > 3:  # Remove a jogada mais antiga se exceder o limite
                antiga_linha, antiga_coluna = self.historico[jogador].pop(0)
                self.tabuleiro[antiga_linha][antiga_coluna] = ' '
            return True
        return False

    def verificar_vencedor(self, jogador):
        # Verifica linhas, colunas e diagonais para identificar um vencedor
        for i in range(3):
            if all(self.tabuleiro[i][j] == jogador for j in range(3)) or \
               all(self.tabuleiro[j][i] == jogador for j in range(3)):
                return True
        if all(self.tabuleiro[i][i] == jogador for i in range(3)) or \
           all(self.tabuleiro[i][2 - i] == jogador for i in range(3)):
            return True
        return False

    def jogada_ia(self):
        # IA faz jogadas em posições aleatórias disponíveis
        while True:
            linha, coluna = random.randint(1, 3), random.randint(1, 3)
            if self.tabuleiro[linha - 1][coluna - 1] == ' ':
                return linha, coluna

    def jogo(self):
        jogadores = ['X', 'O']
        turno = 0
        print("Modo: Homem vs Máquina")
        while True:
            self.limpar_tela()  # Limpa a tela a cada turno
            self.mostrar_tabuleiro()
            jogador = jogadores[turno % 2]
            if jogador == 'X':  # Jogador humano
                print(f"Turno do jogador {jogador}")
                linha = int(input("Escolha a linha (1-3): "))
                coluna = int(input("Escolha a coluna (1-3): "))
            else:  # Máquina (IA)
                print("Turno da IA...")
                linha, coluna = self.jogada_ia()

            if self.jogada(jogador, linha, coluna):
                if self.verificar_vencedor(jogador):
                    self.limpar_tela()  # Limpa a tela antes de mostrar o resultado
                    self.mostrar_tabuleiro()
                    print(f"Jogador {jogador} venceu!")
                    break  # Encerra o jogo após identificar um vencedor
                turno += 1
            else:
                print("Jogada inválida. Tente novamente.")

# Inicializar o jogo
jogo = JogoDaVelhaDinamico()
jogo.jogo()
