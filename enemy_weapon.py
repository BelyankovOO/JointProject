import pygame
import system
import random
import math
import utility

images = {'shuriken':[]}
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken0.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken1.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken2.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken3.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken4.png"))

class EnemyWeapon(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = images['shuriken'][0]
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		if x == 0:
			self.speed_x = random.randrange(1, system.MAX_ENEMY_WEAPON_SPEED)
			self.speed_y = random.randrange(- system.MAX_ENEMY_WEAPON_SPEED,  system.MAX_ENEMY_WEAPON_SPEED)
			self.rect.right = x+system.ENEMY_WIDTH
		elif x == system.WIN_WIDTH-system.ENEMY_WIDTH:
			self.speed_x = random.randrange(- system.MAX_ENEMY_WEAPON_SPEED, -1)
			self.speed_y = random.randrange(- system.MAX_ENEMY_WEAPON_SPEED,  system.MAX_ENEMY_WEAPON_SPEED)
			self.rect.left = x   
		self.start_x = x
		self.start_y = y
		self.rect.centery = y
		self.timer_last = pygame.time.get_ticks()
		self.delta_time = 0
		self.image_num = 0
		self.velocity = math.sqrt(self.speed_x**2+self.speed_y**2)
		self.can_damage = True
		self.cooldowns = {'can_damage':0, 'rotation': (system.SHURIKEN_ROTATION/self.velocity)}
		

	def update(self):
		now = pygame.time.get_ticks()
		self.delta_time = now - self.timer_last;
		self.timer_last = now
		utility.cooldown_tick(self.cooldowns, self.delta_time, {
											'can_damage': self.reset_can_damage,
											'rotation': self.image_rotation
											})
		self.crossing()
		self.rect.y += self.speed_y
		self.rect.x += self.speed_x

	def crossing(self):    
		if self.rect.top < 0:
			self.rect.top = 0
			self.speed_y = -self.speed_y
			self.can_damage = True
		if self.rect.bottom > system.WIN_HEIGHT:
			self.rect.bottom = system.WIN_HEIGHT
			self.speed_y = -self.speed_y
			self.can_damage = True
		if self.rect.right < 0:
			self.rect.right = 0
			self.speed_x = -self.speed_x
			self.can_damage = True
		if self.rect.left > system.WIN_WIDTH:
			self.rect.left = system.WIN_WIDTH
			self.speed_x = -self.speed_x 
			self.can_damage = True

	def reflect_direction(self, colide_point_center):
		L = [self.speed_x, self.speed_y]
		norm = [self.rect.x-colide_point_center[0], self.rect.y-colide_point_center[1]]
		s_norm = math.sqrt(norm[0]**2+norm[1]**2)
		s_L = math.sqrt(L[0]**2+L[1]**2)
		norm[0] = norm[0]/s_norm
		norm[1] = norm[1]/s_norm
		self.speed_x = s_L*(norm[0])
		self.speed_y = s_L*(norm[1]) 

	def reset_can_damage(self):
		self.can_damage = True

	def on_hit(self):
		self.can_damage = False
		self.cooldowns['can_damage'] = system.SHURIKEN_COOLDOWN_AFTER_REFLECT
		
	def image_rotation(self):
		self.image_num = (self.image_num+1)%5
		self.image = images['shuriken'][self.image_num]
		self.mask = pygame.mask.from_surface(self.image)
		self.cooldowns['rotation'] = (system.SHURIKEN_ROTATION/self.velocity)
	  
