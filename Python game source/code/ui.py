import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # bar setup
        self.x = -125
        self.item_bar_rect = pygame.Rect(WIDTH // 2 + self.x,HEIGTH - 100,25,25)
        self.health_bar_rect = pygame.Rect((WIDTH //  2) - 160, HEIGTH - 58,320,5)

        self.image = pygame.image.load("../../Game_world/Icons/cf310145e43029a.png").convert_alpha()

    def display(self,player):
        pygame.draw.rect(self.display_surface,'red',self.health_bar_rect)
        self.display_surface.blit(self.image,((WIDTH //  2) - 160, HEIGTH-50))

