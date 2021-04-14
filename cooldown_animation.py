import pygame
import system
import math
import copy

class CooldownAnimation():
	def __init__(self, image, copy_of_image, cooldown_time, position_on_screen):
		pygame.sprite.Sprite.__init__(self)
		self.start_image = copy_of_image
		self.image = image
		#self.image.set_alpha(128)
		self.rect = self.image.get_rect()
		self.alpha_surface = pygame.Surface((self.rect.width, self.rect.height))
		self.alpha_surface.set_alpha(128)
		self.full_alpha_surface = pygame.Surface((self.rect.width, self.rect.height))
		self.full_alpha_surface.fill((255,255,255,0))
		self.rect.x = position_on_screen[0]
		self.rect.y = position_on_screen[1]
		self.cooldown_time = cooldown_time
		self.angle_of_rotation = 270
		self.radius = math.ceil(math.sqrt((self.rect.width/2)**2 + (self.rect.height/2)**2))
		self.key_points = [(self.rect.width/2, self.rect.height/2), (self.rect.width/2, self.rect.height/2-self.radius), (self.rect.width/2+1, self.rect.height/2-self.radius)]
		pygame.draw.polygon(self.alpha_surface, (255,255,255), self.key_points)
		self.key_points.pop()
		self.image.blit(self.alpha_surface, (0,0))

	def update(self):
		if self.angle_of_rotation - 360 <= 270:
			self.angle_of_rotation += 1
			self.key_points.append((self.get_x_coordinate(self.radius, self.angle_of_rotation), self.get_y_coordinate(self.radius, self.angle_of_rotation)))
			pygame.draw.polygon(self.alpha_surface, (255,255,255), self.key_points)
			if self.angle_of_rotation - 360 not in [45,135,225,315]:
				self.key_points.pop()
			self.image.blit(self.start_image, (0,0))	
			self.image.blit(self.alpha_surface, (0,0))
		else:
			self.image.blit(self.start_image, (0,0))	
			
	def draw(self, screen):
		screen.blit(self.image, self.rect)				
		
	def get_x_coordinate(self, radius, angle):
		return self.rect.width/2 + radius*math.cos(angle*math.pi/180)

	def get_y_coordinate(self, radius, angle):
		return self.rect.height/2 + radius*math.sin(angle*math.pi/180) 	 	
