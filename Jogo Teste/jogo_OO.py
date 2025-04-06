# importa a biblioteca pygame
import os
import pygame 

# configuracoes basicas do jogo
Largura, Altura = 1000, 800 # tamanho da tela
player_velocidade = 4 
FPS = 60

pygame.init()
tela = pygame.display.set_mode((Largura, Altura)) 
clock = pygame.time.Clock()

# carrega as imagens
mapas = {
    "primeiro mapa": pygame.transform.scale(pygame.image.load("Mapa revolution 3000.png"), (Largura, Altura)),
    "segundo mapa": pygame.transform.scale(pygame.image.load("Mapa torre final.png"), (Largura, Altura)),
    "torre": pygame.transform.scale(pygame.image.load("Mapa da torre exposta final.png"), (Largura, Altura))
}
player_spritesheet = pygame.transform.scale(pygame.image.load("personagem.png"), (832, 3456)) 
player_spritesheet2 = pygame.transform.scale(pygame.image.load("Person_Manto.png"), (832, 3456))
player_spritesheet3 = pygame.transform.scale(pygame.image.load("Person_Manto_Cajado.png"), (1536, 4224))

# funcao para carregar os sprites do spritesheet
def get_sprites(sheet, linhas, colunas, largura, altura):
    sprites = []
    for linha in range(linhas): # itera pelas linhas do spritesheet
        for coluna in range(colunas):  # itera pelas colunas do spritesheet
            x = coluna * largura # define largura e altura do sprite
            y = linha * altura
            sprite = sheet.subsurface(pygame.Rect(x, y, largura, altura)) 
            sprites.append(sprite)
    return sprites  

# carrega os sprites do jogador
SPRITE_Largura, SPRITE_Altura = 64, 64 
sprites = get_sprites(player_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)  

ANIM_Baixo = sprites[130:139]  # animacao para baixo
ANIM_Esquerda = sprites[117:126]  # animacao para esquerda
ANIM_Direita = sprites[143:152]  # animacao para direita
ANIM_Cima = sprites[104:113]  # animacao para cima

# Configuração de font para mensagens
font_alagard = pygame.font.Font('alagard.ttf', 40)

# Função para atualizar os sprites do jogador
def atualizar_sprites(player, novo_spritesheet):
    global ANIM_Baixo, ANIM_Esquerda, ANIM_Direita, ANIM_Cima 
    sprites = get_sprites(novo_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)
    ANIM_Baixo = sprites[130:139]
    ANIM_Esquerda = sprites[117:126]
    ANIM_Direita = sprites[143:152]
    ANIM_Cima = sprites[104:113]
    player.direcao = ANIM_Baixo  # Atualiza a direção atual do jogador

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

