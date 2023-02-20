import pygame
from settings import *
from support import *
import time

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # bar setup
        self.x = -125
        self.item_bar_rect = pygame.Rect(WIDTH // 2 + self.x,HEIGTH - 100,25,25)
        self.health_bar_rect = pygame.Rect((WIDTH //  2) - 160, HEIGTH - 58,320,5)

        self.image = pygame.image.load("../../Game_world/Icons/cf310145e43029a.png").convert_alpha()

        font = pygame.font.Font(None, 12)
        # inventory
        self.inventory = pygame.image.load("../../Game_world/Icons/inventory.png").convert_alpha()
        self.wood_image = pygame.image.load("../../Game_world/Icons/Objects/wood.png").convert_alpha()
        self.stone_image = pygame.image.load("../../Game_world/Icons/Objects/stone/big/stone.png").convert_alpha()
        self.player_image = pygame.image.load("../../Game_world/Icons/Characters/character_anim.gif").convert_alpha()
        self.text = font.render("64", True, (255, 255, 255))


    def display(self,player,x,y):
        pygame.draw.rect(self.display_surface,'red',self.health_bar_rect)
        self.display_surface.blit(self.image,((WIDTH //  2) - 160, HEIGTH-50+y))
        self.display_surface.blit(self.stone_image,((WIDTH // 2)-160+8, HEIGTH-50+8+y))
        self.display_surface.blit(self.text,((WIDTH // 2)-160+22, HEIGTH-50+3+y))
        self.display_surface.blit(self.wood_image,((WIDTH // 2)-160+8+32, HEIGTH-50+8+y))
        self.display_surface.blit(self.text,((WIDTH // 2)-160+22+32, HEIGTH-50+3+y))

    def draw_inventory(self,player):
        if player.inventoryIsOpened:
            self.display_surface.blit(self.inventory,((WIDTH // 2)-170, (HEIGTH // 2)-110))
            UI.display(self,player,0,-210)
            self.display_surface.blit(self.player_image,((WIDTH // 2)+(55/2), (HEIGTH // 2)-110+(90/2)))




"""""            
            for i, item in enumerate(player.inventory.items()):
                item_name, item_quantity = item
                font = pygame.font.Font(None, 30)
                text = font.render(item_name + ": " + str(item_quantity), True, (255, 255, 255))
                self.display_surface.blit(text, (100 + 50 * i, 500))"""""





