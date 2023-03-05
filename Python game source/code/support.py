from csv import reader
from os import walk
import pygame
from settings import *

#  Objects id
#  Stones(16 and 17)
#  Trees(0,1,2,3,4,9,10,11,12,13,36,37)


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


# for objects and character animation
def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

class tree_position:
    def __init__(self):
        self.positions = []

    def add_position(self, material,x, y):
        if material == 'tree':
            self.positions.append((material,x-16, y-16, 64, 64))
        else:
            self.positions.append((material, x-16, y-16, 48, 48 ))

    def get_positions(self):
        return self.positions


def blit_fade_image(image_path, screen):
    # Load the image and get its rect
    image = pygame.image.load(image_path).convert_alpha()
    image_rect = (WIDTH-210,HEIGTH/2-80)

    # Gradually increase alpha from 0 to 255 in 5 seconds
    alpha = 0
    alpha_step = 255 / 1000
    last_time = pygame.time.get_ticks()
    while alpha < 255:
        # Calculate the new alpha value based on the elapsed time
        elapsed_time = pygame.time.get_ticks() - last_time
        alpha = int(alpha_step * elapsed_time)
        alpha = min(alpha, 255)  # Cap alpha at 255

        # Set the alpha value of the image surface
        image.set_alpha(alpha)

        screen.blit(image, image_rect)
        pygame.display.flip()

    # Gradually decrease alpha from 255 to 0 in 5 seconds
    alpha = 255
    alpha_step = 255 / 1000
    last_time = pygame.time.get_ticks()
    while alpha > 0:
        # Calculate the new alpha value based on the elapsed time
        elapsed_time = pygame.time.get_ticks() - last_time
        alpha = 255 - int(alpha_step * elapsed_time)
        alpha = max(alpha, 0)  # Cap alpha at 0

        # Set the alpha value of the image surface
        image.set_alpha(alpha)

        screen.blit(image, image_rect)
        pygame.display.flip()

