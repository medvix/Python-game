import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from rendering_objects import render
from ui import UI

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

		# objectt render
		self.ui = UI()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../../Game_world/export/map_floorblock.csv'),
			'objects': import_csv_layout('../../Game_world/export/map_object.csv')
		}
		for style,layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary' or style == 'objects':
							Tile((x,y),[self.obstacle_sprites],'invisible')

		self.player = Player((1400, 1000), [self.visible_sprites], self.obstacle_sprites)


	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.ui.display(self.player)




class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = (self.display_surface.get_size()[0] // 2)
		self.half_height = (self.display_surface.get_size()[1] // 2)
		self.offset = pygame.math.Vector2()

		# creating floor
		self.floor_surf = pygame.image.load('../../Game_world/export/map.jpg').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

		# object render
		self.render = render()

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# drawing object
		self.render.csv_file_cycle(floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)