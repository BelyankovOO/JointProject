import math
import os

import pygame

import lives
import system
import utility
import weapon

image_dir = system.IMAGES_FOLDER+"hero/"
image_hero_cut_ratio = (0.09,0.12)
images_idle    = utility.load_images_by_dir_right(image_dir+"Martial/"+"Idle/")
images_idle_len = len(images_idle[0])
images_run = utility.load_images_by_dir_right(image_dir+"Martial/"+"Run/")
images_run_len = len(images_run[0])
images_attack  = utility.load_images_by_dir_right(image_dir+"Martial/"+"Attack1/")
images_attack_len = len(images_attack[0])
images_jump  = utility.load_images_by_dir_right(image_dir+"Martial/"+"Jump/")
images_jump_len = len(images_jump[0])
images_jump  = utility.load_images_by_dir_right(image_dir+"Martial/"+"Jump/")
images_jump_len = len(images_jump[0])
images_fall  = utility.load_images_by_dir_right(image_dir+"Martial/"+"Fall/")
images_fall_len = len(images_fall[0])
images_die  = utility.load_images_by_dir_right(image_dir+"Martial/"+"Death/")
images_die_len = len(images_die[0])

sound_dir = system.SOUNDS_FOLDER+"hero/"

class Player(pygame.sprite.Sprite):
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
		self.image = images_idle[1][0]
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.screen = screen
		self.speed_x = 0
		self.speed_y = 0
		self.start_x =  self.rect.centerx
		self.start_y =  self.rect.centery
		self.on_ground = False
		self.cooldowns = {'reflect_cd': 0 , 'shoot': 0, 'reflect_time' : 0, 'invulnerable_time': 0, 'hit_image_swap':0, 'sound_run_cd': 0}
		self.timer_last = pygame.time.get_ticks()
		self.delta_time = 0
		self.lives = lives.Lives()
		self.invulnerability = False
		self.width, self.height = self.image.get_size()
		self.hor_offset = int(self.width * image_hero_cut_ratio[0])
		self.ver_offset = int(self.height * image_hero_cut_ratio[1])
		self.direction = 1  # 0 -- left  ; 1 -- right
		self.image_counter = 0
		self.curr_state = 'idle'
		self.prev_state = 'idle'
		self.is_reflecting = False
		self.have_InvulnerableBonus = False
		self.is_last_attack_frame = False
		self.drawable = True
		self.dead = False
		self.dying = False
		print(os.getcwd(), sound_dir)

		self.sound_sword_hit = pygame.mixer.Sound(os.path.join(sound_dir, "sword_hit.flac"))
		self.sound_jump = pygame.mixer.Sound(sound_dir + "jump.ogg")
		self.sound_hurt = pygame.mixer.Sound(sound_dir + "hurt.wav")
		self.sound_step = pygame.mixer.Sound(sound_dir + "step.ogg")

	def update(self):
		if (not self.dying):
			self.speed_x = 0
			self.lives.draw(self.screen)
			keystate = pygame.key.get_pressed()
			now = pygame.time.get_ticks()
			self.delta_time = now - self.timer_last;
			self.timer_last = now
			# tick cooldowns
			utility.cooldown_tick(self.cooldowns, self.delta_time, {'hit_image_swap': self.hit_image_swap})
			# END InvulnerableBonus
			if self.have_InvulnerableBonus and not self.isInvulnerable():
				self.have_InvulnerableBonus = False
			if not self.is_reflecting:
				if not (keystate[pygame.K_LEFT] and keystate[pygame.K_RIGHT]):
					if keystate[pygame.K_LEFT]:
						self.speed_x = -system.PLAYER_SPEED
						self.curr_state = 'run'
						self.direction = 0
					if keystate[pygame.K_RIGHT]:
						self.speed_x = system.PLAYER_SPEED
						self.curr_state = 'run'
						self.direction = 1
					if not keystate[pygame.K_LEFT] and not keystate[pygame.K_RIGHT]:
						self.curr_state = 'idle'
				else:	
					self.curr_state = 'idle'
				if keystate[pygame.K_UP]:
					if self.on_ground:
						self.on_ground = False
						self.speed_y = -system.PLAYER_JUMP
						self.curr_state = 'jump'
						self.sound_jump.play()
						
				if keystate[pygame.K_SPACE] and self.cooldowns['reflect_cd']==0:
					self.curr_state='attack'
					self.is_reflecting = True
					self.sound_sword_hit.play()
					self.reflect()
			if not self.on_ground:
				self.speed_y += system.GRAVITY  
			self.rect.centerx  += self.speed_x
			self.rect.centery  += self.speed_y
			self.crossing()
			if self.is_last_attack_frame:
				self.is_reflecting = False
			self.update_image()
		else:
			self.curr_state = 'dying'
			self.update_image()
		self.prev_state = self.curr_state

	def crossing(self):
		bottom = self.rect.centery+self.ver_offset
		top = self.rect.centery-self.ver_offset
		left = self.rect.centerx-self.hor_offset
		right = self.rect.centerx+self.hor_offset
		if right > system.WIN_WIDTH:
			self.rect.centerx = system.WIN_WIDTH-self.hor_offset
		if left < 0:
			self.rect.centerx = 0+self.hor_offset
		if top < 0:
			self.rect.centery = 0+self.ver_offset
			self.speed_y = 0

		if bottom > system.WIN_HEIGHT:
			self.rect.centery = system.WIN_HEIGHT-self.ver_offset
			self.on_ground = True
			self.speed_y = 0  

	def shoot(self, all_sprites, weapon_sprites):
		if (self.cooldowns['shoot']==0):
			weapon_x = weapon.Weapon(self.rect.centerx, self.rect.centery)
			all_sprites.add(weapon_x)
			weapon_sprites.add(weapon_x)      
			self.cooldowns['shoot']=system.PLAYER_SHOOT_CD 

	def reflect(self):
		if (self.cooldowns['reflect_cd']==0):
			self.cooldowns['reflect_cd']=system.PLAYER_REFLECT_CD
	
	def update_image(self):
		if self.prev_state!=self.curr_state:
			self.image_counter = 0
		self.is_last_attack_frame = False

		if not self.dying:
			if not self.on_ground and not self.curr_state=='attack':
				self.image_counter +=1*system.PLAYER_ANIMATION_SPEED_AIR
				im_counter = int(self.image_counter)%images_fall_len
				if self.speed_y>=0:
					self.image = images_fall[self.direction][im_counter]
				else:
					self.image = images_jump[self.direction][im_counter]
				self.mask = pygame.mask.from_surface(self.image)
			else:
				if self.curr_state=='run':
					self.image_counter +=1*system.PLAYER_ANIMATION_SPEED_RUN
					im_counter = int(self.image_counter)%images_run_len
					self.image = images_run[self.direction][im_counter]
					self.mask = pygame.mask.from_surface(self.image)
					if self.cooldowns['sound_run_cd'] == 0:
						self.sound_step.play()
						self.cooldowns['sound_run_cd'] = system.SOUND_RUN_CD
				if self.curr_state=='attack':
					self.image_counter +=1*system.PLAYER_ANIMATION_SPEED_ATTACK
					im_counter = int(self.image_counter)%images_attack_len
					self.image = images_attack[self.direction][im_counter]
					self.mask = pygame.mask.from_surface(self.image)
					if im_counter==images_attack_len-1:
						self.is_last_attack_frame= True
				if self.curr_state=='idle':
					self.image_counter +=1*system.PLAYER_ANIMATION_SPEED_IDLE
					im_counter = int(self.image_counter)%images_idle_len
					self.image = images_idle[self.direction][im_counter]
					self.mask = pygame.mask.from_surface(self.image)
		else:
			self.image_counter += 1 * system.PLAYER_ANIMATION_SPEED_DIE
			im_counter = math.floor(self.image_counter)
			if im_counter >= images_die_len:
				im_counter = images_die_len - 1
			self.image = images_die[self.direction][im_counter]
			self.mask = pygame.mask.from_surface(self.image)
			if self.image_counter > images_die_len + 15:
				self.dead = True

	def invulnerable(self):
		# self.image = image_invulnerable
		self.mask = pygame.mask.from_surface(self.image)
		self.cooldowns['invulnerable_time'] = system.PLAYER_INVULNERABLE_TIME
		self.cooldowns['hit_image_swap'] = system.PLAYER_ANIMATION_FLICKER_ROTATION
		self.sound_hurt.play()
		self.drawable = False

	def isInvulnerable(self):
		return self.cooldowns['invulnerable_time'] > 0

	def isAlive(self):
		return not self.dead	
			
	def hit_image_swap(self):
		if self.cooldowns['invulnerable_time']>0:
			self.drawable = not self.drawable
			self.cooldowns['hit_image_swap'] = system.PLAYER_ANIMATION_FLICKER_ROTATION
		else:
			self.drawable=True
	
	def getCenter(self):
		return (self.rect.centerx, self.rect.centery+1.2*self.ver_offset)

	def getDamage(self):
		self.lives.decrease_number_of_lives()
		if not self.dying:
			if self.lives.check_number_of_of_lives()>0:
				self.invulnerable()
			else: 
				self.dying = True

	def getLifeBonus(self):
		self.lives.increase_number_of_lives()

	def getInvulnerableBonus(self):
		self.mask = pygame.mask.from_surface(self.image)
		self.cooldowns['invulnerable_time'] = system.BONUS_INVULNERABLE_TIME
		self.cooldowns['hit_image_swap'] = system.PLAYER_ANIMATION_FLICKER_ROTATION
		self.drawable = False
		self.have_InvulnerableBonus = True
