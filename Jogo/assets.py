import pygame
from config import Largura, Altura, SPRITE_Largura, SPRITE_Altura

# carrega as imagens
mapas = {
    "primeiro mapa": pygame.transform.scale(pygame.image.load("mapa_1.png"), (Largura, Altura)),
    "segundo mapa": pygame.transform.scale(pygame.image.load("mapa_2.png"), (Largura, Altura)),
    "torre": pygame.transform.scale(pygame.image.load("mapa_torre.png"), (Largura, Altura))
}

player_spritesheet = pygame.transform.scale(pygame.image.load("personagem.png"), (832, 3456))
player_spritesheet2 = pygame.transform.scale(pygame.image.load("Person_Manto.png"), (832, 3456))
player_spritesheet3 = pygame.transform.scale(pygame.image.load("Person_Manto_Cajado.png"), (1536, 4224))

# funcao para carregar os sprites do spritesheet
def get_sprites(sheet, linhas, colunas, largura, altura):
    sprites = []
    for linha in range(linhas): # itera pelas linhas do spritesheet
        for coluna in range(colunas): # itera pelas colunas do spritesheet
            # calcula a posicao do sprite
            x = coluna * largura
            y = linha * altura
            sprite = sheet.subsurface(pygame.Rect(x, y, largura, altura))
            sprites.append(sprite)
    return sprites

# carrega as sprites do jogador
sprites = get_sprites(player_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)
ANIM_Baixo = sprites[130:139]
ANIM_Esquerda = sprites[117:126]
ANIM_Direita = sprites[143:152]
ANIM_Cima = sprites[104:113]