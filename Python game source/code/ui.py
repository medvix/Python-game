import pygame
from settings import *
from support import *
import time
import crafting

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # bar setup
        self.x = -125
        self.item_bar_rect = pygame.Rect(WIDTH // 2 + self.x,HEIGTH - 100,25,25)
        self.health_bar_rect = pygame.Rect((WIDTH //  2) - 160, HEIGTH - 58,320,5)

        self.image = pygame.image.load("../../Game_world/Icons/cf310145e43029a.png").convert_alpha()

        self.font = pygame.font.Font(None, 12)
        # inventory
        self.inventory = pygame.image.load("../../Game_world/Icons/inventory.png").convert_alpha()
        self.wood_image = pygame.image.load("../../Game_world/Icons/Objects/wood.png").convert_alpha()
        self.stone_image = pygame.image.load("../../Game_world/Icons/Objects/stone/big/stone.png").convert_alpha()
        self.player_image = pygame.image.load("../../Game_world/Icons/Characters/character_anim.gif").convert_alpha()

        # button
        self.button_pressed = False

        # crafting
        self.crafted = True

    def display(self,inventory,x,y):
        pygame.draw.rect(self.display_surface,'red',self.health_bar_rect)
        self.display_surface.blit(self.image,((WIDTH //  2) - 160+x, HEIGTH-50+y))
        self.display_surface.blit(self.stone_image,((WIDTH // 2)-160+8+x, HEIGTH-50+8+y))
        self.display_surface.blit(self.font.render(str(inventory["stone"]), True, (255, 255, 255)),((WIDTH // 2)-160+22+x, HEIGTH-50+3+y))
        self.display_surface.blit(self.wood_image,((WIDTH // 2)-160+8+32+x, HEIGTH-50+8+y))
        self.display_surface.blit(self.font.render(str(inventory["wood"]), True, (255, 255, 255)),((WIDTH // 2)-160+22+32+x, HEIGTH-50+3+y))

    def draw_inventory(self,player):
        if player.inventoryIsOpened:
            self.display_surface.blit(self.inventory,((WIDTH // 2)-170, (HEIGTH // 2)-110))
            UI.display(self,player.inventory,-1,-210)
            self.display_surface.blit(self.player_image,((WIDTH // 2)+(55/2), (HEIGTH // 2)-110+(90/2)))
            # rendering button for crafting
            self.button('STICKS', 20, (WIDTH / 4) + 45, (HEIGTH // 2) - 110 + 1, 100, 40, 'white',
                        (26, 26, 26),'black','white', 2, crafting.sticks, player.inventory)
            self.button('AXE',20,(WIDTH/4)+45,(HEIGTH // 2)-110+1+45,100,40,'white',(26, 26, 26),'black',
                        'white',2,crafting.axe,player.inventory)
            self.button('PICKAXE',20,(WIDTH/4)+45,(HEIGTH // 2)-110+1+90,100,40,'white',(26, 26, 26),'black'
                        ,'white',2,crafting.pickaxe,player.inventory)
            if not self.crafted:
                blit_fade_image('../../Game_world/Icons/error.png', self.display_surface)
                self.crafted = True

    def button(self, text, font_size, x, y, width, height, text_color, color, highlight_color, border_color, border_size, pressed, inventory):
        # Create font object and render text surface
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, text_color)

        # Create button rectangle
        button_rect = pygame.Rect(x, y, width, height)

        # Draw button border
        pygame.draw.rect(pygame.display.get_surface(), border_color, button_rect, border_size)

        # Draw button background
        pygame.draw.rect(pygame.display.get_surface(), color, button_rect.inflate(-border_size*2, -border_size*2))

        # Center text within button rectangle
        text_rect = text_surface.get_rect(center=button_rect.center)

        # Highlight button on mouse over
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            text_surface = font.render(text, True, 'white')
            pygame.draw.rect(pygame.display.get_surface(), highlight_color, button_rect, border_size)

            # Detect button press and print message
            current_time = pygame.time.get_ticks()
            if pygame.mouse.get_pressed()[0] and current_time - pressed.last_pressed_time >= 500:
                pressed.last_pressed_time = current_time
                self.crafted = pressed(inventory)
        else:
            pressed.last_pressed_time = 0

        # Draw text surface onto display surface
        pygame.display.get_surface().blit(text_surface, text_rect)