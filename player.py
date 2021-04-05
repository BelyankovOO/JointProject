import pygame
import system
import weapon
import utility
import lives

image_reflect = pygame.image.load(system.IMAGES_FOLDER+"hero/hero_reflect.png")
image_simple = pygame.image.load(system.IMAGES_FOLDER+"hero/hero.png")
image_invulnerable = pygame.image.load(system.IMAGES_FOLDER+"hero/hero_invulnerable.png")
		
class Player(pygame.sprite.Sprite):
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
		self.image = image_simple
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.screen = screen
		self.speed_x = 0
		self.speed_y = 0
		self.start_x =  self.rect.centerx
		self.start_y =  self.rect.centery
		self.on_ground = False
		self.cooldowns = {'reflect_cd': 0 , 'shoot': 0, 'reflect_time' : 0, 'invulnerable_time': 0}
		self.timer_last = pygame.time.get_ticks()
		self.delta_time = 0
		self.lives = lives.Lives()
		self.invulnerability = False

	def update(self):
		self.speed_x = 0
		self.lives.draw(self.screen)
		keystate = pygame.key.get_pressed()
		now = pygame.time.get_ticks()
		self.delta_time = now - self.timer_last;
		self.timer_last = now
		#tick cooldowns
		utility.cooldown_tick(self.cooldowns, self.delta_time, {'reflect_time' : self.reset_image, 'invulnerable_time' : self.reset_image})
		if not self.isReflecting():
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
		if (self.cooldowns['shoot']==0):
			weapon_x = weapon.Weapon(self.rect.centerx, self.rect.centery)
			all_sprites.add(weapon_x)
			weapon_sprites.add(weapon_x)      
			self.cooldowns['shoot']=system.PLAYER_SHOOT_CD 

	def reset_image(self):
		self.image = image_simple
		self.mask = pygame.mask.from_surface(self.image)
	
	def reflect(self):
		if (self.cooldowns['reflect_cd']==0):
			self.image = image_reflect
			self.mask = pygame.mask.from_surface(self.image)
			self.cooldowns['reflect_cd']=system.PLAYER_REFLECT_CD
			self.cooldowns['reflect_time']=system.PLAYER_REFLECTING_TIME

	def invulnerable(self):
		self.image = image_invulnerable
		self.mask = pygame.mask.from_surface(self.image)
		self.cooldowns['invulnerable_time'] = system.PLAYER_INVULNERABLE_TIME		

	def isReflecting(self):
		return self.cooldowns['reflect_time']>0

	def isInvulnerable(self):
		return self.cooldowns['invulnerable_time']>0	

	def isAlive(self):
		if self.lives.check_number_of_of_lives()>0:
			self.invulnerable()
			return True
		else: 
			return False		

	def getCenter(self):
		return (self.rect.centerx, self.rect.centery)

	def getDamage(self):
		self.lives.decrease_number_of_lives()



			