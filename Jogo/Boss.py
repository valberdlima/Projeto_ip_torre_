import pygame
import random

pygame.init()

# Tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Fight")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonte
font = pygame.font.SysFont(None, 30)


# Classe do Boss
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((150, 150))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH // 2, 100))
        self.health = 100
        self.speed = 3
        self.direction = 1
        self.attack_timer = 0

    def update(self):
        # Movimento horizontal
        self.rect.x += self.speed * self.direction
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1

        # Ataque temporizado
        self.attack_timer += 1
        if self.attack_timer >= 120:  # a cada 2 segundos
            self.attack()
            self.attack_timer = 0

    def attack(self):
        # Pode ser um projétil ou outro ataque
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        boss_bullets.add(bullet)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def draw_health_bar(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, 150, 10))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 10, 150 * (self.health / 100), 10))


# Classe de projétil
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Jogador (simples)
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 60, 50, 50)

# Grupos de sprites
all_sprites = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()

# Instanciando o boss
boss = Boss()
all_sprites.add(boss)

# Loop principal
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    # Atualização
    all_sprites.update()

    # Colisão com projéteis do boss
    if any(b.rect.colliderect(player) for b in boss_bullets):
        print("Jogador atingido!")

    # Render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    boss.draw_health_bar(screen)
    pygame.draw.rect(screen, (0, 0, 255), player)  # jogador
    pygame.display.flip()

pygame.quit()
