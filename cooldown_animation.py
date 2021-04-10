import pygame
import system
import math

class CooldownAnimation(pygame.sprite.Sprite):
	def __init__(self, image, cooldown_time, position_on_screen):
		pygame.sprite.Sprite.__init__(self)
		self.cooldown_ticks_in_angle = 360 / cooldown_time
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = position_on_screen[0]
		self.rect.y = position_on_screen[1]
		self.alpha = 90
		#pygame.draw.line(self.image, ((0,0,0)), (self.rect.width/2, self.rect.height/2), (self.rect.width/2, 0), 2)
		pygame.draw.polygon(self.image, (0,0,0), [(self.rect.width/2, self.rect.height/2), (self.rect.width/2, 0), (self.rect.width/2+1, 0)])
		self.cooldown_time = cooldown_time
		self.angle_1 = 60
		self.x_moving = self.rect.width/2
		self.y_moving = 0

	def update(self):
		#pygame.draw.line(self.image, ((0,0,0)), (self.rect.width/2, self.rect.height/2), (self.get_x_coordinate(self.rect.width/2, self.angle_1), self.get_y_coordinate(self.rect.height/2, self.angle_1)), 2)
		#if self.x_moving <= self.rect.width:
		#	pygame.draw.polygon(self.image, (0,0,0), [(self.rect.width/2, self.rect.height/2), (self.rect.width/2, 0), (self.x_moving, 0)])
		#	self.x_moving += 1
		#elif self.y_moving <= self.rect.height:
		#	pygame.draw.polygon(self.image, (0,0,0), [(self.rect.width/2, self.rect.height/2), (self.rect.width/2, 0), (self.x_moving, 0), (self.x_moving, self.y_moving)])
		#	self.y_moving += 1		

		#print(self.line)
		
	def get_x_coordinate(self, radius, angle):
		return self.rect.width/2 + radius*math.cos(angle*math.pi/180)

	def get_y_coordinate(self, radius, angle):
		return self.rect.height/2 + radius*math.sin(angle*math.pi/180) 	 	
