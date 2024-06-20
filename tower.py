import pygame
from projectile import Projectile

class Tower:
    def __init__(self, x, y):
        self.image = pygame.image.load('tower.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = 100
        self.damage = 10
        self.projectiles = []

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for projectile in self.projectiles:
            projectile.draw(screen)

    def attack(self, enemies):
        for enemy in enemies:
            if self.rect.centerx - self.range < enemy.rect.centerx < self.rect.centerx + self.range and \
               self.rect.centery - self.range < enemy.rect.centery < self.rect.centery + self.range:
                print(f"Enemy within range at ({enemy.rect.centerx}, {enemy.rect.centery})")
                # Create a projectile targeting the enemy
                projectile = Projectile(self.rect.centerx, self.rect.centery, enemy)
                self.projectiles.append(projectile)
                print(f"Projectile created at ({projectile.rect.centerx}, {projectile.rect.centery}) targeting enemy at ({enemy.rect.centerx}, {enemy.rect.centery})")
                break

    def update_projectiles(self, screen):
        for projectile in self.projectiles[:]:
            projectile.move()
            print(f"Projectile moved to ({projectile.rect.centerx}, {projectile.rect.centery})")
            if projectile.has_hit_target():
                projectile.target.health -= self.damage
                print(f"Projectile hit enemy at ({projectile.target.rect.centerx}, {projectile.target.rect.centery}). Enemy health: {projectile.target.health}")
                self.projectiles.remove(projectile)
            elif not screen.get_rect().colliderect(projectile.rect):
                print(f"Projectile out of bounds and removed at ({projectile.rect.centerx}, {projectile.rect.centery})")
                self.projectiles.remove(projectile)
