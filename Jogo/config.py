# importa a biblioteca pygame
import os
import pygame 

# configuracoes basicas do jogo
Largura, Altura = 1000, 800 # tamanho da tela
player_velocidade = 4 
FPS = 60
SPRITE_Largura, SPRITE_Altura = 64, 64  

pygame.init()
tela = pygame.display.set_mode((Largura, Altura)) 
clock = pygame.time.Clock()

# Configuração de fonte para mensagens
fonte = pygame.font.SysFont("arial", 40)

# Áreas de colisão para o mapa "torre final"
colisoes_torre_final = [
    pygame.Rect(0, 0, 40, 165),  # Paredes rochosas superiores
    pygame.Rect(100, 0, 300, 60),  # Paredes rochosas superiores 2
    pygame.Rect(590, 0, 300, 20),  # Paredes rochosas superiores 3
    pygame.Rect(390, 20, 140, 200),  # Torre de pedra
    pygame.Rect(750, 0, 280, 400),  # Água superior
    pygame.Rect(855, 450, 280, 50), # Pier
    pygame.Rect(750, 525, 280, 40), # Água inferior
    pygame.Rect(800, 570, 280, 250), # Água inferior 2
    pygame.Rect(0, 650, 220, 100),  # Paredes rochosas inferiores
    pygame.Rect(250, 700, 130, 100),  # Paredes rochosas inferiores 2
    pygame.Rect(440, 770, 410, 100),  # Paredes rochosas inferiores 3
    pygame.Rect(240, 215, 8, 5),  # Esqueleto
    pygame.Rect(770, 450, 10, 20),  # Baú
]