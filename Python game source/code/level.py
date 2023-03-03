import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from ui import UI
from random import choice
import time
import player

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# objects position
		self.trees = tree_position()

		# sprite setup
		self.create_map()

		# ui render
		self.ui = UI()

		# objects position

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../../Game_world/export/map_floorblock.csv'),
			'objects': import_csv_layout('../../Game_world/export/map_objects.csv')
		}
		graphics ={
			'tree': import_folder("../../Game_world/Icons/Objects/tree/Tree_2x2"),
			'stone': import_folder("../../Game_world/Icons/Objects/stone/big")
		}


		for style,layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'objects' and col == '1':
							random_tree_image = choice(graphics['tree'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'tree',random_tree_image)
							self.trees.add_position('tree',x,y)
						if style == 'objects' and col == '17':
							random_stone_image = choice(graphics['stone'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'stone',random_stone_image)
							self.trees.add_position('stone',x,y)

		self.player = Player((1400, 1000), [self.visible_sprites], self.obstacle_sprites, self.trees.get_positions())

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.ui.display(self.player.inventory,0,0)
		if self.player.inventoryIsOpened:
			self.ui.draw_inventory(self.player)

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
		self.floor_surf_night = pygame.image.load('../../Game_world/map_night.jpg').convert()
		self.start_time = time.time()
		self.day_alpha = 255
		self.night_alpha = 0
		self.time_changed = False
		self.day = True


	def custom_draw(self,player):

		# getting the offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		elapsed_time = time.time() - self.start_time
		current_minute = int(time.strftime("%M"))

		if current_minute % 2 == 0:
			self.time_changed = True		# time Day
			self.day = True
		else:
			self.time_changed = True		# time Night
			self.day = False

		# self.floor_surf_night.set_alpha(255) 0 is transparent

		# changing day and night
		if self.time_changed and self.day:
			if self.day_alpha == 255:
				self.time_changed = False
			elif self.day_alpha < 255  and self.night_alpha >= 0:
				self.day_alpha += 1
				self.night_alpha -= 1
		if self.time_changed and self.day == False:
			if self.night_alpha == 255:
				self.time_changed = False
			elif self.night_alpha < 255 and self.day_alpha >= 0:
				self.night_alpha += 1
				self.day_alpha -= 1

		self.floor_surf.set_alpha(self.day_alpha)
		self.floor_surf_night.set_alpha(self.night_alpha)

		# drawing floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf_night,floor_offset_pos)
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
