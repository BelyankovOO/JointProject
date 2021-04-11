import pygame
import system
import random
import math
import utility

images = {'shuriken':[], 'yellow_shuriken': []}
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken/shuriken0.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken/shuriken1.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken/shuriken2.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken/shuriken3.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/shuriken/shuriken4.png"))

images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/yellow_shuriken/yellow_shuriken0.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/yellow_shuriken/yellow_shuriken1.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/yellow_shuriken/yellow_shuriken2.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/yellow_shuriken/yellow_shuriken3.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER+"bullets/yellow_shuriken/yellow_shuriken4.png"))



class EnemyWeapon(pygame.sprite.Sprite):
	def __init__(self, position, y, enemy_border):
		pygame.sprite.Sprite.__init__(self)
		self.image = images['shuriken'][0]
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		if position == 1:
			self.speed_x = random.randrange(1, system.MAX_ENEMY_WEAPON_SPEED)
			self.speed_y = random.randrange(- system.MAX_ENEMY_WEAPON_SPEED,  system.MAX_ENEMY_WEAPON_SPEED)
			self.rect.right = enemy_border
		elif position == 0:
			self.speed_x = random.randrange(- system.MAX_ENEMY_WEAPON_SPEED, -1)
			self.speed_y = random.randrange(- system.MAX_ENEMY_WEAPON_SPEED,  system.MAX_ENEMY_WEAPON_SPEED)
			self.rect.left = system.WIN_WIDTH - enemy_border   
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
		L[0] = L[0]/s_L
		L[1] = L[1]/s_L
		norm[0] = norm[0]/s_norm
		norm[1] = norm[1]/s_norm
		#self.speed_x = s_L*(norm[0])
		#self.speed_y = s_L*(norm[1])
		scalarNL = L[0]*norm[0] + L[1]*norm[1]
		#self.speed_x = s_L*(L[0]-2*scalarNL*norm[0])
		#self.speed_y = s_L*(L[1]-2*scalarNL*norm[1])
		self.speed_x = s_L*norm[0]
		self.speed_y = s_L*norm[1]
		#print("ref ", norm, colide_point_center)

	def reset_can_damage(self):
		self.can_damage = True

	def on_hit(self):
		self.can_damage = False
		self.cooldowns['can_damage'] = system.SHURIKEN_COOLDOWN_AFTER_REFLECT
		
	def image_rotation(self):
		if self.can_damage: 
			self.image_num = (self.image_num+1)%5
			self.image = images['shuriken'][self.image_num]
			self.mask = pygame.mask.from_surface(self.image)
			self.cooldowns['rotation'] = (system.SHURIKEN_ROTATION/self.velocity)
		else: 
			self.image_num = (self.image_num+1)%5
			self.image = images['yellow_shuriken'][self.image_num]
			self.mask = pygame.mask.from_surface(self.image)
			self.cooldowns['rotation'] = (system.SHURIKEN_ROTATION/self.velocity)	

	  
