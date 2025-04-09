import pygame
from config import Largura, Altura, SPRITE_Largura, SPRITE_Altura, SPRITE_Largura_BOSS,SPRITE_Altura_BOSS

# carrega as imagens
mapas = {
    "primeiro mapa": pygame.transform.scale(pygame.image.load("mapa_1.png"), (Largura, Altura)),
    "segundo mapa": pygame.transform.scale(pygame.image.load("mapa_2.png"), (Largura, Altura)),
    "torre": pygame.transform.scale(pygame.image.load("mapa_torre.png"), (Largura, Altura))
}
# Player spritesheet
player_spritesheet = pygame.transform.scale(pygame.image.load("personagem.png"), (832, 3456))
player_spritesheet2 = pygame.transform.scale(pygame.image.load("Person_Manto.png"), (832, 3456))
player_spritesheet3 = pygame.transform.scale(pygame.image.load("Person_Manto_Cajado.png"), (832, 3456))


##print(pygame.image.load("personagem.png").get_size())
# Boss Spritesheet

BOSS_WIND_SPRITESHEET = pygame.image.load("boss_sprites.png").convert_alpha()
print(BOSS_WIND_SPRITESHEET.get_width(), BOSS_WIND_SPRITESHEET.get_height())

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

sprites2 = get_sprites(player_spritesheet3, 54, 13, SPRITE_Largura, SPRITE_Altura)
ANIM_Baixo_Ataque = sprites2[78:86]
ANIM_Esquerda_Ataque = sprites2[65:73]
ANIM_Direita_Ataque = sprites2[91:99]
ANIM_Cima_Ataque = sprites2[52:60]

# FUNÇÃO DE SLICE
def get_sprites(sheet, linhas, colunas, largura, altura):
    sprites = []
    for linha in range(linhas):
        for coluna in range(colunas):
            x = coluna * largura
            y = linha  * altura
            sprite = sheet.subsurface(pygame.Rect(x, y, largura, altura))
            sprites.append(sprite)
    return sprites

# BOSS ANIMAÇÃO
boss_sprites = get_sprites(BOSS_WIND_SPRITESHEET, 25, 5, SPRITE_Largura_BOSS, SPRITE_Altura_BOSS)

ANIM_BOSS_WALK_DOWN  = boss_sprites[ 0: 5]   # linha 0
ANIM_BOSS_WALK_LEFT  = boss_sprites[ 5:10]   # linha 1
ANIM_BOSS_WALK_RIGHT = boss_sprites[10:15]   # linha 2
ANIM_BOSS_WALK_UP    = boss_sprites[15:20]   # linha 3

ANIM_BOSS_IDLE       = boss_sprites[20:25]   # linha 4
ANIM_BOSS_ATTACK     = boss_sprites[25:30]   # linha 5
ANIM_BOSS_DAMAGE     = boss_sprites[30:35]   # linha 6
ANIM_BOSS_DEATH      = boss_sprites[35:40]   # linha 7
