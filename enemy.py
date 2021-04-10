import pygame
import system
import random
import enemy_weapon
import utility

image_dir = system.IMAGES_FOLDER+"enemy/"
image_enemy_cut_ratio = (0.34,0.04)
images_enemy = utility.load_images_by_dir_right(image_dir)
images_enemy_len = len(images_enemy[0])

class Enemy(pygame.sprite.Sprite):
	def __init__(self, all_sprites, enemy_sprites, enemy_bullet_sprites, player):
		pygame.sprite.Sprite.__init__(self)
		self.all_sprites = all_sprites
		self.enemy_bullet_sprites = enemy_bullet_sprites
		self.position = random.choice([0, 1])
		self.y = -100
		if self.position == 1:
			self.image = images_enemy[1][0]
			self.mask = pygame.mask.from_surface(self.image)
			self.rect = self.image.get_rect()
			self.rect.x = 0
		elif self.position == 0:
			self.image = images_enemy[0][0]
			self.mask = pygame.mask.from_surface(self.image)
			self.rect = self.image.get_rect()
			self.rect.x = system.WIN_WIDTH-self.mask.get_size()[0]
		self.width, self.height = self.image.get_size()
		self.hor_offset = int(self.width*image_enemy_cut_ratio[0])
		self.ver_offset = int(self.height*image_enemy_cut_ratio[1])
		self.speed_y = random.randrange(1, 8)
		self.stop_position = random.randrange(0, system.WIN_HEIGHT-system.ENEMY_HEIGHT)
		self.stopped = False
		self.kill_flag = self.two_enemy_in_one_stop_position(enemy_sprites, self.stop_position)
		self.last_update = pygame.time.get_ticks()
		self.number_of_bullets = 4 
		self.image_counter = 0
		self.is_last_attack_frame = False
		self.player = player

	def update(self):
		if self.kill_flag:
			self.kill()
		self.rect.y += self.speed_y
		if self.rect.top > self.stop_position:
			self.rect.top = self.stop_position
			self.speed_y = 0
			self.stopped = True
		if self.stopped:
			now = pygame.time.get_ticks()
			if now - self.last_update > system.ENEMY_WEAPON_COOLDOWN and self.number_of_bullets > 0:
				self.start_shoot_animation()
				if self.is_last_attack_frame:
					self.image_counter = 0
					self.last_update = now 
					self.number_of_bullets -= 1
					self.shoot() 	

	def two_enemy_in_one_stop_position(self, enemy_sprites, stop_position):
		for enemy in enemy_sprites:
			if self.stop_position in range(enemy.stop_position-system.ENEMY_HEIGHT, enemy.stop_position+system.ENEMY_HEIGHT) and self.position == enemy.position:
				return True
		return False


	def shoot(self):
		bullet = enemy_weapon.EnemyWeapon(self.position, self.rect.centery, self.width-self.hor_offset, self.player.get_player_information())
		self.all_sprites.add(bullet)
		self.enemy_bullet_sprites.add(bullet)

	def start_shoot_animation(self):
		self.is_last_attack_frame = False
		self.image_counter +=1*system.ENEMY_ANIMATION_SPEED_ATTACK
		im_counter = int(self.image_counter)%images_enemy_len
		self.image = images_enemy[self.position][im_counter]
		self.mask = pygame.mask.from_surface(self.image)
		if im_counter==images_enemy_len-1:
			self.is_last_attack_frame= True		