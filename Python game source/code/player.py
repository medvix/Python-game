import pygame
# from settings import*
from support import import_folder
from ui import *
from debug import debug
from support import tree_position


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, object_position):
		super().__init__(groups)
		self.image = pygame.image.load('../../Game_world/Icons/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0, 0)

		self.player_position = pos

		# grapgics
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement
		self.direction = pygame.math.Vector2()
		self.speed = 2
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		# inventory and crafting
		self.inventory = {"wood": 0, "stone": 0, "sticks": 0, "axe": 0, "pickaxe": 0}
		self.inventory_cooldown = 400
		self.inventory_cooldown_end = 0

		self.obstacle_sprites = obstacle_sprites
		self.inventoryIsOpened = False

		# mining
		self.objects = object_position


	def import_player_assets(self):
		character_path = '../../Game_world/Icons/Characters/character/'
		self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		keys = pygame.key.get_pressed()

		# movement input
		if not self.inventoryIsOpened:
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# attack input
			if keys[pygame.K_SPACE] and not self.attacking:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.mining()

			# use input
			if keys[pygame.K_LCTRL] and not self.attacking:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()

		# inventory
		if keys[pygame.K_e]:
			if pygame.time.get_ticks() >= self.inventory_cooldown_end:
				self.inventoryIsOpened = not self.inventoryIsOpened
				self.inventory_cooldown_end = pygame.time.get_ticks() + self.inventory_cooldown

		if keys[pygame.K_ESCAPE] and self.inventoryIsOpened:
			self.inventoryIsOpened = False

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
		"""""
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')
		"""""

	def move(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:  # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:  # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:  # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:  # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def mining(self):
		for i in range(0,len(self.objects),1):
			tree_rect = pygame.Rect(self.objects[i][1], self.objects[i][2], self.objects[i][3], self.objects[i][4])
			if self.hitbox.colliderect(tree_rect):
				if self.objects[i][0] == 'tree':
					self.inventory["wood"] += 3
				else:
					self.inventory["stone"] += 3

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		debug(self.inventory)
		self.animate()
		self.move(self.speed)
