#instala o pygame com pip install pygame ou py -m pip install pygame

#importa o pygame
import pygame
pygame.mixer.quit()

#inicia o pygame
pygame.init()
pygame.mixer.init()

#musica de fundo
pygame.mixer.music.set_volume(0.1)
musica = pygame.mixer.music.load("H:\Projeto IP\Projeto_ip_torre_-1\Jogo Teste\musica_fundo.mp3")
pygame.mixer.music.play(-1)


#tem que configurar a tela 
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo teste')

# Carregar imagem de fundo
background = pygame.image.load("Jogo Teste/mapa teste.jpg")  
background = pygame.transform.scale(background, (LARGURA, ALTURA))

#cores (rgb)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

#config do boneco
jogador_tamanho = 30
jogador_x = LARGURA // 2 #posição inicial dele no eixo x
jogador_y = ALTURA // 2 # eixo y
jogador_velocidade = 5

#rodar o jogo
jogando = True

while jogando:
    pygame.time.delay(30) #controla o fps

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
    
    #codando a movimentação
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jogador_x -= jogador_velocidade #se ele apertar a setinha p esquerda a posição dele no eixo x volta a velocidade dele

    if teclas[pygame.K_RIGHT]:
        jogador_x += jogador_velocidade #se ele apertar a setinha p direita a posição dele no eixo x vai aumentar 

    if teclas[pygame.K_UP]:
        jogador_y -= jogador_velocidade # mesma coisa so q pro eixo y

    if teclas[pygame.K_DOWN]:
        jogador_y += jogador_velocidade 

    #prenchendo a tela
    tela.blit(background, (0, 0))

    #criando um boneco azul
    pygame.draw.rect(tela, AZUL, (jogador_x, jogador_y, jogador_tamanho, jogador_tamanho))

    #atualizar a tela
    pygame.display.update()

#encerrar o game
pygame.quit()