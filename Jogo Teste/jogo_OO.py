# importa a biblioteca pygame
import pygame 

# configuracoes basicas do jogo
Largura, Altura = 1440, 960  # define o tamanho da tela
player_velocidade = 5  # define a velocidade do jogador
FPS = 60  # controla a velocidade da animacao

# iniciando o jogo
pygame.init()  # inicia o pygame
tela = pygame.display.set_mode((Largura, Altura))  # cria a tela do jogo
clock = pygame.time.Clock()  # controla a atualização do jogo

# carrega as imagens do mapa e do jogador
mapas = {
    "primeiro mapa": pygame.transform.scale(pygame.image.load("mapa_1.png"), (Largura, Altura)),
    "segundo mapa": pygame.transform.scale(pygame.image.load("mapa_2.png"), (Largura, Altura))
}
player_spritesheet = pygame.transform.scale(pygame.image.load("personagem.png"), (1664, 6912))

# funcao para cortar as sprites do arquivo
def get_sprites(sheet, linhas, colunas, largura, altura):
    sprites = []
    for linha in range(linhas):
        for coluna in range(colunas):
            x = coluna * largura
            y = linha * altura
            sprite = sheet.subsurface(pygame.Rect(x, y, largura, altura))  # recorta o sprite
            sprites.append(sprite)
    return sprites  

# configura a spritesheet (que eh basicamente a matriz das sprites: essa é 54x13 comecando do 0)
SPRITE_Largura, SPRITE_Altura = 128, 128 
sprites = get_sprites(player_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)  

# indices das animacoes (ex: 130-139 = andar para baixo ou 117-126 = andar para esquerda etc)
ANIM_Baixo = sprites[130:139]  
ANIM_Esquerda = sprites[117:126]  
ANIM_Direita = sprites[143:152]  
ANIM_Cima = sprites[104:113]

# classe do jogador
class Player:
    
    # inicializa o jogador na posicao (x, y)
    def __init__(self, x, y):
        self.x = x  # posicao horizontal do jogador
        self.y = y  # posicao vertical do jogador
        self.frame = 0  # controla qual frame da animação esta sendo mostrado
        self.direcao = ANIM_Baixo  # comeca parado olhando para frente
        
    # funcao para mover o jogador
    def move(self, keys):
        movendo = False  # variavel bool para saber se o jogador esta se movendo

        if keys[pygame.K_LEFT]:  # se a seta esquerda for pressionada
            self.x -= player_velocidade  # move para a esquerda
            self.direcao = ANIM_Esquerda
            movendo = True
            
        if keys[pygame.K_RIGHT]:  # se a seta direita for pressionada
            self.x += player_velocidade  # move para a direita
            self.direcao = ANIM_Direita
            movendo = True
            
        if keys[pygame.K_UP]:  # se a seta para cima for pressionada
            self.y -= player_velocidade  # move para cima
            self.direcao = ANIM_Cima
            movendo = True
            
        if keys[pygame.K_DOWN]:  # se a seta para baixo for pressionada
            self.y += player_velocidade  # move para baixo
            self.direcao = ANIM_Baixo
            movendo = True

        if movendo:  
            self.frame = (self.frame + 1) % len(self.direcao)  # muda o frame da animacao

    # funcao para desenhar o jogador na tela
    def draw(self, screen):  
        screen.blit(self.direcao[self.frame], (self.x, self.y))

# classe do jogo
class Game:
    
    def __init__(self):
        # inicia as variais do jogo
        self.tela = pygame.display.set_mode((Largura, Altura))
        pygame.display.set_caption("A Ordem dos Discretos")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.mapa_atual = "primeiro mapa"  # define o mapa atual
        # cria o jogador
        self.player = Player(Largura // 2, Altura // 2)
        
        # cria o coletavel
        self.coletavel = pygame.transform.scale(pygame.image.load("hamburger 2.0.png"), (64, 64))
        self.coletavel.set_colorkey((0, 0, 0)) # tira o fundo preto da imagem do coletavel
        self.coletou = False

    def game_loop(self):
        
        while self.running:
            self.clock.tick(FPS)  # define o FPS 
            
            # render do mapa e do jogador
            self.tela.blit(mapas[self.mapa_atual], (0, 0))  # coloca o mapa no fundo da tela
            keys = pygame.key.get_pressed()  # pega as teclas pressionadas
            self.player.move(keys)  # move o jogador
            self.player.draw(self.tela)  # desenha o jogador na tela

            # para cada evento ocorrido na tela (ou seja, uma tecla pressionada), eu verifico se a janela foi fechada 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  # se o jogador fechar a janela
                    self.running = False  # o loop é encerrado
            
            # verifica se teve colisao do jogador com o coletavel
            # aqui eu criei um retangulo para o jogador e verifiquei se ele colide com o retangulo do coletavel (gustavo me deu a ideia)
            jogador_rect = pygame.Rect(self.player.x, self.player.y, SPRITE_Largura, SPRITE_Altura)
            
            # se o jogador colidir com o coletavel e ainda nao tiver coletado, eu mudo a variavel para True
            if not self.coletou and jogador_rect.colliderect(self.coletavel.get_rect(topleft = (800, 800))): 
                self.coletou = True

            # se o jogador ainda nao coletou, eu coloco o coletavel na tela
            if not self.coletou:
                self.tela.blit(self.coletavel, (800, 800))
                
            # transicao dos mapas/fases
            if self.mapa_atual == "primeiro mapa" and self.player.y <= 0:
                self.mapa_atual = "segundo mapa"
                
                # aqui eu coloco o jogador na parte de baixo do mapa (ou seja, na parte de cima do segundo mapa)
                self.player.y = Altura - SPRITE_Altura - 20
            
            if self.mapa_atual == "segundo mapa" and self.player.y >= (Altura - SPRITE_Altura):
                self.mapa_atual = "primeiro mapa"
                
                # aqui eu coloco o jogador na parte de cima do mapa (ou seja, na parte de baixo do segundo mapa)
                self.player.y = 20

            pygame.display.update()  # atualiza a tela do jogo

        pygame.quit()  # fecha o pygame

# iniciar o jogo
game = Game()
game.game_loop()