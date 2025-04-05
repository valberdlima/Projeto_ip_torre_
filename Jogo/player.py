from assets import ANIM_Baixo, ANIM_Esquerda, ANIM_Direita, ANIM_Cima
from config import player_velocidade, SPRITE_Largura, SPRITE_Altura
import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.direcao = ANIM_Baixo
        self.animacao_contador = 0  # Contador para controlar a animação

    def move(self, keys, colisoes):
        movendo = False
        novo_x, novo_y = self.x, self.y
        
        # verifica as teclas pressionadas e atualiza a posicao do jogador
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

        # Controla a taxa de atualização da animação
        if movendo:
            self.animacao_contador += 1
            if self.animacao_contador % 5 == 0:  # Atualiza o frame a cada 5 ciclos
                self.frame = (self.frame + 1) % len(self.direcao)
        else:
            self.frame = 0
            self.animacao_contador = 0  # Reseta o contador quando parado

    def draw(self, screen):
        screen.blit(self.direcao[self.frame], (self.x, self.y))