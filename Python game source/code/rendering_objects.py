import pygame
from support import *
from settings import *

class render:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.image = pygame.image.load('../../Game_world/Icons/Objects/tree/Tree_1x2/1.png').convert_alpha()

    def directory_check(self, col):
        path = '../../Game_world/Icons/Objects/'
        name = ''
        if col == '0':
            name = 'tree/Tree_1x2'
            path = path + name
        elif col == '1':
            name = 'tree/Tree_2x2'
            path = path + name
        elif col == '3':
            name = 'tree/TreeBloom_2x2'
            path = path + name
        elif col == '16':
            name = 'stone/small'
            path = path + name
        elif col == '17':
            name = 'stone/big'
            path = path + name
        return path, name

    def csv_file_cycle(self, offset):
        layouts = {
            'objects': import_csv_layout('../../Game_world/export/map_object.csv')
        }
        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if style == 'objects' and col == '0' or col == '1' or col == '3' or col == '16' or col == '17':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        path, name = render.directory_check(self,col)
                        render.reader_drawer(self,(x,y),path,offset,name)

    def reader_drawer(self, pos, path, offset, name):
        image_path = path + '/1.png'
        image_load = pygame.image.load(image_path).convert_alpha()
        self.display_surface.blit(image_load,offset+pos)


