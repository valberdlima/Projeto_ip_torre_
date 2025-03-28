import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Teste")

# Cores rgb
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Relógio para controlar o FPS
clock = pygame.time.Clock()
FPS = 60

# Classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA // 2, ALTURA // 2)
        self.velocidade = 5
        self.pontos = 0
    
    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidade
        
        # Mantém o jogador dentro da tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))

# Classe do Item para coletar
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.rect.y = random.randint(0, ALTURA - self.rect.height)

# Cria grupos de sprites
todos_sprites = pygame.sprite.Group()
itens = pygame.sprite.Group()

# Cria o jogador
jogador = Jogador()
todos_sprites.add(jogador)

# Cria alguns itens
for i in range(10):
    item = Item()
    todos_sprites.add(item)
    itens.add(item)

# Fonte para o texto
fonte = pygame.font.SysFont(None, 36)

# Loop principal do jogo
rodando = True
while rodando:
    # Mantém o loop rodando na velocidade correta
    clock.tick(FPS)
    
    # Processa os eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    # Atualiza
    todos_sprites.update()
    
    # Verifica colisões entre jogador e itens
    itens_coletados = pygame.sprite.spritecollide(jogador, itens, True)
    for item in itens_coletados:
        jogador.pontos += 1
        # Cria um novo item
        novo_item = Item()
        todos_sprites.add(novo_item)
        itens.add(novo_item)
    
    # Renderiza
    tela.fill(PRETO)
    todos_sprites.draw(tela)
    
    # Mostra a pontuação
    texto_pontos = fonte.render(f"Pontos: {jogador.pontos}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))
    
    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
sys.exit()