import pygame
from config import tela, clock, FPS, Largura, Altura, fonte, colisoes_torre_final, SPRITE_Altura, SPRITE_Largura
from assets import mapas, player_spritesheet2, player_spritesheet3, atualizar_sprites
from player import Player

class Game: 
    def __init__(self): # inicializa o jogo
        self.tela = pygame.display.set_mode((Largura, Altura)) # tela de entrada
        pygame.display.set_caption("A Ordem dos Discretos") # nome do jogo
        self.clock = pygame.time.Clock() 
        self.running = True 
        self.mapa_atual = "primeiro mapa"
        self.player = Player(Largura // 2, Altura // 2)

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
            texto_surface = fonte.render(self.mensagem_texto, True, (255, 255, 255))
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
            texto_surface = fonte.render("Bem-vindo a A Ordem dos Discretos!", True, (255, 255, 255))
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
            else:
                colisoes = []  # Sem colisões no primeiro mapa

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
            if self.mapa_atual == "primeiro mapa" and self.player.y <= 0:
                self.mapa_atual = "segundo mapa"
                self.player.y = Altura // 2 + 20
                self.player.x = 15 
            if self.mapa_atual == "segundo mapa":
                #voltar para o primeiro mapa
                if self.player.x <= 5:
                    self.mapa_atual = "primeiro mapa"
                    self.player.y = 20
                #transicão para dentro da torre    
                elif 420 < self.player.x < 460 and self.player.y <= 225:
                    self.mapa_atual = "primeiro mapa"
                    self.player.x = 800
                    self.player.y = 600

            # Desenha a mensagem se houver
            self.desenhar_mensagem()

            pygame.display.update()

        pygame.quit()