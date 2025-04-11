import pygame
import pygame.mixer
from config import Largura, Altura, FPS, tela, clock, font_dialogo, font_instrucao, font_mensagem, SPRITE_Largura, SPRITE_Altura, DIALOGO_VELOCIDADE, DIALOGO_MARGEM, DIALOGO_CAIXA_X, DIALOGO_CAIXA_Y, DIALOGO_CAIXA_LARGURA_MAX, DIALOGO_CAIXA_ALTURA_MIN
from assets import mapas, player_spritesheet2, player_spritesheet3, sprite_barra_vida
from player import Player, Projectplay, atualizar_sprites, ANIM_Baixo_Ataque, ANIM_Esquerda_Ataque, ANIM_Direita_Ataque, ANIM_Cima_Ataque
from collisions import colisoes_segundo_mapa, colisoes_mapa_torre, colisoes_primeiro_mapa, colisoes_terceiro_mapa
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
        pygame.mixer.music.load("Audios\Hobbit OST 8 bits.mp3")  # Substitua pelo nome do arquivo MP3
        pygame.mixer.music.set_volume(0.05)  # Ajuste o volume (0.0 a 1.0)
        pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop

        #boss_até entrar na torre
        self.all_sprites   = pygame.sprite.Group()
        self.boss_attacks  = pygame.sprite.Group()
        self.boss          = None

        # Carrega os sprites dos coletáveis
        self.coletavel_img2 = pygame.transform.scale(pygame.image.load("Sprites\sprite_bau_fechado.png"), (46, 36))
        self.coletavel_img3 = pygame.transform.scale(pygame.image.load("Sprites\sprite_bau_aberto.png"), (46, 36))
        self.coletavel_img4 = pygame.transform.scale(pygame.image.load("Sprites\Caveira_Com_Manto.png"), (100, 100))
        self.coletavel_img5 = pygame.transform.scale(pygame.image.load("Sprites\Caveira_Sem_Manto.png"), (100, 100))
        self.coletavel_img6 = pygame.transform.scale(pygame.image.load("Sprites\Chave.png"), (30, 30))
        self.coletavel_img7 = pygame.transform.scale(pygame.image.load("Sprites\Chave_Coletada.png"), (30, 30))

        # Coletáveis por mapa
        # o "pos" define a posição do item no mapa.
        self.coletaveis = {
            "primeiro mapa": [],
            "segundo mapa": [
                {"pos": (200, 180), "coletado": False},
                {"pos": (750, 470), "coletado": False}
            ],
            "terceiro mapa": [
                {"pos": (550, 35), "coletado": False}
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
            "Devo estar louco... ou ter pego no sono estudando para a prova de matemática discreta"
        ]
        self.dialogo_caveira = ["MEU DEUS!! Kenneth Rosen"]
        self.dialogo_atual_lista = self.dialogo_textos
        self.dialogo_atual = 0
        self.dialogo_letra_contador = 0
        self.dialogo_frame_contador = 0
        self.dialogo_texto_atual = ""
        self.dialogo_caveira_ativa = False
        self.coleta_pendente = None

        # Contador geral de objetos coletados
        self.objetos_coletados = 0
        # Inicializar os contadores de cada coletável
        self.contadores_coletaveis = {
            "chave": 0,
            "cajado": 0,
            "manto": 0,
            "livro": 0 
        }
        
        # carregar a imagem da moldura dos contadores
        self.moldura_coletaveis = pygame.image.load("Sprites\moldura_coletaveis.png").convert_alpha()
        self.moldura_coletaveis = pygame.transform.scale(self.moldura_coletaveis, (300, 150))
                     
        # Carregar a imagem da caixa de diálogo
        self.caixa_dialogo_img = pygame.image.load("Sprites\Caixa_Texto_Com_Foto.png").convert_alpha()
        self.caixa_dialogo_largura, self.caixa_dialogo_altura = self.caixa_dialogo_img.get_size()
        self.caixa_dialogo_img = pygame.transform.scale(self.caixa_dialogo_img, (460, 155))  # Ajuste para o tamanho desejado
        self.caixa_dialogo_largura, self.caixa_dialogo_altura = self.caixa_dialogo_img.get_size()

        # Variáveis para diálogo do boss
        self.boss_dialogue_active = False
         
        self.player_projectiles = pygame.sprite.Group() # Grupo para os projeteis do player

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

        # Usar o tamanho fixo da imagem (sem redimensionamento)
        largura = self.caixa_dialogo_largura
        altura = self.caixa_dialogo_altura
        caixa_x = DIALOGO_CAIXA_X  # Mantém a imagem na posição original
        caixa_y = DIALOGO_CAIXA_Y

        # Desenhar a imagem da caixa de diálogo na tela (sem redimensionar)
        self.tela.blit(self.caixa_dialogo_img, (caixa_x, caixa_y))

        # Definir margens ajustadas para evitar o rosto do personagem
        margem_esquerda = 135  
        margem_superior = 55   

        # Ajustar a posição do texto principal
        texto_x = caixa_x + margem_esquerda
        texto_y = caixa_y + margem_superior

        # Atualizar o texto do diálogo (lógica de animação de letras)
        if self.dialogo_letra_contador < len(self.dialogo_atual_lista[self.dialogo_atual]):
            self.dialogo_frame_contador += 1
            if self.dialogo_frame_contador >= DIALOGO_VELOCIDADE:
                self.dialogo_letra_contador += 1
                self.dialogo_texto_atual = self.dialogo_atual_lista[self.dialogo_atual][:self.dialogo_letra_contador]
                self.dialogo_frame_contador = 0

        # Desenhar o texto sobre a caixa, com margens ajustadas
        linhas_atuais = self.quebrar_texto(self.dialogo_texto_atual, largura - margem_esquerda - DIALOGO_MARGEM)
        for i, linha in enumerate(linhas_atuais):
            texto_surface = font_dialogo.render(linha, True, (200, 200, 200))
            texto_rect = texto_surface.get_rect(topleft=(texto_x, texto_y + i * font_dialogo.get_height()))
            self.tela.blit(texto_surface, texto_rect)

        # Desenhar a instrução "[ESPAÇO]" quando o texto estiver completo
        if self.dialogo_letra_contador >= len(self.dialogo_atual_lista[self.dialogo_atual]):
            instrucao_texto = "[ESPAÇO]"
            instrucao_surface = font_instrucao.render(instrucao_texto, True, (150, 150, 150))
            # Ajustar apenas a posição vertical (descer mais)
            ajuste_vertical_espaco = 10  # Ajuste este valor para descer mais a mensagem "[ESPAÇO]"
            instrucao_rect = instrucao_surface.get_rect(
                bottomright=(caixa_x + largura - DIALOGO_MARGEM, caixa_y + altura - DIALOGO_MARGEM + ajuste_vertical_espaco)
            )
            self.tela.blit(instrucao_surface, instrucao_rect)

    def mostrar_dialogo_boss(self, texto, speaker):
        # Usar o tamanho fixo da caixa de diálogo
        largura = self.caixa_dialogo_largura
        altura = self.caixa_dialogo_altura
        caixa_x = DIALOGO_CAIXA_X
        caixa_y = DIALOGO_CAIXA_Y

        # Escolher a caixa de diálogo com base no falante
        if speaker == "boss":
            self.tela.blit(self.boss.boss_dialog_box, (caixa_x, caixa_y))
            margem_esquerda = 135  # Ajustado para evitar o rosto
        else:  # player
            self.tela.blit(self.caixa_dialogo_img, (caixa_x, caixa_y))
            margem_esquerda = 135  # Mesmo ajuste para consistência

        margem_superior = 55
        texto_x = caixa_x + margem_esquerda
        texto_y = caixa_y + margem_superior

        # Atualizar o texto do diálogo (lógica de animação de letras)
        if self.dialogo_letra_contador < len(texto):
            self.dialogo_frame_contador += 1
            if self.dialogo_frame_contador >= DIALOGO_VELOCIDADE:
                self.dialogo_letra_contador += 1
                self.dialogo_texto_atual = texto[:self.dialogo_letra_contador]
                self.dialogo_frame_contador = 0

        # Desenhar o texto sobre a caixa
        linhas_atuais = self.quebrar_texto(self.dialogo_texto_atual, largura - margem_esquerda - DIALOGO_MARGEM)
        for i, linha in enumerate(linhas_atuais):
            texto_surface = font_dialogo.render(linha, True, (200, 200, 200))
            texto_rect = texto_surface.get_rect(topleft=(texto_x, texto_y + i * font_dialogo.get_height()))
            self.tela.blit(texto_surface, texto_rect)

        # Desenhar a instrução "[ESPAÇO]" quando o texto estiver completo
        if self.dialogo_letra_contador >= len(texto):
            instrucao_texto = "[ESPAÇO]"
            instrucao_surface = font_instrucao.render(instrucao_texto, True, (150, 150, 150))
            ajuste_vertical_espaco = 10
            instrucao_rect = instrucao_surface.get_rect(
                bottomright=(caixa_x + largura - DIALOGO_MARGEM, caixa_y + altura - DIALOGO_MARGEM + ajuste_vertical_espaco)
            )
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

    def desenhar_contadores_separados(self):
        # desenha a moldura dos coletaveis e os contadores abaixo de cada icone
        margem_x = 650  # margem direita
        margem_y = 10  # margem superior
        espacamento_entre_icones = 66  # espaco horizontal entre os contadores
        contador_y_offset = 110  # espaco vertical entre a moldura e o contador

        # desenha a moldura dos coletaveis
        self.tela.blit(self.moldura_coletaveis, (margem_x, 0))

        # lista de contadores para cada coletavel
        contadores = [
            self.contadores_coletaveis["chave"],
            self.contadores_coletaveis["cajado"],
            self.contadores_coletaveis["manto"],
            self.contadores_coletaveis["livro"]
        ]

        # desenhar os contadores abaixo de cada icone
        for i, contador in enumerate(contadores):
            texto = f"{contador}"
            texto_surface = font_mensagem.render(texto, True, (255, 255, 255))
            texto_rect = texto_surface.get_rect(center=(margem_x + 52 + i * espacamento_entre_icones, margem_y + contador_y_offset))
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
        fonte_botao = pygame.font.Font('Fontes\PressStart2P-Regular.ttf', 18)

        # Carregar imagem de fundo
        fundo = pygame.image.load("Sprites\sprite_tela_inicial.png")  # Certifique-se de ter essa imagem no diretório do jogo
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
            texto_botao_rect = texto_surface.get_rect(center = (botao_x + botao_largura // 2, botao_y + botao_altura // 2))

            # Desenhar o contorno (deslocado em várias direções)
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x - 1, texto_botao_rect.y))  # Esquerda
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x + 1, texto_botao_rect.y))  # Direita
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x, texto_botao_rect.y - 1))  # Cima
            self.tela.blit(texto_surface_sombra, (texto_botao_rect.x, texto_botao_rect.y + 1))  # Baixo

            # Desenhar o texto principal
            self.tela.blit(texto_surface, texto_botao_rect)
            
            pygame.display.update()

    def tela_vitoria(self):
        # exibe a tela de vitoria com o resumo das sprites coletadas
        while True:
            pygame.time.delay(2000)  # aguarda 2 segundos antes de exibir a tela
            # desenha a tela final
            tela_final = pygame.image.load("Sprites\sprite_tela_final.png").convert_alpha()
            tela_final = pygame.transform.scale(tela_final, (Largura, Altura))
            self.tela.blit(tela_final, (0, 0))

            # resumo das sprites coletadas
            fonte_resumo = pygame.font.Font('Fontes\PressStart2P-Regular.ttf', 20)
            texto_resumo = "Resumo das Coletas:"
            resumo_surface = fonte_resumo.render(texto_resumo, True, (255, 255, 255))
            resumo_rect = resumo_surface.get_rect(center = (Largura // 2, Altura // 2))
            self.tela.blit(resumo_surface, resumo_rect)

            # exibe os contadores de cada coletavel
            margem_y = Altura // 2 + 50
            espacamento = 40
            for i, (coletavel, contador) in enumerate(self.contadores_coletaveis.items()):
                texto = f"{coletavel.capitalize()}: {contador}"
                texto_surface = fonte_resumo.render(texto, True, (255, 255, 255))
                texto_rect = texto_surface.get_rect(center = (Largura // 2, margem_y + i * espacamento))
                self.tela.blit(texto_surface, texto_rect)

            # instrucao para sair
            texto_instrucao = "Pressione [ESC] para sair"
            instrucao_surface = fonte_resumo.render(texto_instrucao, True, (200, 200, 200))
            instrucao_rect = instrucao_surface.get_rect(center=(Largura // 2, Altura - 50))
            self.tela.blit(instrucao_surface, instrucao_rect)

            pygame.display.update()

            # verifica eventos para sair
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

    def tela_game_over(self):
        # mostra a tela de Game Over com o resumo das sprites coletadas
        while True:
            self.tela.fill((0, 0, 0))  # preenche a tela com preto
            
            # ajuste o tamanho da fonte para "GAME OVER"
            fonte_game_over = pygame.font.Font('Fontes\PressStart2P-Regular.ttf', 80)  # fonte maior
        
            # texto "Game Over"
            texto_surface = fonte_game_over.render("GAME OVER", True, (225, 0, 0))
            texto_rect = texto_surface.get_rect(center = (Largura // 2, Altura // 3))
            self.tela.blit(texto_surface, texto_rect) # desenha o texto na tela

            # resumo das sprites coletadas
            fonte_resumo = pygame.font.Font('Fontes\PressStart2P-Regular.ttf', 20)
            texto_resumo = "Resumo das Coletas:"
            resumo_surface = fonte_resumo.render(texto_resumo, True, (255, 255, 255))
            resumo_rect = resumo_surface.get_rect(center = (Largura // 2, Altura // 2))
            self.tela.blit(resumo_surface, resumo_rect) # desenha o resumo na tela

            # exibi os contadores de cada coletavel
            margem_y = Altura // 2 + 50
            espacamento = 40
            for i, (coletavel, contador) in enumerate(self.contadores_coletaveis.items()):
                texto = f"{coletavel.capitalize()}: {contador}"
                texto_surface = fonte_resumo.render(texto, True, (255, 255, 255))
                texto_rect = texto_surface.get_rect(center=(Largura // 2, margem_y + i * espacamento))
                self.tela.blit(texto_surface, texto_rect)

            # instrucao para sair
            texto_instrucao = "Pressione [ESC] para sair"
            instrucao_surface = fonte_resumo.render(texto_instrucao, True, (200, 200, 200))
            instrucao_rect = instrucao_surface.get_rect(center=(Largura // 2, Altura - 50))
            self.tela.blit(instrucao_surface, instrucao_rect)

            pygame.display.update()

            # verifica eventos para sair
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
                
    def game_loop(self):
        if not self.tela_inicial():
            return

        while self.running:
            
            self.clock.tick(FPS)
            self.tela.blit(mapas[self.mapa_atual], (0, 0))
            keys = pygame.key.get_pressed()

            if self.mapa_atual == "torre" and self.boss:
                # Verifica se o diálogo está ativo
                if not self.boss.dialogue_complete and not self.boss_dialogue_active:
                    self.boss_dialogue_active = True
                    self.dialogo_letra_contador = 0
                    self.dialogo_texto_atual = ""
                    self.dialogo_frame_contador = 0

                  # Atualiza animações do boss e projéteis apenas após o diálogo
                if self.boss.dialogue_complete:
                    self.all_sprites.update()
                    self.all_sprites.draw(self.tela)
                    self.boss.draw_health_bar(self.tela)  # Desenha a barra de vida do boss

                    # Checa colisão projétil ↔ jogador
                    jogador_rect = pygame.Rect(
                        self.player.x, self.player.y,
                        SPRITE_Largura, SPRITE_Altura
                    )
                    for gust in self.boss_attacks:  # Percorrer os projéteis do boss
                        if gust.rect.colliderect(jogador_rect):  # Verifica colisão com o jogador
                            self.player.tomar_dano(10)  # Reduz a vida do jogador em 10
                            self.mostrar_mensagem("HAHA! Você morrerá", 60)  # Exibe uma mensagem
                            gust.kill()  # Remove o projétil após a colisão
                else:
                    # Desenha o boss parado durante o diálogo
                    self.tela.blit(self.boss.image, self.boss.rect)

            if self.mapa_atual == "primeiro mapa":
                colisoes = colisoes_primeiro_mapa
            elif self.mapa_atual == "segundo mapa":
                colisoes = colisoes_segundo_mapa
            elif self.mapa_atual == "terceiro mapa":
                colisoes = colisoes_terceiro_mapa
            else:
                colisoes = colisoes_mapa_torre

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        if self.dialogo_ativa:
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
                                            self.contadores_coletaveis["manto"] += 1  # Incrementa o contador do manto
                                            self.objetos_coletados += 1
                                            self.coleta_pendente = None
                                            
                                        self.dialogo_caveira_ativa = False
                                        self.dialogo_atual_lista = self.dialogo_textos

                                    elif self.mapa_atual == "terceiro mapa" and self.coleta_pendente is not None:
                                        coletavel = self.coletaveis["terceiro mapa"][self.coleta_pendente]
                                        coletavel["coletado"] = True
                                        self.mostrar_mensagem("Você encontrou a chave", 120)
                                        self.contadores_coletaveis["chave"] += 1  # se estiver usando um contador específico
                                        self.objetos_coletados += 1
                                        self.coleta_pendente = None

                                else:
                                    self.dialogo_letra_contador = 0
                                    self.dialogo_texto_atual = ""
                                    self.dialogo_frame_contador = 0

                        elif self.boss_dialogue_active and self.boss and not self.boss.dialogue_complete:
                            if self.dialogo_letra_contador < len(self.boss.dialogues[self.boss.dialogue_index]):
                                self.dialogo_letra_contador = len(self.boss.dialogues[self.boss.dialogue_index])
                                self.dialogo_texto_atual = self.boss.dialogues[self.boss.dialogue_index]
                            else:
                                self.boss.next_dialogue()
                                self.dialogo_letra_contador = 0
                                self.dialogo_texto_atual = ""
                                self.dialogo_frame_contador = 0
                                if self.boss.dialogue_complete:
                                    self.boss_dialogue_active = False
                                    
                    # adicionando um elif pra o ataque
                    elif event.key == pygame.K_a:  # tecla "A" para atacar
                        if self.mapa_atual == "torre" and self.boss and self.player.tempo_ataque == 0:
                            # cria o projetil com base na direcao do jogador
                            projetil = Projectplay(
                                self.player.x + SPRITE_Largura // 2,
                                self.player.y + SPRITE_Altura // 2,
                                self.player.direcao  # passa a direcao diretamente
                            )
                            self.player_projectiles.add(projetil) # adiciona o projetil ao grupo
                            # reinicia o contador de ataque do jogador
                            self.player.tempo_ataque = 10
                            
                                    
            # atualiza e desenha os projeteis do jogador
            self.player_projectiles.update()
            self.player_projectiles.draw(self.tela)

            # verifica colisao dos projeteis com o boss
            for projetil in self.player_projectiles:
                if self.boss and projetil.rect.colliderect(self.boss.rect):
                    self.boss.tomar_dano_boss(10)  # causa 10 de dano ao boss
                    projetil.kill()  # remove o projetil dps da colisao

            # desenha o jogador e a barra de vida
            self.player.draw(self.tela)
            self.player.draw_barra_vida(self.tela, sprite_barra_vida)
            
            if not self.dialogo_ativa:
                self.player.move(keys, colisoes, self.objetos_coletados)

            jogador_rect = pygame.Rect(self.player.x, self.player.y, SPRITE_Largura, SPRITE_Altura)

            for index, coletavel in enumerate(self.coletaveis[self.mapa_atual]):

                if not coletavel["coletado"]:
                    coletavel_rect_bau = self.coletavel_img2.get_rect(topleft=coletavel["pos"])
                    coletavel_rect_esq = self.coletavel_img4.get_rect(topleft=coletavel["pos"])
                    coletavel_rect_key = self.coletavel_img6.get_rect(topleft=coletavel["pos"])

                    # Lógica de interação com coletável no segundo mapa
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

                    # Lógica de interação com coletável no terceiro mapa
                    if index == 0 and self.mapa_atual == "terceiro mapa":
                        if jogador_rect.colliderect(coletavel_rect_key):
                            coletavel["coletado"] = True
                            self.mostrar_mensagem("Você encontrou a chave", 120)
                            self.contadores_coletaveis["chave"] += 1
                            self.objetos_coletados += 1

                    if (self.mapa_atual == "segundo mapa" and index == 1 and len(self.coletaveis[self.mapa_atual]) > 1 and self.coletaveis["segundo mapa"][0]["coletado"] and self.contadores_coletaveis.get("chave", 0) > 0):
                        if jogador_rect.colliderect(coletavel_rect_bau):
                            coletavel["coletado"] = True
                            self.mostrar_mensagem("Cajado da Vacuidade coletado!", 120)
                            atualizar_sprites(self.player, player_spritesheet3)
                            self.contadores_coletaveis["cajado"] += 1  # Incrementa o contador do cajado
                            self.objetos_coletados += 1
                    
            for index, coletavel in enumerate(self.coletaveis[self.mapa_atual]):
                if index == 1 and self.mapa_atual == "segundo mapa":
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img2, coletavel["pos"])
                    else:
                        self.tela.blit(self.coletavel_img3, coletavel["pos"])

                elif self.mapa_atual == "terceiro mapa":
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img6, coletavel["pos"])
                    else:
                        self.tela.blit(self.coletavel_img7, coletavel["pos"])

                else:
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img4, coletavel["pos"])
                    else:
                        self.tela.blit(self.coletavel_img5, coletavel["pos"])

            #Bloco de manipulação de mapas
            if self.mapa_atual == "primeiro mapa":
                if self.player.x >= 970:
                    self.mapa_atual = "segundo mapa"
                    self.player.y = Altura // 2 + 35
                    self.player.x = 15

                elif self.player.y == 0:
                    self.mapa_atual = "terceiro mapa"
                    self.player.y = 700
                    self.player.x = 480
                
            elif self.mapa_atual == "segundo mapa":
                if self.player.x <= 5:
                    self.mapa_atual = "primeiro mapa"
                    self.player.y = Altura // 2 - 20
                    self.player.x = 950
                    
                elif 420 < self.player.x < 460 and self.player.y <= 225:
                    self.mapa_atual = "torre"
                    self.player.x = Largura // 2 - 30
                    self.player.y = 780
                    
                    pygame.mixer.music.load("Audios\OST BOSS FIGHT.mp3")
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

                    pygame.mixer.music.load("Audios\Hobbit OST 8 bits.mp3")
                    pygame.mixer.music.set_volume(0.05)
                    pygame.mixer.music.play(-1)

                    # destroi o boss e limpa os projéteis
                    if self.boss:
                        self.boss.kill()
                        self.boss_attacks.empty()
                        self.boss = None

            # verifica se o jogador morreu
            if self.player.vida_atual <= 0: 
                self.player.morrer(self.tela, self.clock)  # animacao de morte
                pygame.time.delay(1000)  # aguarda 1 segundos
                self.tela_game_over()  # exibe a tela de Game Over
                return  # sai do loop principal
            
            # chamando as defs
            self.desenhar_mensagem()
            if self.boss_dialogue_active and self.boss and not self.boss.dialogue_complete:
                self.mostrar_dialogo_boss(self.boss.dialogues[self.boss.dialogue_index], self.boss.dialogue_speakers[self.boss.dialogue_index])
            self.desenhar_dialogo()
            self.desenhar_contadores_separados()  # desenha a moldura e os contadores
            pygame.display.update()
            
        # finaliza o mixer e o pygame   
        pygame.mixer.music.stop()
        pygame.quit()