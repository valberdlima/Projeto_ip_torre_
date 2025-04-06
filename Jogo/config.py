import pygame
import os

# Configurações básicas do jogo
Largura, Altura = 1000, 800
player_velocidade = 4
FPS = 60

# iniciando o pygame
pygame.init()
tela = pygame.display.set_mode((Largura, Altura)) # ja redimensionei direto na tela
clock = pygame.time.Clock()

# configuracao da fonte do jogo
font_alagard = pygame.font.Font('alagard.ttf', 40)

# dimensoes das sprites
SPRITE_Largura, SPRITE_Altura = 64, 64