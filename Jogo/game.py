import pygame
import pygame.mixer
from config import Largura, Altura, FPS, tela, clock, font_dialogo, font_instrucao, font_mensagem, SPRITE_Largura, SPRITE_Altura, DIALOGO_VELOCIDADE, DIALOGO_MARGEM, DIALOGO_CAIXA_X, DIALOGO_CAIXA_Y, DIALOGO_CAIXA_LARGURA_MAX, DIALOGO_CAIXA_ALTURA_MIN
from assets import mapas, player_spritesheet2, player_spritesheet3, sprite_barra_vida
from player import Player, atualizar_sprites
from collisions import colisoes_segundo_mapa, colisoes_mapa_torre, colisoes_primeiro_mapa
from Boss import Boss, WindGust

class Game:
    def __init__(self):
        self.tela = tela
        pygame.display.set_caption("Elinaldo e a Torre Discreta")
        self.clock = clock
        self.running = True
        self.mapa_atual = "primeiro mapa"
        self.player = Player(30, Altura // 2)

        # Inicializar o mixer de som
        pygame.mixer.init()
        # Carregar e tocar a música em loop
        pygame.mixer.music.load("Hobbit OST 8 bits.mp3")  # Substitua pelo nome do arquivo MP3
        pygame.mixer.music.set_volume(0.05)  # Ajuste o volume (0.0 a 1.0)
        pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop

        ##boss_até entrar na torre
        self.all_sprites   = pygame.sprite.Group()
        self.boss_attacks  = pygame.sprite.Group()
        self.boss          = None

        # Carrega os sprites dos coletáveis
        self.coletavel_img2 = pygame.transform.scale(pygame.image.load("bau_fechado.png"), (46, 36))
        self.coletavel_img3 = pygame.transform.scale(pygame.image.load("bau_aberto.png"), (46, 36))
        self.coletavel_img4 = pygame.transform.scale(pygame.image.load("Caveira_Com_Manto.png"), (100, 100))
        self.coletavel_img5 = pygame.transform.scale(pygame.image.load("Caveira_Sem_Manto.png"), (100, 100))

        # Coletáveis por mapa
        self.coletaveis = {
            "primeiro mapa": [],
            "segundo mapa": [
                {"pos": (200, 180), "coletado": False},
                {"pos": (750, 470), "coletado": False}
            ],
            "torre": []
        }

        # Variáveis para mensagens normais
        self.mensagem_tempo = 0
        self.mensagem_texto = ""

        # Variáveis para diálogos
        self.dialogo_ativa = True
        self.dialogo_textos = [
            "Oxe… Que lugar é esse? Como vim parar aqui?",
            "….",
            "Devo estar enlouquecendo… ou pego no sono\nestudando para a prova de matemática discreta"
        ]
        self.dialogo_caveira = ["MEU DEUS!! Kenneth Rosen"]
        self.dialogo_atual_lista = self.dialogo_textos
        self.dialogo_atual = 0
        self.dialogo_letra_contador = 0
        self.dialogo_frame_contador = 0
        self.dialogo_texto_atual = ""
        self.dialogo_caveira_ativa = False
        self.coleta_pendente = None

        # Contador de objetos coletados
        self.objetos_coletados = 0

    def quebrar_texto(self, texto, largura_max):
        """Divide o texto em linhas para caber na largura máxima."""
        palavras = texto.replace('\n', ' \n ').split(' ')
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            if palavra == '\n':
                linhas.append(linha_atual.strip())
                linha_atual = ""
                continue
            teste_linha = (linha_atual + " " + palavra).strip()
            largura_texto = font_dialogo.render(teste_linha, True, (200, 200, 200)).get_width()
            if largura_texto <= largura_max:
                linha_atual = teste_linha
            else:
                if linha_atual:
                    linhas.append(linha_atual.strip())
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual.strip())
        return linhas

    def calcular_tamanho_caixa(self, texto):
        """Calcula o tamanho da caixa com base no texto com quebras de linha."""
        largura_max = DIALOGO_CAIXA_LARGURA_MAX - 2 * DIALOGO_MARGEM
        linhas = self.quebrar_texto(texto, largura_max)
        max_largura = 0
        for linha in linhas:
            texto_surface = font_dialogo.render(linha, True, (200, 200, 200))
            max_largura = max(max_largura, texto_surface.get_width())
        largura = min(max_largura + 2 * DIALOGO_MARGEM, DIALOGO_CAIXA_LARGURA_MAX)
        altura = max(len(linhas) * font_dialogo.get_height() + 2 * DIALOGO_MARGEM, DIALOGO_CAIXA_ALTURA_MIN)
        return largura, altura, linhas

    def desenhar_dialogo(self):
        if not self.dialogo_ativa:
            return

        largura, altura, linhas = self.calcular_tamanho_caixa(self.dialogo_atual_lista[self.dialogo_atual])
        caixa_x, caixa_y = DIALOGO_CAIXA_X, DIALOGO_CAIXA_Y - (altura - DIALOGO_CAIXA_ALTURA_MIN)

        pygame.draw.rect(self.tela, (10, 10, 10), (caixa_x + 5, caixa_y + 5, largura, altura), border_radius=10)
        surface_caixa = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(surface_caixa, (30, 30, 30, 220), (0, 0, largura, altura), border_radius=10)
        pygame.draw.rect(surface_caixa, (100, 100, 100), (0, 0, largura, altura), 3, border_radius=10)
        self.tela.blit(surface_caixa, (caixa_x, caixa_y))

        if self.dialogo_letra_contador < len(self.dialogo_atual_lista[self.dialogo_atual]):
            self.dialogo_frame_contador += 1
            if self.dialogo_frame_contador >= DIALOGO_VELOCIDADE:
                self.dialogo_letra_contador += 1
                self.dialogo_texto_atual = self.dialogo_atual_lista[self.dialogo_atual][:self.dialogo_letra_contador]
                self.dialogo_frame_contador = 0

        linhas_atuais = self.quebrar_texto(self.dialogo_texto_atual, DIALOGO_CAIXA_LARGURA_MAX - 2 * DIALOGO_MARGEM)
        for i, linha in enumerate(linhas_atuais):
            texto_surface = font_dialogo.render(linha, True, (200, 200, 200))
            texto_rect = texto_surface.get_rect(topleft=(caixa_x + DIALOGO_MARGEM, caixa_y + DIALOGO_MARGEM + i * font_dialogo.get_height()))
            self.tela.blit(texto_surface, texto_rect)

        if self.dialogo_letra_contador >= len(self.dialogo_atual_lista[self.dialogo_atual]):
            instrucao_texto = "[ESPAÇO]"
            instrucao_surface = font_instrucao.render(instrucao_texto, True, (150, 150, 150))
            instrucao_rect = instrucao_surface.get_rect(bottomright=(caixa_x + largura - DIALOGO_MARGEM, caixa_y + altura - DIALOGO_MARGEM))
            self.tela.blit(instrucao_surface, instrucao_rect)

    def mostrar_mensagem(self, texto, duracao):
        self.mensagem_texto = texto
        self.mensagem_tempo = duracao

    def desenhar_mensagem(self):
        if self.mensagem_tempo > 0:
            largura = Largura // 1.5
            altura = Altura // 5
            caixa_x, caixa_y = (Largura - largura) // 2, Altura // 3

            pygame.draw.rect(self.tela, (20, 20, 20), (caixa_x + 5, caixa_y + 5, largura, altura), border_radius=15)
            surface_caixa = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(surface_caixa, (60, 60, 60, 230), (0, 0, largura, altura), border_radius=15)
            pygame.draw.rect(surface_caixa, (200, 180, 100), (0, 0, largura, altura), 3, border_radius=15)
            self.tela.blit(surface_caixa, (caixa_x, caixa_y))

            texto_surface_sombra = font_mensagem.render(self.mensagem_texto, True, (40, 40, 40))
            texto_surface = font_mensagem.render(self.mensagem_texto, True, (255, 215, 0))
            texto_rect = texto_surface.get_rect(center=(caixa_x + largura // 2, caixa_y + altura // 2))
            self.tela.blit(texto_surface_sombra, (texto_rect.x + 2, texto_rect.y + 2))
            self.tela.blit(texto_surface, texto_rect)
            
            self.mensagem_tempo -= 1

    def desenhar_contador(self):
        """Desenha o contador de objetos coletados no canto superior direito."""
        texto = f"Objetos coletados: {self.objetos_coletados}"
        texto_surface = font_mensagem.render(texto, True, (255, 255, 255))
        texto_rect = texto_surface.get_rect(topright=(Largura - 10, 10))
        self.tela.blit(texto_surface, texto_rect)

    def transicao(self, duracao, tipo="fade-in"):
        """Efeito de transição suave (fade-in ou fade-out)."""
        overlay = pygame.Surface((Largura, Altura))
        overlay.fill((0, 0, 0))

        for alpha in range(0, 255, int(255 / (FPS * duracao))):
            if tipo == "fade-in":
                overlay.set_alpha(255 - alpha)
            elif tipo == "fade-out":
                overlay.set_alpha(alpha)

            self.tela.blit(overlay, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)    

    def tela_inicial(self):
        """Exibe a tela inicial com um botão 'Play'."""
        #fonte_tela_inicial = pygame.font.Font('PressStart2P-Regular.ttf', 40)
        fonte_botao = pygame.font.Font('PressStart2P-Regular.ttf', 18)

        # Carregar imagem de fundo
        fundo = pygame.image.load("Tela inicial do game.png")  # Certifique-se de ter essa imagem no diretório do jogo
        fundo = pygame.transform.scale(fundo, (Largura, Altura))

        # Configuração do botão "Play"
        botao_largura, botao_altura = 250, 75
        botao_x = (Largura - botao_largura) // 2
        botao_y = Altura // 2 - 100
        cor_botao = (19, 37, 58)
        cor_botao_hover = (14, 27, 48)
        cor_borda = (74, 77, 106)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique esquerdo
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if botao_x <= mouse_x <= botao_x + botao_largura and botao_y <= mouse_y <= botao_y + botao_altura:
                            self.transicao(1, tipo="fade-out")  # Adiciona transição ao sair da tela inicial
                            return True  # Inicia o jogo

            # Desenhar fundo
            self.tela.blit(fundo, (0, 0))

            # Desenhar botão "Play"
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if botao_x <= mouse_x <= botao_x + botao_largura and botao_y <= mouse_y <= botao_y + botao_altura:
                pygame.draw.rect(self.tela, cor_botao_hover, (botao_x, botao_y, botao_largura, botao_altura), border_radius=10)
            else:
                pygame.draw.rect(self.tela, cor_botao, (botao_x, botao_y, botao_largura, botao_altura), border_radius=10)

            # Desenhar borda do botão
            pygame.draw.rect(self.tela, cor_borda, (botao_x, botao_y, botao_largura, botao_altura), width=3, border_radius=10)

            # Texto do botão com contorno
            texto_botao = "Iniciar Jogo"
            texto_surface = fonte_botao.render(texto_botao, True, (219, 147, 51))  # Cor principal
            texto_surface_sombra = fonte_botao.render(texto_botao, True, (0, 0, 0))  # Cor do contorno
            texto_botao_rect = texto_surface.get_rect(center=(botao_x + botao_largura // 2, botao_y + botao_altura // 2))

            # Desenhar o contorno (deslocado em várias direções)
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x - 1, texto_botao_rect.y))  # Esquerda
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x + 1, texto_botao_rect.y))  # Direita
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x, texto_botao_rect.y - 1))  # Cima
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x, texto_botao_rect.y + 1))  # Baixo

            # Desenhar o texto principal
            self.tela.blit(texto_surface, texto_botao_rect)
            
            pygame.display.update()

    def game_loop(self):
        if not self.tela_inicial():
            return

        while self.running:
            
            self.clock.tick(FPS)
            self.tela.blit(mapas[self.mapa_atual], (0, 0))
            keys = pygame.key.get_pressed()

            if self.mapa_atual == "torre" and self.boss:
                # 1) atualiza animações do boss e projéteis
                self.all_sprites.update()
                
                # 2) desenha boss e projéteis
                self.all_sprites.draw(self.tela)
                
                # 3) desenha barra de vida
                self.boss.draw_health_bar(self.tela)
                
                # 4) checa colisão projétil ↔ jogador
                jogador_rect = pygame.Rect(
                    self.player.x, self.player.y,
                    SPRITE_Largura, SPRITE_Altura
                )
                for gust in self.boss_attacks:
                    if gust.rect.colliderect(jogador_rect):
                        self.mostrar_mensagem("HAHA! Você morrerá!", 60)
                        gust.kill()

            if self.mapa_atual == "segundo mapa":
                colisoes = colisoes_segundo_mapa
            elif self.mapa_atual == "torre":
                colisoes = colisoes_mapa_torre
            else:
                colisoes = colisoes_primeiro_mapa

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and self.dialogo_ativa:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        if self.dialogo_letra_contador < len(self.dialogo_atual_lista[self.dialogo_atual]):
                            self.dialogo_letra_contador = len(self.dialogo_atual_lista[self.dialogo_atual])
                            self.dialogo_texto_atual = self.dialogo_atual_lista[self.dialogo_atual]
                        else:
                            self.dialogo_atual += 1
                            if self.dialogo_atual >= len(self.dialogo_atual_lista):
                                self.dialogo_ativa = False
                                if self.dialogo_caveira_ativa:
                                    if self.coleta_pendente is not None:
                                        coletavel = self.coletaveis["segundo mapa"][self.coleta_pendente]
                                        coletavel["coletado"] = True
                                        self.mostrar_mensagem("Manto da Sabedoria coletado!", 120)
                                        atualizar_sprites(self.player, player_spritesheet2)
                                        self.objetos_coletados += 1  # Incrementa o contador
                                        self.coleta_pendente = None
                                    self.dialogo_caveira_ativa = False
                                    self.dialogo_atual_lista = self.dialogo_textos
                            else:
                                self.dialogo_letra_contador = 0
                                self.dialogo_texto_atual = ""
                                self.dialogo_frame_contador = 0

            if not self.dialogo_ativa:
                self.player.move(keys, colisoes, self.objetos_coletados)

            # desenha o jogador e a barra de vida
            self.player.draw(self.tela)
            self.player.draw_barra_vida(self.tela, sprite_barra_vida)

            jogador_rect = pygame.Rect(self.player.x, self.player.y, SPRITE_Largura, SPRITE_Altura)
            for index, coletavel in enumerate(self.coletaveis[self.mapa_atual]):
                if not coletavel["coletado"]:
                    coletavel_rect_bau = self.coletavel_img2.get_rect(topleft=coletavel["pos"])
                    coletavel_rect_esq = self.coletavel_img4.get_rect(topleft=coletavel["pos"])

                    if index == 0 and self.mapa_atual == "segundo mapa" and not self.dialogo_caveira_ativa and not self.dialogo_ativa:
                        proximidade_rect = coletavel_rect_esq.inflate(100, 100)
                        if jogador_rect.colliderect(proximidade_rect):
                            self.dialogo_ativa = True
                            self.dialogo_caveira_ativa = True
                            self.dialogo_atual_lista = self.dialogo_caveira
                            self.dialogo_atual = 0
                            self.dialogo_letra_contador = 0
                            self.dialogo_texto_atual = ""
                            self.dialogo_frame_contador = 0
                            self.coleta_pendente = index

                    if coletavel == self.coletaveis[self.mapa_atual][1]:
                        if jogador_rect.colliderect(coletavel_rect_bau) and self.coletaveis["segundo mapa"][0]["coletado"]:
                            coletavel["coletado"] = True
                            self.mostrar_mensagem("Cajado da Vacuidade coletado!", 120)
                            atualizar_sprites(self.player, player_spritesheet3)
                            self.objetos_coletados += 1  # Incrementa o contador

            for coletavel in self.coletaveis[self.mapa_atual]:
                if coletavel == self.coletaveis[self.mapa_atual][1]:
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img2, coletavel["pos"])
                    else:
                        self.tela.blit(self.coletavel_img3, coletavel["pos"])
                else:
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img4, coletavel["pos"])
                    else:
                        self.tela.blit(self.coletavel_img5, coletavel["pos"])

            if self.mapa_atual == "primeiro mapa" and self.player.x >= 970:
                self.mapa_atual = "segundo mapa"
                self.player.y = Altura // 2 + 35
                self.player.x = 15
            elif self.mapa_atual == "segundo mapa":
                if self.player.x <= 5:
                    self.mapa_atual = "primeiro mapa"
                    self.player.y = Altura // 2 - 20
                    self.player.x = 950
                elif 420 < self.player.x < 460 and self.player.y <= 225:
                    self.mapa_atual = "torre"
                    self.player.x = Largura // 2 - 30
                    self.player.y = 780
                    
                    pygame.mixer.music.load("OST BOSS FIGHT.mp3")
                    pygame.mixer.music.set_volume(0.05)
                    pygame.mixer.music.play(-1)
                    
                    # instancia o boss só uma vez
                    if self.boss is None:
                        self.boss = Boss(
                            x=Largura//2, y=230,
                            all_sprites_group=self.all_sprites,
                            attack_group=self.boss_attacks,
                            game=self
                        )
                    self.all_sprites.add(self.boss)    
            elif self.mapa_atual == "torre":
                if 415 < self.player.x < 600 and self.player.y >= 790:
                    self.mapa_atual = "segundo mapa"
                    self.player.x = 440
                    self.player.y = 225

                    # destroi o boss e limpa os projéteis
                    if self.boss:
                        self.boss.kill()
                        self.boss_attacks.empty()
                        self.boss = None

            self.desenhar_mensagem()
            self.desenhar_dialogo()
            self.desenhar_contador()  # Desenha o contador em todas as atualizações
            pygame.display.update()
            
            
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()