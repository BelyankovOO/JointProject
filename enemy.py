import pygame
import system
import random
import enemy_weapon

class Enemy(pygame.sprite.Sprite):
	def __init__(self, all_sprites, enemy_sprites, enemy_bullet_sprites):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((system.ENEMY_WIDTH, system.ENEMY_HEIGHT))
		self.image.fill(pygame.Color(system.ENEMY_COLOR))
		self.all_sprites = all_sprites
		self.enemy_bullet_sprites = enemy_bullet_sprites
		self.x = random.choice([0, system.WIN_WIDTH])
		self.y = -100
		if self.x == 0:
			self.rect = pygame.Rect(self.x, self.y, system.ENEMY_WIDTH, system.ENEMY_HEIGHT)
		elif self.x == system.WIN_WIDTH:
			self.rect = pygame.Rect(system.WIN_WIDTH-system.ENEMY_WIDTH, self.y, system.ENEMY_WIDTH, system.ENEMY_HEIGHT)    
		self.speed_y = random.randrange(1, 8)
		self.stop_position = random.randrange(0, system.WIN_HEIGHT-system.ENEMY_HEIGHT)
		self.kill_flag = self.two_enemy_in_one_stop_position(enemy_sprites, self.stop_position)
		self.last_update = pygame.time.get_ticks()
		self.number_of_bullets = 4 

	def update(self):
		if self.kill_flag:
			self.kill()
		now = pygame.time.get_ticks()
		if now - self.last_update > system.ENEMY_WEAPON_COOLDOWN and self.number_of_bullets > 0:
			self.last_update = now
			self.number_of_bullets -= 1
			self.shoot()
		self.rect.y += self.speed_y
		if self.rect.top > self.stop_position:
			self.rect.top = self.stop_position
			self.speed_y = 0

	def two_enemy_in_one_stop_position(self, enemy_sprites, stop_position):
		for enemy in enemy_sprites:
			if self.stop_position in range(enemy.stop_position-system.ENEMY_HEIGHT, enemy.stop_position+system.ENEMY_HEIGHT) and self.x == enemy.x:
				return True
		return False


	def shoot(self):
		bullet = enemy_weapon.EnemyWeapon(self.rect.x, self.rect.centery)
		self.all_sprites.add(bullet)
		self.enemy_bullet_sprites.add(bullet)	



