import pygame

class Projectile:
    def __init__(self, x, y, target, speed=5):
        self.image = pygame.image.load('projectile.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.target = target

    def move(self):
        # Calculate direction towards the target
        direction = pygame.math.Vector2(self.target.rect.centerx - self.rect.centerx,
                                        self.target.rect.centery - self.rect.centery).normalize()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed
        print(f"Projectile moving towards target at ({self.target.rect.centerx}, {self.target.rect.centery})")

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def has_hit_target(self):
        return self.rect.colliderect(self.target.rect)
