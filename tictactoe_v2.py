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

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela (Windows ou Linux/Mac)

    def mostrar_tabuleiro(self):
        print("\n        1       2       3")  # Cabeçalho das colunas
        print("   " + "+-------+-------+-------+")
        for i, linha in enumerate(self.tabuleiro, start=1):
            print(f" {i} " + "|       |       |       |")
            print(f"   " + "|   " + "   |   ".join([self._colorize(c) for c in linha]) + "   |")
            print(f"   " + "|       |       |       |")
            print("   " + "+-------+-------+-------+")

    def _colorize(self, char):
        if char == 'X':
            return f"{Fore.RED}{char}{Style.RESET_ALL}"  # Cor vermelha para X
        elif char == 'O':
            return f"{Fore.BLUE}{char}{Style.RESET_ALL}"  # Cor azul para O
        return ' '  # Espaço vazio sem cor

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

    def mostrar_placar(self):
        print("\nPlacar Atual:")
        print(f"{Fore.RED}Jogador X: {self.placar['X']}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Jogador O: {self.placar['O']}{Style.RESET_ALL}\n")

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

    def reiniciar_tabuleiro(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.historico = {'X': [], 'O': []}

    def jogo(self):
        self.escolher_modo_jogo()  # Escolher entre 1 ou 2 jogadores
        jogadores = ['X', 'O']
        turno = 0
        while True:
            self.limpar_tela()  # Limpa a tela a cada turno
            self.mostrar_placar()  # Mostra o placar atualizado
            self.mostrar_tabuleiro()
            jogador = jogadores[turno % 2]

            if self.modo_jogo == 1 and jogador == 'O':  # Modo contra IA
                print("Turno da IA...")
                linha, coluna = self.jogada_ia()
            else:  # Jogador humano
                print(f"Turno do jogador {jogador}")
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
                    print(f"Jogador {jogador} venceu!")
                    self.placar[jogador] += 1
                    self.mostrar_placar()

                    # Perguntar se deseja jogar novamente
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
