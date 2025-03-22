import os
import random
from colorama import Fore, Style, init

class JogoDaVelhaDinamico:
    def __init__(self):
        init(autoreset=True)  # Inicializa o colorama para gerenciar as cores
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.historico = {'X': [], 'O': []}
        self.placar = {'X': 0, 'O': 0}  # Placar dos jogadores
        self.modo_jogo = None  # Escolha do modo de jogo
        self.jogadores = {'X': 'Jogador X', 'O': 'Jogador O'}  # Nomes dos jogadores

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela (Windows ou Linux/Mac)

    def mostrar_tabuleiro(self):
        print("\n        1       2       3")
        print("   " + "+-------+-------+-------+")
        for i, linha in enumerate(self.tabuleiro, start=1):
            print("   " + "|       |       |       |")
            linha_formatada = "   |   ".join([self._esmaecer(c, jogador='X') for c in linha])
            print(f" {i} " + f"|   {linha_formatada}   | {i}")
            print("   " + "|       |       |       |")
            print("   " + "+-------+-------+-------+")
        print("        1       2       3")

    def _esmaecer(self, char, jogador):
        # Aplica o efeito de esmaecer apenas à peça mais antiga no histórico
        if char == jogador and self.historico[jogador]:
            linha_antiga, coluna_antiga = self.historico[jogador][0]
            if self.tabuleiro[linha_antiga][coluna_antiga] == char:
                return f"{Fore.LIGHTBLACK_EX}{char}{Style.RESET_ALL}"
        # Aplica cor padrão às outras peças
        if char == 'X':
            return f"{Fore.RED}{char}{Style.RESET_ALL}"
        elif char == 'O':
            return f"{Fore.BLUE}{char}{Style.RESET_ALL}"
        return ' '  # Espaço vazio sem cor

    def jogada(self, jogador, linha, coluna):
        if self.tabuleiro[linha - 1][coluna - 1] == ' ':
            self.tabuleiro[linha - 1][coluna - 1] = jogador
            self.historico[jogador].append((linha - 1, coluna - 1))
            if len(self.historico[jogador]) > 3:  # Remove a jogada mais antiga
                antiga_linha, antiga_coluna = self.historico[jogador].pop(0)
                self.tabuleiro[antiga_linha][antiga_coluna] = ' '
            return True
        return False

    def verificar_vencedor(self, jogador):
        for i in range(3):
            if all(self.tabuleiro[i][j] == jogador for j in range(3)) or \
               all(self.tabuleiro[j][i] == jogador for j in range(3)):
                return True
        if all(self.tabuleiro[i][i] == jogador for i in range(3)) or \
           all(self.tabuleiro[i][2 - i] == jogador for i in range(3)):
            return True
        return False

    def jogada_ia(self):
        while True:
            linha, coluna = random.randint(1, 3), random.randint(1, 3)
            if self.tabuleiro[linha - 1][coluna - 1] == ' ':
                return linha, coluna

    def mostrar_placar(self):
        print("\nPlacar Atual:")
        print(f"{Fore.RED}{self.jogadores['X']}: {self.placar['X']}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{self.jogadores['O']}: {self.placar['O']}{Style.RESET_ALL}\n")

    def escolher_modo_jogo(self):
        while True:
            try:
                print("Escolha o modo de jogo:")
                print("1 - Jogador vs IA")
                print("2 - Jogador vs Jogador")
                self.modo_jogo = int(input("Digite 1 ou 2: "))
                if self.modo_jogo not in [1, 2]:
                    raise ValueError
                break
            except ValueError:
                print("Entrada inválida. Escolha 1 ou 2.")

    def definir_nomes_jogadores(self):
        print("\nVamos personalizar os nomes dos jogadores!")
        self.jogadores['X'] = input("Digite o nome do jogador X: ").strip() or "Jogador X"
        self.jogadores['O'] = input("Digite o nome do jogador O (ou pressione Enter para 'IA'): ").strip() or "IA"

    def reiniciar_tabuleiro(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.historico = {'X': [], 'O': []}

    def jogo(self):
        self.escolher_modo_jogo()  # Escolher entre 1 ou 2 jogadores
        self.definir_nomes_jogadores()  # Definir nomes dos jogadores
        jogadores = ['X', 'O']
        turno = 0
        while True:
            self.limpar_tela()
            self.mostrar_placar()
            self.mostrar_tabuleiro()
            jogador = jogadores[turno % 2]
            jogador_nome = self.jogadores[jogador]

            if self.modo_jogo == 1 and jogador == 'O':  # Modo contra IA
                print("Turno da IA...")
                linha, coluna = self.jogada_ia()
            else:  # Jogador humano
                print(f"Turno do {jogador_nome}")
                try:
                    linha = int(input("Escolha a linha (1-3): "))
                    coluna = int(input("Escolha a coluna (1-3): "))
                    if linha not in range(1, 4) or coluna not in range(1, 4):
                        raise ValueError
                except ValueError:
                    print("Entrada inválida! Certifique-se de digitar números entre 1 e 3.")
                    input("Pressione Enter para continuar...")
                    continue

            if self.jogada(jogador, linha, coluna):
                if self.verificar_vencedor(jogador):
                    self.limpar_tela()
                    self.mostrar_tabuleiro()
                    print(f"{jogador_nome} venceu!")
                    self.placar[jogador] += 1
                    self.mostrar_placar()
                    continuar = input("Deseja jogar novamente? (s/n): ").lower()
                    if continuar == 's':
                        self.reiniciar_tabuleiro()
                        turno = 0
                        continue
                    else:
                        print("Obrigado por jogar!")
                        break
                turno += 1
            else:
                print("Jogada inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

# Inicializar o jogo
if __name__ == "__main__":
    jogo = JogoDaVelhaDinamico()
    jogo.jogo()