import pygame

# Iniciando o game
pygame.init()

# Criando a tela
tela = pygame.display.set_mode((1440, 960))
pygame.display.set_caption("Game Teste")

# Dicionário com os mapas
mapas = {
    "mapa inicial": pygame.transform.scale(pygame.image.load("mapa 1.png"), (1440, 960)),
    "mapa praia": pygame.transform.scale(pygame.image.load("mapa 2.png"), (1440, 960))
}

# Criando o clock do FPS
clock = pygame.time.Clock()

jogador_tamanho = 128
jogador_x = 1280 // 2 - jogador_tamanho // 2  
jogador_y = 960 // 2 - jogador_tamanho // 2 
jogador_velocidade = 5

img_sprites = pygame.transform.scale(pygame.image.load("emanoel 2.0.png"), (1664, 6912))

coletavel = pygame.transform.scale(pygame.image.load("hamburger 2.0.png"), (64, 64))
coletavel.set_colorkey((0, 0, 0))

sprites = [
    [img_sprites.subsurface((i * jogador_tamanho, 8 * jogador_tamanho, jogador_tamanho, jogador_tamanho)) for i in range(9)],
    [img_sprites.subsurface((i * jogador_tamanho, 9 * jogador_tamanho, jogador_tamanho, jogador_tamanho)) for i in range(9)],
    [img_sprites.subsurface((i * jogador_tamanho, 10 * jogador_tamanho, jogador_tamanho, jogador_tamanho)) for i in range(9)],
    [img_sprites.subsurface((i * jogador_tamanho, 11 * jogador_tamanho, jogador_tamanho, jogador_tamanho)) for i in range(9)]
]

# Variáveis do jogo
jogando = True
mapa_atual = "mapa inicial"
sprite_atual = 2
frame_atual = 0
anim_atual = 0
conta_mzr = 0
taxa = 2

coletou = False

while jogando:
    movendo = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador_x > 0:
        jogador_x -= jogador_velocidade
        sprite_atual = 1
        conta_mzr += 1
        movendo = True

    if teclas[pygame.K_RIGHT] and jogador_x < (1320):
        jogador_x += jogador_velocidade
        sprite_atual = 3
        conta_mzr += 1
        movendo = True

    if teclas[pygame.K_UP] and jogador_y > 0:
        jogador_y -= jogador_velocidade
        sprite_atual = 0
        conta_mzr += 1
        movendo = True

    if teclas[pygame.K_DOWN] and jogador_y < (960 - jogador_tamanho):
        jogador_y += jogador_velocidade
        sprite_atual = 2
        conta_mzr += 1
        movendo = True
    
    # Atualização da animação
    if movendo:
        if conta_mzr > taxa:
            conta_mzr = 0
            anim_atual = (anim_atual + 1) % len(sprites[sprite_atual])
    else:
        anim_atual = 0  # Volta para o primeiro frame quando para de se mover

    # Verificar colisão do personagem com o item
    jogador_rect = sprites[sprite_atual][anim_atual].get_rect(topleft=(jogador_x, jogador_y))  # Define o retângulo com base na posição do jogador

    if not coletou and jogador_rect.colliderect(coletavel.get_rect(topleft=(800, 800))):  # A posição do item coletável
        coletou = True
  
    # Renderização do mapa
    tela.blit(mapas[mapa_atual], (0, 0))
    tela.blit(sprites[sprite_atual][anim_atual], (jogador_x, jogador_y))

    if not coletou:
        tela.blit(coletavel, (800, 800))
    
    # Transição de mapa
    if mapa_atual == "mapa inicial" and jogador_y <= 0:
        mapa_atual = "mapa praia"
        jogador_y = 960 - jogador_tamanho - 20
    
    if mapa_atual == "mapa praia" and jogador_y >= (960 - jogador_tamanho):
        mapa_atual = "mapa inicial"
        jogador_y = 20
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