# class para o jogo
class Game: 
    def __init__(self): # inicializa o jogo
        self.tela = pygame.display.set_mode((Largura, Altura)) # tela de entrada
        pygame.display.set_caption("A Ordem dos Discretos") # nome do jogo
        self.clock = pygame.time.Clock() 
        self.running = True 
        self.mapa_atual = "primeiro mapa"
        self.player = Player(30, Altura // 2)

        # carrega os sprites dos coletaveis
        self.coletavel_img2 = pygame.transform.scale(pygame.image.load("bau fechado 2.png"), (46, 36))
        self.coletavel_img3 = pygame.transform.scale(pygame.image.load("bau aberto 2.png"), (46, 36))

        self.coletavel_img4 = pygame.transform.scale(pygame.image.load("Caveira_Com_Manto.png"), (100, 100))
        self.coletavel_img5 = pygame.transform.scale(pygame.image.load("Caveira_Sem_Manto.png"), (100, 100))

        # Coletáveis por mapa
        self.coletaveis = {
            "primeiro mapa": [
            #     {"pos": (800, 600), "coletado": False},
            #     {"pos": (200, 300), "coletado": False},
            #     {"pos": (800, 500), "coletado": False}
            ],
            "segundo mapa": [
                # {"pos": (600, 400), "coletado": False},
                {"pos": (200, 180), "coletado": False},
                {"pos": (750, 470), "coletado": False}
            ],
            "torre": [

            ]
        }

        # Variáveis para mensagens
        self.mensagem_tempo = 0
        self.mensagem_texto = ""

    # define a mensagem a ser exibida
    def mostrar_mensagem(self, texto, duracao):
        self.mensagem_texto = texto
        self.mensagem_tempo = duracao
    
    # desenha a mensagem na tela
    def desenhar_mensagem(self):
        if self.mensagem_tempo > 0:
            # Define a posição e tamanho da caixa de mensagem
            caixa_largura, caixa_altura = Largura // 2, Altura // 6
            caixa_x, caixa_y = Largura // 4, Altura // 3
            # Desenha o retângulo de fundo
            pygame.draw.rect(self.tela, (50, 50, 50), (caixa_x, caixa_y, caixa_largura, caixa_altura))
            # Renderiza o texto e centraliza dentro da caixa
            texto_surface = font_alagard.render(self.mensagem_texto, True, (255, 255, 255))
            texto_rect = texto_surface.get_rect(center=(caixa_x + caixa_largura // 2, caixa_y + caixa_altura // 2))
            self.tela.blit(texto_surface, texto_rect)
            self.mensagem_tempo -= 1

    # def para a tela inicial
    def tela_inicial(self):
        inicio_tempo = pygame.time.get_ticks()
        while pygame.time.get_ticks() - inicio_tempo < 3000: # 3 segundos
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
            self.tela.fill((0, 0, 0)) # tela preta
            texto_surface = font_alagard.render("Bem-vindo a A Ordem dos Discretos!", True, (255, 255, 255))
            texto_rect = texto_surface.get_rect(center=(Largura // 2, Altura // 2))
            self.tela.blit(texto_surface, texto_rect)
            pygame.display.update() # atualiza a tela
        return True

    def game_loop(self):
        if not self.tela_inicial():
            return

        while self.running:
            self.clock.tick(FPS)
            self.tela.blit(mapas[self.mapa_atual], (0, 0))
            keys = pygame.key.get_pressed()

            # Define as colisões do mapa atual
            if self.mapa_atual == "segundo mapa":
                colisoes = colisoes_torre_final
            if self.mapa_atual == "torre":
                colisoes = colisoes_torre_interior
            if self.mapa_atual == "primeiro mapa":
                colisoes = colisoes_mapa_inicial

            self.player.move(keys, colisoes)
            self.player.draw(self.tela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Verifica colisão com coletáveis
            jogador_rect = pygame.Rect(self.player.x, self.player.y, SPRITE_Largura, SPRITE_Altura)
            for index, coletavel in enumerate(self.coletaveis[self.mapa_atual]):
                if not coletavel["coletado"]:
                    coletavel_rect_bau = self.coletavel_img2.get_rect(topleft=coletavel["pos"])
                    coletavel_rect_esq = self.coletavel_img4.get_rect(topleft=coletavel["pos"])
                    if coletavel == self.coletaveis[self.mapa_atual][1]:
                        if jogador_rect.colliderect(coletavel_rect_bau) and self.coletaveis["segundo mapa"][0]["coletado"]:
                            coletavel["coletado"] = True
                            self.mostrar_mensagem("Item coletado!", 120)
                            
                            # Troca o spritesheet do jogador com base no coletável
                            if index == 0:  # Coletável [0]
                                atualizar_sprites(self.player, player_spritesheet2)
                            elif index == 1:  # Coletável [1]
                                atualizar_sprites(self.player, player_spritesheet3)
                    else:
                        if jogador_rect.colliderect(coletavel_rect_esq):
                            coletavel["coletado"] = True
                            self.mostrar_mensagem("Item coletado!", 120)
                            
                            # Troca o spritesheet do jogador com base no coletável
                            if index == 0:  # Coletável [0]
                                atualizar_sprites(self.player, player_spritesheet2)
                            elif index == 1:  # Coletável [1]
                                atualizar_sprites(self.player, player_spritesheet3)

            # Desenha coletáveis não coletados
            for coletavel in self.coletaveis[self.mapa_atual]:
                if coletavel == self.coletaveis[self.mapa_atual][1]:
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img2, coletavel["pos"])
                    if coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img3, coletavel["pos"])
                else:
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img4, coletavel["pos"])
                    if coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img5, coletavel["pos"])

            # Transição dos mapas
            #transição para o segundo mapa
            if self.mapa_atual == "primeiro mapa" and self.player.x >=970:
                self.mapa_atual = "segundo mapa"
                self.player.y = Altura // 2 + 35
                self.player.x = 15 
            if self.mapa_atual == "segundo mapa":
                #voltar para o primeiro mapa
                if self.player.x <= 5:
                    self.mapa_atual = "primeiro mapa"
                    self.player.y = Altura // 2 - 20
                    self.player.x = 950
                #transicão para dentro da torre    
                elif 420 < self.player.x < 460 and self.player.y <= 225:
                    self.mapa_atual = "torre"
                    self.player.x = Largura // 2 - 30
                    self.player.y = 780

            # Desenha a mensagem se houver
            self.desenhar_mensagem()

            pygame.display.update()

        pygame.quit()

#colisões prontas
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

#colisões prontas
colisoes_torre_interior = [
    pygame.Rect(0, 0, 1000, 200),  # Parede fundo
    pygame.Rect(0, 210, 60, 30),  # Parede fundo esquerda
    pygame.Rect(945, 210, 60, 30),  # Parede fundo direita
    pygame.Rect(0, 0, 3, 800),  # Parede lateral esquerda
    pygame.Rect(997, 0, 3, 800),  # Parede lateral direita
    pygame.Rect(0, 750, 20, 50),  # Parede lateral direita
    pygame.Rect(970, 750, 20, 50),  # Parede lateral direita
    pygame.Rect(30, 795, 385, 3),  # Parede inferior esquerda
    pygame.Rect(600, 795, 400, 3),  # Parede inferior direita
    pygame.Rect(0, 850, 1000, 1),  # Barreira porta
    pygame.Rect(140, 220, 30, 80),  # Estatua superior esquerda
    pygame.Rect(800, 220, 30, 80),  # Estatua superior direita
    pygame.Rect(20, 420, 60, 50),  # Estatua meio esquerda
    pygame.Rect(920, 420, 30, 50),  # Estatua meio direita
    pygame.Rect(135, 670, 30, 50),  # Estatua inferior esquerda
    pygame.Rect(825, 670, 30, 50),  # Estatua inferior direita
    pygame.Rect(490, 210, 20, 35),  # Trono
    
]

#colisoes prontas
colisoes_mapa_inicial = [
    pygame.Rect(0, 0, 1, 800),  # Parede lateral esquerda
    pygame.Rect(0, 0, 1000, 1),  # Parede superior
    pygame.Rect(0, 799, 1000, 1),  # Parede inferior
    pygame.Rect(950, 0, 100, 250),  # Parede lateral direita superior
    pygame.Rect(800, 550, 200, 200),  # Parede lateral direita inferior
    pygame.Rect(0, 0, 200, 340),  # Bloco arvores e pedras esquerda
    pygame.Rect(0, 600, 50, 200),  # Arvore inferior
    pygame.Rect(80, 550, 50, 250),  # Arvore inferior
    pygame.Rect(260, 650, 240, 150),  # Lago
    pygame.Rect(650, 680, 350, 100),  # Floresta inferior direita
    pygame.Rect(860, 30, 50, 100),  # Arvore superior direita
    pygame.Rect(700, 80, 50, 100),  # Estatua
    pygame.Rect(390, 10, 160, 130),  # Arvore cercada
    pygame.Rect(410, 230, 70, 40),  # Fonte
    pygame.Rect(575, 245, 60, 105),  # Arvore central
    pygame.Rect(200, 40, 70, 30),  # Pedra superior esquerda

]

# Iniciar o jogo
game = Game()
game.game_loop()