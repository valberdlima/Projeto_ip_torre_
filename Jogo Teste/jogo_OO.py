# importa a biblioteca pygame
import pygame 

# configuracoes basicas do jogo
Largura, Altura = 1440, 960
player_velocidade = 5
FPS = 60

pygame.init()
tela = pygame.display.set_mode((Largura, Altura))
clock = pygame.time.Clock()

# carrega as imagens
mapas = {
    "primeiro mapa": pygame.transform.scale(pygame.image.load("mapa_1.png"), (Largura, Altura)),
    "segundo mapa": pygame.transform.scale(pygame.image.load("mapa torre final.png"), (Largura, Altura))
}
player_spritesheet = pygame.transform.scale(pygame.image.load("personagem.png"), (1664, 6912))

def get_sprites(sheet, linhas, colunas, largura, altura):
    sprites = []
    for linha in range(linhas):
        for coluna in range(colunas):
            x = coluna * largura
            y = linha * altura
            sprite = sheet.subsurface(pygame.Rect(x, y, largura, altura))
            sprites.append(sprite)
    return sprites  

SPRITE_Largura, SPRITE_Altura = 128, 128 
sprites = get_sprites(player_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)  

ANIM_Baixo = sprites[130:139]  
ANIM_Esquerda = sprites[117:126]  
ANIM_Direita = sprites[143:152]  
ANIM_Cima = sprites[104:113]

# Configuração de fonte para mensagens
fonte = pygame.font.SysFont("arial", 40)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.direcao = ANIM_Baixo
        
    def move(self, keys):
        movendo = False
        if keys[pygame.K_LEFT]:
            self.x -= player_velocidade
            self.direcao = ANIM_Esquerda
            movendo = True
        if keys[pygame.K_RIGHT]:
            self.x += player_velocidade
            self.direcao = ANIM_Direita
            movendo = True
        if keys[pygame.K_UP]:
            self.y -= player_velocidade
            self.direcao = ANIM_Cima
            movendo = True
        if keys[pygame.K_DOWN]:
            self.y += player_velocidade
            self.direcao = ANIM_Baixo
            movendo = True
        if movendo:
            self.frame = (self.frame + 1) % len(self.direcao)
        
        else:
            self.frame = 0

    def draw(self, screen):
        screen.blit(self.direcao[self.frame], (self.x, self.y))

class Game:
    def __init__(self):
        self.tela = pygame.display.set_mode((Largura, Altura))
        pygame.display.set_caption("A Ordem dos Discretos")
        self.clock = pygame.time.Clock()
        self.running = True
        self.mapa_atual = "primeiro mapa"
        self.player = Player(Largura // 2, Altura // 2)

        # Carrega o coletável
        self.coletavel_img = pygame.transform.scale(pygame.image.load("hamburger 2.0.png"), (64, 64))
        self.coletavel_img.set_colorkey((0, 0, 0))

        # Coletáveis por mapa
        self.coletaveis = {
            "primeiro mapa": [
                {"pos": (800, 800), "coletado": False},
                {"pos": (200, 300), "coletado": False},
                {"pos": (1200, 500), "coletado": False}
            ],
            "segundo mapa": [
                {"pos": (600, 400), "coletado": False},
                {"pos": (1000, 700), "coletado": False}
            ]
        }

        # Variáveis para mensagens
        self.mensagem_tempo = 0
        self.mensagem_texto = ""

    def mostrar_mensagem(self, texto, duracao):
        self.mensagem_texto = texto
        self.mensagem_tempo = duracao

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

    def tela_inicial(self):
        inicio_tempo = pygame.time.get_ticks()
        while pygame.time.get_ticks() - inicio_tempo < 3000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
            self.tela.fill((0, 0, 0))
            texto_surface = fonte.render("Bem-vindo a A Ordem dos Discretos!", True, (255, 255, 255))
            texto_rect = texto_surface.get_rect(center=(Largura // 2, Altura // 2))
            self.tela.blit(texto_surface, texto_rect)
            pygame.display.update()
        return True

    def game_loop(self):
        if not self.tela_inicial():
            return

        while self.running:
            self.clock.tick(FPS)
            self.tela.blit(mapas[self.mapa_atual], (0, 0))
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.draw(self.tela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Verifica colisão com coletáveis
            jogador_rect = pygame.Rect(self.player.x, self.player.y, SPRITE_Largura, SPRITE_Altura)
            for coletavel in self.coletaveis[self.mapa_atual]:
                if not coletavel["coletado"]:
                    coletavel_rect = self.coletavel_img.get_rect(topleft=coletavel["pos"])
                    if jogador_rect.colliderect(coletavel_rect):
                        coletavel["coletado"] = True
                        self.mostrar_mensagem("Item coletado!", 120)

            # Desenha coletáveis não coletados
            for coletavel in self.coletaveis[self.mapa_atual]:
                if not coletavel["coletado"]:
                    self.tela.blit(self.coletavel_img, coletavel["pos"])

            # Transição dos mapas
            if self.mapa_atual == "primeiro mapa" and self.player.y <= 0:
                self.mapa_atual = "segundo mapa"
                self.player.y = Altura - SPRITE_Altura - 20
            if self.mapa_atual == "segundo mapa" and self.player.y >= (Altura - SPRITE_Altura):
                self.mapa_atual = "primeiro mapa"
                self.player.y = 20

            # Desenha a mensagem se houver
            self.desenhar_mensagem()

            pygame.display.update()

        pygame.quit()

# Iniciar o jogo
game = Game()
game.game_loop()