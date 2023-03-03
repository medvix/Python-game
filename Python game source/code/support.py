from csv import reader
from os import walk
import pygame

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









