import pygame
import system
import weapon

class Player(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((system.PLAYER_WIDTH, system.PLAYER_HEIGHT))
		#self.image.fill(pygame.Color(system.PLAYER_COLOR))
		#self.rect = pygame.Rect(x, y, system.PLAYER_WIDTH, system.PLAYER_HEIGHT)
		self.image_reflect = pygame.image.load(system.IMAGES_FOLDER+"hero/hero_reflect.png")
		self.image_simple = pygame.image.load(system.IMAGES_FOLDER+"hero/hero.png")
		self.image = self.image_simple
		self.rect = self.image.get_rect()
		self.speed_x = 0
		self.speed_y = 0
		self.start_x =  self.rect.centerx
		self.start_y =  self.rect.centery
		self.on_ground = False
		self.cooldowns = { 'reflect_cd': 0 , 'shoot': 0, 'reflect_time' : 0}
		self.timer_last = pygame.time.get_ticks()
		self.delta_time = 0

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		now = pygame.time.get_ticks()
		self.delta_time = now - self.timer_last;
		self.timer_last = now
		#tick cooldowns
		for name in self.cooldowns:
			self.cooldowns[name] -= self.delta_time
			if self.cooldowns[name] < 0:
				self.cooldowns[name] = 0
				if name=='reflect_time':
					self.image = self.image_simple
		if not self.isReflecting():
			self.image = self.image_simple
			if keystate[pygame.K_UP]:
				if self.on_ground:
					self.speed_y = -system.PLAYER_JUMP
			if keystate[pygame.K_LEFT]:
				self.speed_x = -system.PLAYER_SPEED
			if keystate[pygame.K_RIGHT]:
				self.speed_x = system.PLAYER_SPEED
			if keystate[pygame.K_SPACE]:
				self.reflect()
		if not self.on_ground:
			self.speed_y += system.GRAVITY
		self.on_ground = False     
		self.rect.centerx  += self.speed_x
		self.rect.centery  += self.speed_y
		self.crossing()

	def crossing(self):
		if self.rect.right > system.WIN_WIDTH:
			self.rect.right = system.WIN_WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
			self.speed_y = 0
		if self.rect.bottom > system.WIN_HEIGHT:
			self.rect.bottom = system.WIN_HEIGHT
			self.on_ground = True
			self.speed_y = 0  

	def shoot(self, all_sprites, weapon_sprites):
		#weapon_x = weapon.Weapon(self.rect.centerx, self.rect.centery)
		#all_sprites.add(weapon_x)
		#weapon_sprites.add(weapon_x)
		if (self.cooldowns['shoot']==0):
			weapon_x = weapon.Weapon(self.rect.centerx, self.rect.centery)
			all_sprites.add(weapon_x)
			weapon_sprites.add(weapon_x)      
			self.cooldowns['shoot']=system.PLAYER_SHOOT_CD 

	def reflect(self):
		if (self.cooldowns['reflect_cd']==0):
			self.image = self.image_reflect
			self.cooldowns['reflect_cd']=system.PLAYER_REFLECT_CD
			self.cooldowns['reflect_time']=system.PLAYER_REFLECTING_TIME

	def isReflecting(self):
		return self.cooldowns['reflect_time']>0

	def getCenter(self):
		return (self.rect.centerx, self.rect.centery)		                     

