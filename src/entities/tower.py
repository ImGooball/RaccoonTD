import pygame
from src.entities.projectile import Projectile

class Tower:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/images/tower.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = 100
        self.damage = 34
        self.projectiles = []
        self.cooldown = 500  # Cooldown time in milliseconds
        self.last_shot_time = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for projectile in self.projectiles:
            projectile.draw(screen)

    def attack(self, enemies, current_time):
        if current_time - self.last_shot_time < self.cooldown:
            return
        for enemy in enemies:
            if self.rect.centerx - self.range < enemy.rect.centerx < self.rect.centerx + self.range and \
               self.rect.centery - self.range < enemy.rect.centery < self.rect.centery + self.range:
                projectile = Projectile(self.rect.centerx, self.rect.centery, enemy)
                self.projectiles.append(projectile)
                self.last_shot_time = current_time
                break

    def update_projectiles(self, screen):
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.has_hit_target():
                projectile.target.health -= self.damage
                self.projectiles.remove(projectile)
            elif not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
