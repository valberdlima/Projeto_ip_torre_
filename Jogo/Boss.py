import pygame
from assets import get_sprites, BOSS_WIND_SPRITESHEET
from config import SPRITE_Largura, SPRITE_Altura, FPS, Largura, Altura
import random


boss_spritesheet = pygame.transform.scale(pygame.image.load("boss spritesheet.png"), (832, 3456))

# --- Primeiro, defina as animações do boss ---
sprites = get_sprites(boss_spritesheet, 54, 13, SPRITE_Largura, SPRITE_Altura)

ANIM_BOSS_IDLE = sprites[26:33]    # linha 0, cols 0–7
ANIM_BOSS_ATTACK = sprites[182:188]  # linha 1, cols 0–7

# BOSS Classe do projétil de vento ---
class WindGust(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        # >>> GPT: Cria imagem circular transparente com efeito de vento
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (180, 220, 255, 180), (15, 15), 15)
        self.rect = self.image.get_rect(center=(x, y))

        # Calcula a direção para o alvo (jogador)
        dx = target_x - x
        dy = target_y - y
        distance = max((dx**2 + dy**2) ** 0.5, 0.1)  # evita divisão por zero

        self.speed = 6
        self.velocity_x = self.speed * dx / distance
        self.velocity_y = self.speed * dy / distance

    def update(self):
        # >>> GPT: Movimento contínuo do projétil
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # mata se sair da tela
        if (self.rect.right < 0 or self.rect.left > Largura or 
            self.rect.bottom < 0 or self.rect.top > Altura):
            self.kill()


# BOSS Classe do Boss ---
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites_group, attack_group, game):
        super().__init__()
        self.idle_anim = ANIM_BOSS_IDLE
        self.attack_anim = ANIM_BOSS_ATTACK
        self.frame = 0
        self.anim_counter = 0
        self.state = "idle"  # Estado inicial
        self.dialogo_mostrado = False  # Controle do diálogo
        self.attack_timer = 0

        self.image = self.idle_anim[self.frame]
        self.rect = self.image.get_rect(center=(x, y))

        self.health = 200
        self.all_sprites = all_sprites_group
        self.attack_group = attack_group
        self.game = game  # Referência ao jogo para acessar `self.mostrar_mensagem`

    def update(self):
        if self.state == "idle":
            # Mostra o diálogo na tela antes de atacar
            if not self.dialogo_mostrado:
                self.game.mostrar_mensagem("Prepare-se para enfrentar meu poder!", 120)
                self.dialogo_mostrado = True
            else:
                # Após esperar por 5 segundos, muda para o estado de ataque
                self.attack_timer += 1
                if self.attack_timer >= FPS * 5:  # 5 segundos
                    self.state = "attack"
                    self.attack_timer = 0

        elif self.state == "attack":
            # Controla a animação e os ataques
            self.anim_counter += 1
            if self.anim_counter % 8 == 0:
                self.frame = (self.frame + 1) % len(self.current_anim)
                self.image = self.current_anim[self.frame]

            # Temporizador de ataque
            self.attack_timer += 1
            if self.attack_timer >= FPS * 2:  # Ataca a cada 2 segundos
                self.attack()
                self.attack_timer = 0

    @property
    def current_anim(self):
        # Retorna animação atual com base no estado
        return self.attack_anim if self.state == "attack" else self.idle_anim

    def attack(self):
        # Troca para animação de ataque
        self.frame = 0
        self.anim_counter = 0

        # >>> GPT: Lança projétil na direção do jogador
        player = self.game.player  # >>> GPT: Garante que o boss saiba onde está o player
        gust = WindGust(self.rect.centerx, self.rect.bottom, player.rect.centerx, player.rect.centery)
        self.all_sprites.add(gust)
        self.attack_group.add(gust)

    def draw_health_bar(self, surface):
        # Barra de vida acima do boss
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 12, SPRITE_Largura, 8))
        hp_width = SPRITE_Largura * (self.health / 200)
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 12, hp_width, 8))
