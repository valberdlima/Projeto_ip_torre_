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
    # BOSS Classe do Boss ---
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
            self.frame = 0  # Reinicia o frame para a animação de morte

    def update(self):
        if self.state == "dialogue":
            # Exibe os diálogos sequencialmente
            if not self.dialogo_mostrado:
                self.game.mostrar_dialogo_boss(self.dialogues[self.dialogue_index], self.dialogue_speakers[self.dialogue_index])
                self.dialogo_mostrado = True
            # A transição para o próximo diálogo ou estado é tratada no Game

        elif self.state == "idle":
            self.attack_timer += 1
            if self.attack_timer >= FPS * 1.5:  # 1.5 segundos
                self.state = "attack"
                self.attack_timer = 0

        elif self.state == "attack":
            # Controla a animação e os ataques
            self.anim_counter += 1
            if self.anim_counter % 8 == 0:
                self.frame = (self.frame + 1) % len(self.current_anim)
                self.image = self.current_anim[self.frame]

            # Sincroniza o ataque com o final da animação
            if self.frame == len(self.attack_anim) - 1 and self.anim_counter % 8 == 0:
                self.attack()

            # Temporizador para pausa entre ataques
            self.attack_timer += 1
            if self.attack_timer >= FPS * 1.5:  # Pausa de 1,5 segundos
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

    def draw_health_bar(self, surface):
        # Barra de vida acima do boss
        if self.state == "morte": # 
            return
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 12, SPRITE_Largura, 8))
        hp_width = SPRITE_Largura * (self.health / 200)
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 12, hp_width, 8))

    def next_dialogue(self):
        # Avança para o próximo diálogo ou inicia a luta
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogues):
            self.state = "idle"
            self.dialogue_complete = True
            self.dialogo_mostrado = False
        else:
            self.dialogo_mostrado = False