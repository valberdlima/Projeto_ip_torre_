import pygame
# Colisões dos Mapas

#Dimenções do pygame.Rect(x, y, largura, altura)
colisoes_primeiro_mapa = [
    pygame.Rect(0, 0, 1, 800),           # Parede lateral esquerda
    pygame.Rect(0, 0, 500, 1),           # Parede superior esquerda
    pygame.Rect(670, 0, 400, 1),         # Parede superior direita
    pygame.Rect(0, 799, 1000, 1),        # Parede inferior
    pygame.Rect(950, 0, 100, 250),       # Parede lateral direita superior
    pygame.Rect(800, 550, 200, 200),     # Parede lateral direita inferior
    pygame.Rect(0, 0, 200, 340),         # Bloco arvores e pedras esquerda
    pygame.Rect(0, 600, 50, 200),        # Arvore inferior
    pygame.Rect(80, 550, 50, 250),       # Arvore inferior
    pygame.Rect(260, 650, 240, 150),     # Lago
    pygame.Rect(650, 680, 350, 100),     # Floresta inferior direita
    pygame.Rect(860, 30, 50, 100),       # Arvore superior direita
    pygame.Rect(700, 80, 50, 100),       # Estatua
    pygame.Rect(390, 10, 160, 130),      # Arvore cercada
    pygame.Rect(410, 230, 70, 40),       # Fonte
    pygame.Rect(575, 245, 60, 105),      # Arvore central
    pygame.Rect(200, 40, 70, 30),        # Pedra superior esquerda
]

colisoes_segundo_mapa = [
    pygame.Rect(0, 0, 40, 165),          # Paredes rochosas superiores
    pygame.Rect(100, 0, 300, 60),        # Paredes rochosas superiores 2
    pygame.Rect(590, 0, 300, 20),        # Paredes rochosas superiores 3
    pygame.Rect(390, 20, 140, 200),      # Torre de pedra
    pygame.Rect(750, 0, 280, 400),       # Água superior
    pygame.Rect(855, 450, 280, 50),      # Pier
    pygame.Rect(750, 525, 280, 40),      # Água inferior
    pygame.Rect(800, 570, 280, 250),     # Água inferior 2
    pygame.Rect(0, 650, 220, 100),       # Paredes rochosas inferiores
    pygame.Rect(250, 700, 130, 100),     # Paredes rochosas inferiores 2
    pygame.Rect(440, 770, 410, 100),     # Paredes rochosas inferiores 3
    pygame.Rect(240, 215, 8, 5),         # Esqueleto
    pygame.Rect(770, 450, 10, 20),       # Baú
]

#Dimenções do pygame.Rect(x, y, largura, altura)
colisoes_terceiro_mapa = [
    pygame.Rect(0, 0, 90, 800),          # Parede esquerda
    pygame.Rect(0, 0, 1000, 20),         # Parede superior total
    pygame.Rect(0, 0, 200, 100),         # Parede superior esquerda
    pygame.Rect(720, 0, 200, 100),       # Parede superior direita
    pygame.Rect(900, 0, 1, 1200),        # Parede direita
    pygame.Rect(0, 800, 430, 1),         # Parede inferior esquerda
    pygame.Rect(560, 800, 500, 1),       # Parede inferior direita
    pygame.Rect(0, 190, 200, 130),       # Lago superior esquerdo
    pygame.Rect(280, 190, 100, 80),      # Buraco central superior esquerdo
    pygame.Rect(320, 400, 80, 80),       # Buraco central inferior esquerdo
    pygame.Rect(670, 600, 110, 90),      # Buraco inferior direito
    pygame.Rect(330, 560, 45, 50),       # Estátua meio inferior esquerdo
    pygame.Rect(720, 345, 80, 50),       # Cones lado direito
]

#Dimenções do pygame.Rect(x, y, largura, altura)
colisoes_mapa_torre = [
    pygame.Rect(0, 0, 1000, 200),        # Parede fundo
    pygame.Rect(0, 210, 60, 30),         # Parede fundo esquerda
    pygame.Rect(945, 210, 60, 30),       # Parede fundo direita
    pygame.Rect(0, 0, 3, 800),           # Parede lateral esquerda
    pygame.Rect(997, 0, 3, 800),         # Parede lateral direita
    pygame.Rect(0, 750, 20, 50),         # Parede lateral direita
    pygame.Rect(970, 750, 20, 50),       # Parede lateral direita
    pygame.Rect(30, 795, 385, 3),        # Parede inferior esquerda
    pygame.Rect(600, 795, 400, 3),       # Parede inferior direita
    #pygame.Rect(0, 850, 1000, 1),       # Barreira porta
    pygame.Rect(140, 220, 30, 80),       # Estatua superior esquerda
    pygame.Rect(800, 220, 30, 80),       # Estatua superior direita
    pygame.Rect(20, 420, 60, 50),        # Estatua meio esquerda
    pygame.Rect(920, 420, 30, 50),       # Estatua meio direita
    pygame.Rect(135, 670, 30, 50),       # Estatua inferior esquerda
    pygame.Rect(825, 670, 30, 50),       # Estatua inferior direita
    pygame.Rect(490, 210, 20, 35),       # Trono
]