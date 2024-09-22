import pygame
import random

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Battle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 30, GREEN)
        self.speed = 5
        self.health = 100
        self.lives = 3
        self.score = 0

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        return Projectile(self.rect.right, self.rect.centery)

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 30, RED)
        self.speed = 2
        self.health = 30

    def move(self):
        self.rect.x -= self.speed

    def shoot(self):
        if random.randint(1, 100) == 1:
            return Projectile(self.rect.left, self.rect.centery, -5)
        return None

class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface([100, 60])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 200
        self.speed = 1

    def shoot(self):
        if random.randint(1, 50) == 1:
            return Projectile(self.rect.left, self.rect.centery, -7)
        return None

class Projectile(GameObject):
    def __init__(self, x, y, speed=7):
        super().__init__(x, y, 10, 5, YELLOW)
        self.speed = speed

    def move(self):
        self.rect.x += self.speed

class Collectible(GameObject):
    def __init__(self, x, y, type):
        super().__init__(x, y, 20, 20, YELLOW)
        self.type = type  # 'health' or 'extra_life'

class Game:
    def __init__(self):
        self.player = Player(50, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.level = 1
        self.boss = None
        self.font = pygame.font.Font(None, 36)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.projectiles.add(self.player.shoot())

            keys = pygame.key.get_pressed()
            self.player.move(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
                             keys[pygame.K_DOWN] - keys[pygame.K_UP])

            self.update()
            self.draw()

            if self.player.lives <= 0:
                running = self.game_over()

            clock.tick(60)

        pygame.quit()

    def update(self):
        # Spawn enemies
        if random.randint(1, 60) == 1 and len(self.enemies) < 5 + self.level:
            self.enemies.add(Enemy(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - 30)))

        # Spawn collectibles
        if random.randint(1, 180) == 1:
            collectible_type = random.choice(['health', 'extra_life'])
            self.collectibles.add(Collectible(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - 20), collectible_type))

        # Update all sprite groups
        self.all_sprites.update()
        self.enemies.update()
        self.projectiles.update()
        self.collectibles.update()

        # Move enemies, projectiles, and check for off-screen
        for enemy in self.enemies:
            enemy.move()
            enemy_projectile = enemy.shoot()
            if enemy_projectile:
                self.projectiles.add(enemy_projectile)
            if enemy.rect.right < 0:
                enemy.kill()

        for projectile in self.projectiles:
            projectile.move()
            if projectile.rect.left > SCREEN_WIDTH or projectile.rect.right < 0:
                projectile.kill()

        # Check for collisions
        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, True):
            self.player.health -= 10
            if self.player.health <= 0:
                self.player.lives -= 1
                self.player.health = 100

        for collectible in pygame.sprite.spritecollide(self.player, self.collectibles, True):
            if collectible.type == 'health':
                self.player.health = min(self.player.health + 20, 100)
            elif collectible.type == 'extra_life':
                self.player.lives += 1

        for enemy in pygame.sprite.groupcollide(self.enemies, self.projectiles, False, True):
            enemy.health -= 10
            if enemy.health <= 0:
                enemy.kill()
                self.player.score += 10

        # Check for level completion
        if self.player.score >= self.level * 100:
            self.level += 1
            if self.level % 3 == 0:  # Boss level every 3rd level
                self.spawn_boss()

        # Update boss
        if self.boss:
            self.boss.move()
            boss_projectile = self.boss.shoot()
            if boss_projectile:
                self.projectiles.add(boss_projectile)
            if pygame.sprite.collide_rect(self.player, self.boss):
                self.player.health -= 20
                if self.player.health <= 0:
                    self.player.lives -= 1
                    self.player.health = 100
            for projectile in pygame.sprite.spritecollide(self.boss, self.projectiles, True):
                self.boss.health -= 10
                if self.boss.health <= 0:
                    self.boss.kill()
                    self.boss = None
                    self.player.score += 100

    def draw(self):
        screen.fill(WHITE)
        self.all_sprites.draw(screen)
        self.enemies.draw(screen)
        self.projectiles.draw(screen)
        self.collectibles.draw(screen)
        if self.boss:
            screen.blit(self.boss.image, self.boss.rect)

        # Draw HUD
        score_text = self.font.render(f"Score: {self.player.score}", True, BLACK)
        health_text = self.font.render(f"Health: {self.player.health}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, BLACK)
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))
        screen.blit(lives_text, (10, 90))
        screen.blit(level_text, (SCREEN_WIDTH - 100, 10))

        pygame.display.flip()

    def spawn_boss(self):
        self.boss = BossEnemy(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - 30)

    def game_over(self):
        screen.fill(BLACK)
        game_over_text = self.font.render("GAME OVER", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()  # Reset the game
                        return True
                    elif event.key == pygame.K_q:
                        return False
        return False

if __name__ == "__main__":
    game = Game()
    game.run()