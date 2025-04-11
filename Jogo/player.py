import pygame
from config import SPRITE_Largura, SPRITE_Altura, player_velocidade
from assets import get_sprites, ANIM_Baixo, ANIM_Esquerda, ANIM_Direita, ANIM_Cima, ANIM_Baixo_Ataque, ANIM_Esquerda_Ataque, ANIM_Direita_Ataque, ANIM_Cima_Ataque, ANIM_Morte, mapas, sprite_barra_vida

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

# class para os projeteis do player
class Projectplay(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direcao): # def principal do projetil
        super().__init__() # inicializa
        projetil_player = pygame.image.load("projetil_player.png").convert_alpha()  # carrega a sprite do projetil
        self.image = pygame.transform.scale(projetil_player, (72, 72))  # ajusta o tamanho da sprite
        self.rect = self.image.get_rect(center = (x, y)) # faz um quadrado em volta do projetil
        
        # define a velocidade com base na direcao
        if direcao == ANIM_Direita_Ataque:
            self.velocidade_x, self.velocidade_y = 8, 0
        elif direcao == ANIM_Esquerda_Ataque:
            self.velocidade_x, self.velocidade_y = -8, 0
        elif direcao == ANIM_Cima_Ataque:
            self.velocidade_x, self.velocidade_y = 0, -8
        elif direcao == ANIM_Baixo_Ataque:
            self.velocidade_x, self.velocidade_y = 0, 8
        else:
            self.velocidade_x, self.velocidade_y = 0, -8  # padrao pra cima

    def update(self): # atualiza o projetil
        # movimento continuo do projetil
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        
        # remove o projetil se sair da tela
        if (self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width() or
            self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height()):
            self.kill()

# Agora a classe herda de Sprite
class Player(pygame.sprite.Sprite):  
    def __init__(self, x, y):
        super().__init__()  

        self.x = x
        self.y = y
        self.frame = 0
        self.direcao = ANIM_Baixo
        self.animacao_contador = 0  # Contador para controlar a animação
        self.tempo_ataque = 0  # contador para controlar o tempo de ataque
        self.morte = False  # controle de morte do jogador

        # Cria imagem e rect para usar com grupos do pygame
        self.image = self.direcao[self.frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        # atributos de vida do jogador
        self.max_vida = 100
        self.vida_atual = self.max_vida
        self.barra_vida = 50  # tamanho da barra de vida
        self.relacao = self.max_vida / self.barra_vida # cada pixel da barra de vida representa 2 de vida
        
    def move(self, keys, colisoes, objetos_coletados):
        movendo = False
        atacando = False
        novo_x, novo_y = self.x, self.y
        
        if self.tempo_ataque > 0: # fica atualizando o tempo de ataque
            self.tempo_ataque -= 1
        
        # atualiza imagem e rect com o novo frame e posição
        self.image = self.direcao[self.frame]
        self.rect.topleft = (self.x, self.y)

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

        # Verifica se o jogador está atacando
        if keys[pygame.K_a] and objetos_coletados > 1:  # Tecla de ataque
            atacando = True
            if self.direcao == ANIM_Baixo:
                self.direcao = ANIM_Baixo_Ataque
            elif self.direcao == ANIM_Esquerda:
                self.direcao = ANIM_Esquerda_Ataque
            elif self.direcao == ANIM_Direita:
                self.direcao = ANIM_Direita_Ataque
            elif self.direcao == ANIM_Cima:
                self.direcao = ANIM_Cima_Ataque

        # Verifica colisões
        jogador_rect = pygame.Rect(novo_x, novo_y, SPRITE_Largura, SPRITE_Altura)
        if not any(jogador_rect.colliderect(colisao) for colisao in colisoes):
            self.x, self.y = novo_x, novo_y  # Atualiza posição se não houver colisão
            self.rect.topleft = (self.x, self.y)  # Atualiza a posição do rect

        # Controla a taxa de atualização da animação
        if movendo or atacando:
            self.animacao_contador += 1
            if self.animacao_contador % 4 == 0:  # Atualiza o frame a cada 4 ciclos
                self.frame = (self.frame + 1) % len(self.direcao)
        else:
            self.frame = 0
            self.animacao_contador = 0  # Reseta o contador quando parado
        
        # atualiza o tempo de ataque
        if self.animacao_contador % 4 == 0:  # atualiza o frame a cada 4 ciclos
            self.frame = (self.frame + 1) % len(self.direcao)  # garante que o indice esteja dentro dos limites
        #repassa as informações para o rect
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.direcao[self.frame], (self.x, self.y))
    
    # desenha a barra de vida na tela
    def draw_barra_vida(self, screen, sprite_barra_vida):
        # posicao e tamanho da barra de vida
        moldura_x = 20  # posicao horizontal da moldura
        moldura_y = 20  # posicao vertical da moldura
        
        barra_x = moldura_x + 81 # posicao horizontal para alinhar a barra
        barra_y = moldura_y + 60  # posicao vertical para alinhar a barra
        barra_largura = 82  # largura total da barra
        barra_altura = 20  # altura da barra

        # calcula a largura da barra com base na vida atual
        largura_atual = int(self.vida_atual / self.max_vida * barra_largura)

        # desenha a barra de vida (vermelha para o fundo, verde para a vida atual)
        pygame.draw.rect(screen, (255, 0, 0), (barra_x, barra_y, barra_largura, barra_altura))  # fundo vermelho
        pygame.draw.rect(screen, (0, 255, 0), (barra_x, barra_y, largura_atual, barra_altura))  # vida atual (verde)

        # desenha o sprite da moldura ao redor da barra de vida
        screen.blit(sprite_barra_vida, (moldura_x, moldura_y)) 
    
    def tomar_dano(self, dano): # def de dano do jogador
        # reduz a vida do jogador
        self.vida_atual -= dano + 10
        if self.vida_atual <= 0:
            self.vida_atual = 0  # evita valores negativos
            # ai ele morre
            
    def atacar(self, boss): # def de ataque do jogador
        # ataca o boss se estiver proximo
        alcance_ataque = 50  # distancia maxima para o ataque
        jogador_rect = pygame.Rect(self.x, self.y, SPRITE_Largura, SPRITE_Altura)
        if jogador_rect.colliderect(boss.rect.inflate(-alcance_ataque, -alcance_ataque)):
            boss.tomar_dano(10)  # causa 10 de dano ao boss
            print("Ataque realizado!")
    
    def morrer(self, tela, clock): # def de morte do jogador
        # reproduz a animacao de morte do jogador
        self.animacao_morte = True
        for frame in ANIM_Morte:
            tela.blit(mapas["torre"], (0, 0))
            tela.blit(frame, (self.x, self.y))  # desenha o frame da animacao
            pygame.display.update()
            clock.tick(6)  # controla a velocidade da animacao
        self.animacao_morte = False