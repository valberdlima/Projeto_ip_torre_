import pygame
from assets import get_sprites, BOSS_WIND_SPRITESHEET
from config import SPRITE_Largura, SPRITE_Altura, FPS, Largura, Altura
import random

boss_spritesheet = pygame.transform.scale(pygame.image.load("boss spritesheet.png"), (832, 3456))

# --- Primeiro, defina as animações do boss ---
sprites = get_sprites(boss_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)

ANIM_BOSS_IDLE = sprites[26:33]
ANIM_BOSS_ATTACK = sprites[182:188]  
ANIM_BOSS_MORTE = sprites[260:266] 

# BOSS Classe do projétil de vento ---
class WindGust(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        # Carrega e redimensiona a imagem do projétil
        original_image = pygame.image.load("boss projetil.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (72, 72))  # Ajuste o tamanho aqui
        self.rect = self.image.get_rect(center=(x, y))

        # Calcula a direção para o alvo (jogador)
        dx = target_x - x
        dy = target_y - y
        distance = max((dx**2 + dy**2) ** 0.5, 0.1)  # evita divisão por zero

        self.speed = 6
        self.velocity_x = self.speed * dx / distance
        self.velocity_y = self.speed * dy / distance

    def update(self):
        # Movimento contínuo do projétil
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Mata o projétil se sair da tela
        if (self.rect.right < 0 or self.rect.left > Largura or 
            self.rect.bottom < 0 or self.rect.top > Altura):
            self.kill()


# BOSS Classe do Boss ---
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites_group, attack_group, game):
        super().__init__()
        # Redimensiona as animações do boss
        self.idle_anim = [pygame.transform.scale(frame, (96, 96)) for frame in ANIM_BOSS_IDLE]
        self.attack_anim = [pygame.transform.scale(frame, (96, 96)) for frame in ANIM_BOSS_ATTACK]
        self.death_anim = [pygame.transform.scale(frame, (96, 96)) for frame in ANIM_BOSS_MORTE]
        self.frame = 0
        self.anim_counter = 0
        self.state = "dialogue"  # Estado inicial agora é "dialogue"
        self.dialogo_mostrado = False  # Controle do diálogo inicial
        self.attack_timer = 0
        self.dialogue_index = 0  # Índice do diálogo atual
        self.dialogue_complete = False  # Marca quando o diálogo termina

        # Movimento
        self.speed = 2
        self.move_timer = 0
        self.move_direction = random.choice(["left", "right"])

        # Perseguição e retorno à posição original
        self.tempo_batalha = 0  # Tempo total da luta em segundos
        self.perseguindo = False  # Controle do estado de perseguição
        self.tempo_perseguindo = 0  # Temporizador da perseguição
        self.pos_inicial = (x, y)  # Posição original do boss

        self.tempo_ataque_especial = 0  # Controla quando soltar o ataque especial


        # Lista de diálogos
        self.dialogues = [
            "Elinaldo, o que faz aqui?",
            "Não sei",
            "Então vou acabar com você! Prepare-se"
        ]
        self.dialogue_speakers = ["boss", "player", "boss"]  # Quem fala cada linha

        self.image = self.idle_anim[self.frame]
        self.rect = self.image.get_rect(center=(x, y))

        self.health = 200
        self.all_sprites = all_sprites_group
        self.attack_group = attack_group
        self.game = game  # Referência ao jogo para acessar métodos como `mostrar_mensagem`

        # Carregar a imagem da caixa de diálogo do boss
        self.boss_dialog_box = pygame.image.load("Caixa_Texto_Com_Foto_Boss.png").convert_alpha()
        self.boss_dialog_box = pygame.transform.scale(self.boss_dialog_box, (460, 155))  # Mesmo tamanho da caixa do jogador
        self.item_spawned = False  # Controle para spawnar o item apenas uma vez

    # def de dano do boss
    def tomar_dano_boss(self, dano):
        # Impede que o boss tome dano se já estiver morto
        if self.state == "morte":
            return
         
         # Reduz a vida do boss
        self.health -= dano
        if self.health <= 0:
            self.health = 0
            self.state = "morte"  # Define o estado como "morte"
            self.frame = 0 # Reinicia o frame para a animação de morte

    def update(self):
        # Conta o tempo de batalha se o diálogo já terminou
        if self.dialogue_complete:
            self.tempo_batalha += 1
            # Após 15 segundos, o boss entra em modo perseguição
            if self.tempo_batalha >= FPS * 15 and self.state not in ["perseguindo", "voltando", "morte"]:
                self.state = "perseguindo"
                self.tempo_perseguindo = 0

        if self.state == "dialogue":
            # Exibe os diálogos sequencialmente
            if not self.dialogo_mostrado:
                self.game.mostrar_dialogo_boss(self.dialogues[self.dialogue_index], self.dialogue_speakers[self.dialogue_index])
                self.dialogo_mostrado = True

        elif self.state == "idle":
            # Espera antes de se mover
            self.move_timer += 1
            if self.move_timer >= FPS * 0.5:
                self.move_direction = random.choice(["left", "right"])
                self.move_timer = 0
                self.state = "walk"

        elif self.state == "walk":
            # Movimento lateral
            self.anim_counter += 1
            if self.anim_counter % 8 == 0:
                self.frame = (self.frame + 1) % len(self.idle_anim)
                self.image = self.idle_anim[self.frame]

            if self.move_direction == "left":
                self.rect.x -= self.speed
            elif self.move_direction == "right":
                self.rect.x += self.speed

            if self.rect.x < 100:
                self.rect.x = 100
                self.move_direction = "right"
            elif self.rect.x > Largura - 100:
                self.rect.x = Largura - 100
                self.move_direction = "left"

            self.move_timer += 1
            if self.move_timer >= FPS:
                self.move_timer = 0
                self.state = "attack"

        elif self.state == "perseguindo":
            # Boss persegue o jogador por 10 segundos
            self.tempo_perseguindo += 1
            player = self.game.player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max((dx**2 + dy**2) ** 0.5, 0.1)
            self.rect.x += int(self.speed * dx / dist)
            self.rect.y += int(self.speed * dy / dist)

            self.anim_counter += 1
            if self.anim_counter % 8 == 0:
                self.frame = (self.frame + 1) % len(self.idle_anim)
                self.image = self.idle_anim[self.frame]

             # Controla o tempo entre ataques especiais
            self.tempo_ataque_especial += 1
            if self.tempo_ataque_especial >= FPS * 2:  # Ataca a cada 2 segundos
                self.ataque_especial()
                self.tempo_ataque_especial = 0   

            # Após 10s, começa a retornar à posição inicial
            if self.tempo_perseguindo >= FPS * 10:
                self.state = "voltando"

        elif self.state == "voltando":
            # Retorna à posição original antes de voltar ao estado normal
            destino_x, destino_y = self.pos_inicial
            dx = destino_x - self.rect.centerx
            dy = destino_y - self.rect.centery
            dist = max((dx**2 + dy**2) ** 0.5, 0.1)

            if dist < 5:
                self.rect.center = self.pos_inicial
                self.tempo_batalha = 0  # reinicia o ciclo de perseguição
                self.state = "idle"
            else:
                self.rect.x += int(self.speed * dx / dist)
                self.rect.y += int(self.speed * dy / dist)

        elif self.state == "attack":
            # Animação e ataque
            self.anim_counter += 1
            if self.anim_counter % 8 == 0:
                self.frame = (self.frame + 1) % len(self.current_anim)
                self.image = self.current_anim[self.frame]
            # Sincroniza o ataque com o final da animação
            if self.frame == len(self.attack_anim) - 1 and self.anim_counter % 8 == 0:
                self.attack()
                
            # Temporizador para pausa entre ataques
            self.attack_timer += 1
            if self.attack_timer >= FPS * 1.5: # Pausa de 1,5 segundos
                self.state = "idle"
                self.attack_timer = 0

        elif self.state == "morte":
            # Executa a animação de morte
            if self.frame < len(self.death_anim) - 1:
                self.anim_counter += 1
                if self.anim_counter % 8 == 0:
                    self.frame += 1
                    self.image = self.death_anim[self.frame]
            else:
                # Mantém o último sprite da animação de morte
                self.image = self.death_anim[-1]
                # Spawn do item após a morte
                if not self.item_spawned:
                    self.spawn_item()
                    self.item_spawned = True

    @property
    def current_anim(self):
        # Retorna animação atual com base no estado
        return self.attack_anim if self.state == "attack" else self.idle_anim

    def attack(self):
        # Troca para animação de ataque
        self.frame = 0
        self.anim_counter = 0
        # Lança projétil na direção do jogador
        player = self.game.player
        gust = WindGust(self.rect.centerx, self.rect.bottom, player.rect.centerx, player.rect.centery)
        self.all_sprites.add(gust)
        self.attack_group.add(gust)
    
    def ataque_especial(self):
    # lança 3 projéteis em direções levemente diferentes
        player = self.game.player
        cx, cy = self.rect.centerx, self.rect.bottom
        offsets = [-30, 0, 30]  # ângulos simulados (deslocamentos no alvo)

        for offset in offsets:
            alvo_x = player.rect.centerx + offset
            alvo_y = player.rect.centery
            gust = WindGust(cx, cy, alvo_x, alvo_y)
            self.all_sprites.add(gust)
            self.attack_group.add(gust)
        
        #Configurações da barra de vida
    def draw_health_bar(self, surface):
        """Desenha uma barra de vida épica para o boss."""
        if self.state == "morte":
            return
        barra_largura = 400
        barra_altura = 25
        barra_x = (Largura - barra_largura) // 2 # Centraliza horizontalmente
        barra_y = 50 # Posição vertical da barra
        # Calcula a proporção da vida restante        
        proporcao_vida = self.health / 200
        largura_vida = int(barra_largura * proporcao_vida)  # Vida máxima do boss é 200
        # Desenha a barra de fundo (preta)
        pygame.draw.rect(surface, (0, 0, 0), (barra_x, barra_y, barra_largura, barra_altura), border_radius=5)
        # Desenha a barra de vida (vermelha)
        pygame.draw.rect(surface, (200, 0, 0), (barra_x, barra_y, largura_vida, barra_altura), border_radius=5)
        # Desenha a borda da barra (dourada)        
        pygame.draw.rect(surface, (255, 215, 0), (barra_x, barra_y, barra_largura, barra_altura), 3, border_radius=5)
        # Desenha o nome do boss acima da barra        
        font_nome = pygame.font.Font(None, 36)  # Fonte para o nome do boss
        texto_nome = "Príncipe da Casa dos Pombos"
        texto_surface = font_nome.render(texto_nome, True, (255, 255, 255))
        texto_rect = texto_surface.get_rect(center=(Largura // 2, barra_y - 20))
        surface.blit(texto_surface, texto_rect)

    def next_dialogue(self):
        # Avança para o próximo diálogo ou inicia a luta
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogues):
            self.state = "idle"
            self.dialogue_complete = True
            self.dialogo_mostrado = False
        else:
            self.dialogo_mostrado = False

    def spawn_item(self):
        # Spawna o livro mágico como um coletável na frente do boss
        # Calcula a posição do livro mágico (na frente do boss)
        livro_x = self.rect.centerx
        livro_y = self.rect.bottom + 10# Ajuste para posicionar na frente do boss
        livro_magico = LivroMagico(livro_x, livro_y, self.game)
        # Adiciona o coletável ao grupo de sprites        
        self.all_sprites.add(livro_magico)
        

class LivroMagico(pygame.sprite.Sprite):
    """Classe para o coletável Livro Mágico."""

    def __init__(self, x, y, game):
        super().__init__()
        # Carrega a imagem do livro mágico
        self.image = pygame.image.load("livro_magico.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.game = game  # Referência ao jogo para acessar o jogador e lógica de coleta


    def update(self):
        # Verifica colisão com o jogador
        jogador_rect = self.game.player.rect
        if self.rect.colliderect(jogador_rect):
            # Coleta o item (incrementa contador ou realiza ação)            
            self.game.contadores_coletaveis["livro"] += 1
            self.kill()
            
            # Exibe o pop-up de coleta            
            self.game.mostrar_mensagem("Livro Mágico Coletado!", 100)

            # Garante que a tela de vitória só será chamada uma vez
            if not hasattr(self.game, "vitoria_exibida") or not self.game.vitoria_exibida:
                self.game.vitoria_exibida = True
                self.game.tela_vitoria()