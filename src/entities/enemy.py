import pygame

class Enemy:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load('assets/images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = 100
        self.path = []

    def set_path(self, path):
        self.path = path.copy()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
