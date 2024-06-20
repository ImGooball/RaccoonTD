import pygame

class Enemy:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = 100

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
