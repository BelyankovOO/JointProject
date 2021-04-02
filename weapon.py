import pygame
import system

class Weapon(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((system.WEAPON_WIDTH, 0))
		self.image.fill(pygame.Color(system.WEAPON_COLOR))
		self.rect =  pygame.Rect(x, y, system.WEAPON_WIDTH, 0)
		self.start_x = x
		self.start_y = y
		self.rect.y = y
		self.rect.x = x
		self.height = 0
		#self.speedy = -10

	def update(self):
		self.height += system.WEAPON_SPEED
		if self.height > system.WEAPON_HEIGHT:
			self.kill()
		self.image = pygame.transform.scale(self.image, (system.WEAPON_WIDTH, self.height))
		self.image.fill(pygame.Color(system.WEAPON_COLOR))
		self.rect.y -= system.WEAPON_SPEED
		if self.rect.top < 0:
			self.kill()
		self.rect.inflate_ip(0,system.WEAPON_SPEED)
