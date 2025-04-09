import pygame
from config import SPRITE_Largura, SPRITE_Altura, player_velocidade
from assets import get_sprites, ANIM_Baixo, ANIM_Esquerda, ANIM_Direita, ANIM_Cima, ANIM_Baixo_Ataque, ANIM_Esquerda_Ataque, ANIM_Direita_Ataque, ANIM_Cima_Ataque

# Função para atualizar sprites
def atualizar_sprites(player, novo_spritesheet):
    global ANIM_Baixo, ANIM_Esquerda, ANIM_Direita, ANIM_Cima
    sprites = get_sprites(novo_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)

    ANIM_Baixo = sprites[130:139]
    ANIM_Esquerda = sprites[117:126]
    ANIM_Direita = sprites[143:152]
    ANIM_Cima = sprites[104:113]

    ANIM_Baixo_Ataque = sprites[53:62]
    ANIM_Esquerda_Ataque = sprites[66:75]
    ANIM_Direita_Ataque = sprites[79:88]
    ANIM_Cima_Ataque = sprites[92:101]

    player.direcao = ANIM_Baixo # Atualiza a direção atual do jogador

# Agora a classe herda de Sprite
class Player(pygame.sprite.Sprite):  
    def __init__(self, x, y):
        super().__init__()  

        self.x = x
        self.y = y
        self.frame = 0
        self.direcao = ANIM_Baixo
        self.animacao_contador = 0  # Contador para controlar a animação

        # Cria imagem e rect para usar com grupos do pygame
        self.image = self.direcao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def move(self, keys, colisoes):
        movendo = False
        novo_x, novo_y = self.x, self.y

        # Verifica as teclas pressionadas e atualiza a posição do jogador
        if keys[pygame.K_LEFT]:
            novo_x -= player_velocidade
            self.direcao = ANIM_Esquerda
            movendo = True
        if keys[pygame.K_RIGHT]:
            novo_x += player_velocidade
            self.direcao = ANIM_Direita
            movendo = True
        if keys[pygame.K_UP]:
            novo_y -= player_velocidade
            self.direcao = ANIM_Cima
            movendo = True
        if keys[pygame.K_DOWN]:
            novo_y += player_velocidade
            self.direcao = ANIM_Baixo
            movendo = True

        # Verifica colisões
        jogador_rect = pygame.Rect(novo_x, novo_y, SPRITE_Largura, SPRITE_Altura)
        if not any(jogador_rect.colliderect(colisao) for colisao in colisoes):
            self.x, self.y = novo_x, novo_y  # Atualiza posição se não houver colisão
            self.rect.topleft = (self.x, self.y)  # Atualiza a posição do rect

        # Controla a taxa de atualização da animação
        if movendo:
            self.animacao_contador += 1
            if self.animacao_contador % 5 == 0:  # Atualiza o frame a cada 5 ciclos
                self.frame = (self.frame + 1) % len(self.direcao)
        else:
            self.frame = 0
            self.animacao_contador = 0  # Reseta o contador quando parado

        # Atualiza imagem e rect com o novo frame e posição
        self.image = self.direcao[self.frame]
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.direcao[self.frame], (self.x, self.y))
