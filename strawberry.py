"""
purpose: strawberry
"""
import pygame

class Strawberry:
    def __init__(self, position, ripe=True):
        self.position = pygame.Vector2(position)
        self.ripe = ripe

        # LOADING IMAGE
        self.image = pygame.image.load("assets/strawberry.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,(50, 50))

    def draw(self, screen):
        screen.blit(self.image, self.position)
    