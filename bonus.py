import pygame
import system
import random
import utility

image_dir = system.IMAGES_FOLDER+"bonus/heart/"
image_bonus_resize = (30,30)
images_bonus = utility.load_images_by_dir_right(image_dir)
images_bonus_len = len(images_bonus[0])

class BonusCreater(object):
	def __init__(self, hero):
		self.last_ticks = pygame.time.get_ticks()
		self.hero = hero

	def need_create_bonus(self):
		seconds_passed = (pygame.time.get_ticks() - self.last_ticks) / 1000
		if seconds_passed > system.SPAWN_BONUS_CD:
			self.last_ticks = pygame.time.get_ticks()
			return True
		else:
			return False

	def create_bonus(self, all_sprites, bonus_sprites):
		if self.need_create_bonus():
			bonus_example = LifeBonus(all_sprites, bonus_sprites, self.hero)
			bonus_sprites.add(bonus_example)
			all_sprites.add(bonus_example)
		else:
			pass

class BonusBase(pygame.sprite.Sprite):
	def __init__(self, all_sprites, bonus_sprites, hero, image):
		pygame.sprite.Sprite.__init__(self)
		self.all_sprites = all_sprites
		self.bonus_sprites = bonus_sprites
		self.hero = hero

		# Load image
		self.image = image
		self.image  = pygame.transform.scale(self.image, image_bonus_resize)
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()

		# Set position
		self.bot_y, self.top_y = 500, 600
		self.left_x, self.right_x = 0, system.WIN_WIDTH - self.image.get_width()
		self.rect.y = random.randint(self.bot_y, self.top_y)
		self.rect.x = random.randint(self.left_x, self.right_x)

		self.is_taken = False
		self.last_update = pygame.time.get_ticks()

	def action(self):
		pass

	def take_bonus(self):
		self.is_taken = True
		self.action()

	def update(self):
		if self.is_taken:
			self.kill()

class LifeBonus(BonusBase):
	def __init__(self, all_sprites, bonus_sprites, hero):
		super().__init__(all_sprites, bonus_sprites, hero, images_bonus[0][0])

	def action(self):
		self.hero.getLifeBonus()
