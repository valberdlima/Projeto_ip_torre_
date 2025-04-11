import pygame
import os

# Configurações básicas do jogo
Largura, Altura = 1000, 800
player_velocidade = 4
FPS = 60

# Iniciando o pygame
pygame.init()
tela = pygame.display.set_mode((Largura, Altura))
clock = pygame.time.Clock()

# Configuração da fonte do jogo
font_dialogo = pygame.font.Font('Fontes\PressStart2P-Regular.ttf', 15)  # Fonte principal para diálogos
font_instrucao = pygame.font.Font('Fontes\PressStart2P-Regular.ttf', 10)  # Fonte menor para [ENTER ou ESPAÇO]
font_mensagem = pygame.font.Font('Fontes\PressStart2P-Regular.ttf', 22) # Fonte da mensagem de coleta de itens
# Dimensões das sprites
SPRITE_Largura, SPRITE_Altura = 64, 64

# Dimensões das sprites BOSS
SPRITE_Largura_BOSS, SPRITE_Altura_BOSS = 64, 64

# Configurações da caixa de diálogo
DIALOGO_VELOCIDADE = 3  # Frames por letra
DIALOGO_MARGEM = 30  # Margem interna da caixa
DIALOGO_CAIXA_X = 20  # Canto inferior esquerdo
DIALOGO_CAIXA_Y = Altura - 175  # Ajustado para ficar acima da borda inferior
DIALOGO_CAIXA_LARGURA_MAX = Largura // 1.8  # Largura máxima
DIALOGO_CAIXA_ALTURA_MIN = 100  # Altura mínima
