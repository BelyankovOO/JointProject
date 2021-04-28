#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import os
import locale
import pygame
import pygame_menu
import system
import player
import enemy
from leaderboard import Leaderboard
import enemy_weapon
import cooldown_animation
import utility
import bonuscreater


sound_dir = system.SOUNDS_FOLDER+"background/"
image_dir = system.IMAGES_FOLDER+"cooldown_animation/"
ru = 'locales/ru_RU'
en = 'locales/en_US'

image_cooldown = utility.load_images_by_dir(image_dir)
copy_of_image_cooldown = utility.load_images_by_dir(image_dir)

class Game():
    """Application's main window class
    """
	def __init__(self):
		"""Initialize pygame, create window, add title,
		load settings, and other initializations 
		"""
		pygame.init() # Инициация PyGame, обязательная строчка 
		self.screen = pygame.display.set_mode(system.DISPLAY) # Создаем окошко
		pygame.display.set_caption("NinjaSamurai") # Пишем в шапку
		self.background = pygame.Surface((system.WIN_WIDTH,system.WIN_HEIGHT)) 
		self.background.fill(pygame.Color(system.BACKGROUND_COLOR))
		self.timer = pygame.time.Clock()  
		self.font = pygame.font.SysFont("Arial", 18)
		self.game_state = 'menu'
		self.game_exit = False
		self.leaderboard = Leaderboard()
		try:
			self.background_music = pygame.mixer.music.load(sound_dir+"background.mp3")
			pygame.mixer.music.play(loops=-1)
			self.have_mixer=True
		except(pygame.error):
			self.have_mixer=False
		self.game_control = {}
		self.controlButtons={}
		self.locale={}
		self.load_settings()
		return
		
	def run(self):
		"""Start infinite loop of the application."""
		while (not self.game_exit):
			if self.game_state == 'menu':
				self.menu_loop()
			elif self.game_state == 'setting':
				self.setting_loop()
			elif self.game_state == 'control':
				self.control_loop()
			elif self.game_state == 'locale':
				self.locale_loop()
			elif self.game_state == 'ladder':
				self.leaderboard_loop()
			elif self.game_state == 'game':
				self.game_loop()
			elif self.game_state == 'game_over':
				self.game_over_loop()
			elif self.game_state == 'round_win':
				self.win_loop()
		return
		
	def update_fps(self):
		"""Update value of the fps counter."""
		fps = str(int(self.timer.get_fps()))
		fps_text = self.font.render(fps, 1, pygame.Color("coral"))
		return fps_text
		
	def game_loop(self):
		"""Start infinite loop of a game."""
		all_sprites = pygame.sprite.Group()
		enemys_sprites = pygame.sprite.Group()
		enemy_bullet_sprites = pygame.sprite.Group()
		bonus_sprites = pygame.sprite.Group()
		haduken_sprites = pygame.sprite.Group()

		self.background.fill(pygame.Color(system.BACKGROUND_COLOR))
		hero = player.Player(self.screen, all_sprites, haduken_sprites)

		cooldown_1 = cooldown_animation.CooldownAnimation(image_cooldown[0], copy_of_image_cooldown[0], 3, (system.WIN_WIDTH - 100, 40))
		
		#all_sprites.add(hero)
		r,g,b,_	= pygame.Color(system.BACKGROUND_COLOR)
		for i in range(system.ENEMY_COUNT):
			mob = enemy.Enemy(all_sprites, enemys_sprites, enemy_bullet_sprites, hero)
			all_sprites.add(mob)
			enemys_sprites.add(mob)

		#Bonus
		bonus_creater = bonuscreater.BonusCreater(hero, bonus_sprites)
		
		self.running = True
		self.start_time = pygame.time.get_ticks()
		while self.running and not self.game_exit:
			self.timer.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					self.game_exit = True
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.pause_menu_loop()
			
			if hero.dying:
				r+=10*system.COLOR_FILL_SPEED
				if (r>255):
					r = 255
				g = g*system.COLOR_FILL_SPEED
				b = b*system.COLOR_FILL_SPEED
				self.background.fill((r,g,b))
			self.screen.blit(self.background, (0,0))
			self.screen.blit(self.update_fps(), (10,0))

			bonus_creater.create_bonus()

			hero.update(self.game_control)
			bonus_sprites.update()
			all_sprites.update()
			cooldown_1.update()
      
			cooldown_1.draw(self.screen)
			bonus_creater.draw(self.screen)
			all_sprites.draw(self.screen)
      
			if hero.drawable:
				self.screen.blit(hero.image, hero.rect)
			pygame.display.update()
			
			hero_bullets_hits = pygame.sprite.spritecollide(hero, enemy_bullet_sprites, False, collided=pygame.sprite.collide_mask)
			enemy_hits = pygame.sprite.groupcollide(enemys_sprites, enemy_bullet_sprites, False, False, collided=pygame.sprite.collide_mask)
			hero_bonus_hits = pygame.sprite.spritecollide(hero, bonus_sprites, False, collided=pygame.sprite.collide_mask)
			haduken_hits = pygame.sprite.groupcollide(enemys_sprites, haduken_sprites, True, True, collided=pygame.sprite.collide_mask)
			if enemy_hits:
				for nindja in enemy_hits.keys():
					for bullet in enemy_hits[nindja]:
						if not bullet.can_damage:
							bullet.kill()
							nindja.kill()

			if hero_bullets_hits:
				if hero.is_reflecting or hero.have_InvulnerableBonus:
					for bullet in hero_bullets_hits :
						if bullet.can_damage:
							bullet.reflect_direction(hero.getCenter())
							bullet.on_hit()
				elif not hero.isInvulnerable():
					for bullet in hero_bullets_hits :
						if bullet.can_damage:
							hero.getDamage()
							bullet.kill()

			if hero_bonus_hits:
				for one_bonus in hero_bonus_hits:
					one_bonus.take_bonus()

			if not hero.isAlive():
				self.running = False
				self.game_state='game_over'
				break

			if len(enemys_sprites) == 0:
				self.running = False
				self.end_time = pygame.time.get_ticks()
				self.game_time = (self.end_time - self.start_time) / 1000
				self.game_state = 'round_win'
				break
			
		return
	
	def menu_loop(self):
		"""Main menu loop."""
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu('NinjaSamurai', w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button(self.locale['Play'], self.start_the_game)
		self.menu.add.button(self.locale['Setting'], self.start_setting)
		self.menu.add.button(self.locale['Leaderboard'], self.start_ladder)
		self.menu.add.button(self.locale['Quit'], self.set_game_exit)
		self.menu.mainloop(self.screen)
		return

	def load_settings(self):
		"""Load settings from 'profile' file. If the file does not exist,
		then create new with default values.
        """
		if os.path.isfile('profile'):
			file = open('profile')
			lines = file.readlines()
			self.difficulty=int(lines[0].strip())
			self.sound_in = bool(int(lines[1].strip()))
			self.sound_level = float(lines[2].strip())
			if self.have_mixer:
				if self.sound_in:
					pygame.mixer.music.set_volume(self.sound_level)
				else:
					pygame.mixer.music.set_volume(0.0)
			self.game_control['Left'] = pygame.key.key_code(lines[3].strip())
			self.game_control['Right'] = pygame.key.key_code(lines[4].strip())
			self.game_control['Up'] = pygame.key.key_code(lines[5].strip())
			self.game_control['Down'] = pygame.key.key_code(lines[6].strip())
			self.game_control['Space'] = pygame.key.key_code(lines[7].strip())
			# language = lines[8].strip()
			self.language = lines[8].strip()
			self.load_locale()
			file.close()
		else:
			file = open('profile','w')
			file.write("1\n1\n0.02\nleft\nright\nup\ndown\nspace\nlocale\n")
			file.close()
			self.load_settings()
		return
	
	def load_locale(self):
		"""Load localization's strings depending on the current settings."""
		if (self.language=='locale'):
			default, _ = locale.getdefaultlocale()
			if default=='ru_RU':
				language = default
			else:
				language = 'en_US'
		else:
			language = self.language
		
		src_language=open(en,'r')
		if language=='ru_RU':
			file=open(ru,'r', encoding='utf-8')
		else:
			file=open(en,'r')
		
		for element in src_language.readlines():
			line = element.strip()
			self.locale[line] = file.readline().strip()
		file.close()
		src_language.close()
		
	def save_settings_to_file(self):
		"""Save the current settings to the 'profile' file."""
		file = open('profile','w')
		file.write(str(self.difficulty)+'\n')
		file.write(str(int(self.sound_in))+'\n')
		file.write(str(self.sound_level)+'\n')
		file.write(pygame.key.name(self.game_control['Left'])+'\n')
		file.write(pygame.key.name(self.game_control['Right'])+'\n')
		file.write(pygame.key.name(self.game_control['Up'])+'\n')
		file.write(pygame.key.name(self.game_control['Down'])+'\n')
		file.write(pygame.key.name(self.game_control['Space'])+'\n')
		file.write(self.language+'\n')
		file.close()
		return
	
	def save_setting(self):
		"""Save selected values in the main settings menu and 
		reload them. After saving it leaves that menu.
        """
		data = self.menu.get_input_data()
		self.difficulty = data['difficulty'][1]
		self.save_settings_to_file()
		self.load_settings()
		self.exit_to_main_menu()
		return

	def change_sound(self, *kwargs):
		"""Invert state of sound."""
		self.sound_in = not self.sound_in
		return

	def make_default_value(self):
		"""Revert values in main settings to default ones."""
		self.sound_in = True
		self.difficulty = 1
		self.sound_switch.set_default_value(self.sound_in)
		self.difficulty_selector.set_default_value(self.difficulty)
		self.menu.reset_value()
		return

	def setting_loop(self):
		"""Main settings loop."""
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(self.locale['Setting'], w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button(self.locale['Control'], self.start_control)
		self.menu.add.button(self.locale['Language'], self.start_locale)
		items = [(self.locale['Easy'], self.locale['EASY']), (self.locale['Medium'], self.locale['MEDIUM']), (self.locale['Hard'], self.locale['HARD'])]
		self.difficulty_selector = self.menu.add.selector( self.locale['Select difficulty']+':\t', items, selector_id='difficulty', default=self.difficulty)
		
		self.sound_switch = self.menu.add.toggle_switch(self.locale['Sound'], self.sound_in, onchange=self.change_sound, toggleswitch_id='sound_in_id')
		self.menu.add.button(self.locale['Save'], self.save_setting)
		self.menu.add.button(self.locale['Default'], self.make_default_value)
		self.menu.add.button(self.locale['Back'], self.exit_to_main_menu)
		self.menu.mainloop(self.screen)
		return
	
	def locale_loop(self):
		"""Language selection loop."""
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(self.locale['Language'], w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button(self.locale['local'], self.change_local)
		self.menu.add.button('English', self.change_en_US)
		self.menu.add.button('Русский', self.change_ru_RU)
		self.menu.add.button(self.locale['Back'], self.start_setting)
		self.menu.mainloop(self.screen)
	
	def change_local(self):
		"""Change the language to be selected by current environment locale."""
		self.language='local'
		self.save_settings_to_file()
		self.load_settings()
		self.start_setting()
	
	def change_ru_RU(self):
		"""Change the language to Russian"""
		self.language='ru_RU'
		self.save_settings_to_file()
		self.load_settings()
		self.start_setting()
		
	def change_en_US(self):
		"""Change the language to English"""
		self.language='en_US'
		self.save_settings_to_file()
		self.load_settings()
		self.start_setting()
	
	def save_control(self):
		"""Save and reload the control changes. After that it leaves
		to main settings menu."""
		self.save_settings_to_file()
		self.load_settings()
		self.start_setting()
		return

	def default_control(self):
		"""Set the control buttons to default ones."""
		self.game_control['Left'] = pygame.key.key_code('left')
		self.controlButtons['Left']._title = 'left'
		self.game_control['Right'] = pygame.key.key_code('right')
		self.controlButtons['Right']._title = 'right'
		self.game_control['Up'] = pygame.key.key_code('up')
		self.controlButtons['Up']._title = 'up'
		self.game_control['Down'] = pygame.key.key_code('down')
		self.controlButtons['Down']._title = 'down'
		self.game_control['Space'] = pygame.key.key_code('space')
		self.controlButtons['Space']._title = 'space'
		return
	
	def control_up(self):
		"""Set the jump control button."""
		ok = True
		while ok:
			events = pygame.event.get();
			for event in events:
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						ok = False
						break
					self.controlButtons['Up']._title = pygame.key.name(event.key)
					self.game_control['Up'] = event.key
					ok = False
					break
		return
	
	def control_down(self):
		"""Set the charge control button."""
		ok = True
		while ok:
			events = pygame.event.get();
			for event in events:
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						ok = False
						break
					self.controlButtons['Down']._title = pygame.key.name(event.key)
					self.game_control['Down'] = event.key
					ok = False
					break
		return
	
	def control_left(self):
		"""Set the left run control button."""
		ok = True
		while ok:
			events = pygame.event.get();
			for event in events:
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						ok = False
						break
					self.controlButtons['Left']._title = pygame.key.name(event.key)
					self.game_control['Left'] = event.key
					ok = False
					break
		return
	
	def control_right(self):
		"""Set the right run control button."""
		ok = True
		while ok:
			events = pygame.event.get();
			for event in events:
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						ok = False
						break
					self.controlButtons['Right']._title = pygame.key.name(event.key)
					self.game_control['Right'] = event.key
					ok = False
					break
		return
	
	def control_space(self):
		"""Set the attack control button."""
		ok = True
		while ok:
			events = pygame.event.get();
			for event in events:
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						ok = False
						break
					self.controlButtons['Space']._title = pygame.key.name(event.key)
					self.game_control['Space'] = event.key
					ok = False
					break
		return
		
	def control_loop(self):
		"""Control change menu loop."""
		w, h = pygame.display.get_surface().get_size()
		
		self.menu = pygame_menu.Menu(self.locale['Control'], w, h, theme=pygame_menu.themes.THEME_SOLARIZED, columns=3, rows=5)
		self.menu.add.label(self.locale['Run left']+':')
		self.menu.add.label(self.locale['Run right']+':')
		self.menu.add.label(self.locale['Jump']+':')
		self.menu.add.label(self.locale['Charge']+':')
		self.menu.add.label(self.locale['Attack']+':')
		
		self.controlButtons['Left']=self.menu.add.button(pygame.key.name(self.game_control['Left']), self.control_left)
		self.controlButtons['Right']=self.menu.add.button(pygame.key.name(self.game_control['Right']), self.control_right)
		self.controlButtons['Up']=self.menu.add.button(pygame.key.name(self.game_control['Up']), self.control_up)
		self.controlButtons['Down']=self.menu.add.button(pygame.key.name(self.game_control['Down']), self.control_down)
		self.controlButtons['Space']=self.menu.add.button(pygame.key.name(self.game_control['Space']), self.control_space)
		
		self.menu.add.button(self.locale['Save'], self.save_control)
		self.menu.add.button(self.locale['Default'], self.default_control)
		self.menu.add.button(self.locale['Back'], self.start_setting)
		self.menu.mainloop(self.screen)
		return

	def game_over_loop(self):
		"""Game over menu loop."""
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(self.locale['Game OVER'], w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button(self.locale['Restart'], self.start_the_game)
		self.menu.add.button(self.locale['Go to main menu'], self.exit_to_main_menu)
		self.menu.add.button(self.locale['Quit'], self.set_game_exit)
		self.menu.mainloop(self.screen)
		return

	def save_best_score(self, current_text):
		"""Save new score to the leaderboard"""
		self.leaderboard.save_score(current_text, self.game_time)

	def win_loop(self):
		"""Win menu loop."""
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(self.locale['YOU WIN']+'! '+self.locale['YOUR TIME']+': '+f'{int(self.game_time // 60)}.{round(self.game_time % 60)} '
									 +self.locale['minutes'], w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add_text_input('Name'+' :', maxchar=10, onreturn=self.save_best_score, input_underline_len=20)
		# print(self.menu.get_value())
		self.menu.add.button(self.locale['Restart'], self.start_the_game)
		self.menu.add.button(self.locale['Leaderboard'], self.leaderboard_loop)
		self.menu.add.button(self.locale['Go to main menu'], self.exit_to_main_menu)
		self.menu.add.button(self.locale['Quit'], self.set_game_exit)
		self.menu.mainloop(self.screen)

		return

	def leaderboard_loop(self):
		"""Leaderboard menu loop."""
		w, h = pygame.display.get_surface().get_size()
		self.menu.disable()
		self.menu = pygame_menu.Menu(self.locale['LEADERBOARD'], w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		table = self.menu.add.table(table_id='LEADERBOARD', font_size=20, font_name='century gothic')
		self.leaderboard.add_leader_table(table)
		self.menu.add.button(self.locale['Go to main menu'], self.exit_to_main_menu)
		self.menu.add.button(self.locale['Quit'], self.set_game_exit)
		self.menu.mainloop(self.screen)
		return
	
	def pause_menu_loop(self):
		"""In game pause menu loop."""
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(self.locale['Pause'], w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button(self.locale['Resume'], self.menu.disable)
		self.menu.add.button(self.locale['Restart'], self.start_the_game)
		self.menu.add.button(self.locale['Go to main menu'], self.exit_to_main_menu)
		self.menu.add.button(self.locale['Quit'], self.set_game_exit)
		self.menu.mainloop(self.screen)
	
	def start_the_game(self):
		"""Start game loop"""
		self.running = False
		self.game_state='game'
		self.menu.disable()
		return

	def start_setting(self):
		"""Start main settings loop"""
		self.running = False
		self.game_state = 'setting'
		self.load_settings()
		self.menu.disable()
		return

	def start_control(self):
		"""Start the control change loop"""
		self.running = False
		self.game_state = 'control'
		self.load_settings()
		self.menu.disable()
		return
		
	def start_ladder(self):
		"""Start the leaderboard loop"""
		self.running = False
		self.game_state = 'ladder'
		self.load_settings()
		self.menu.disable()
		return
		
	def set_game_exit(self):
		"""Stop application"""
		self.running = False
		self.game_exit=True
		self.menu.disable()
		return
	
	def start_locale(self):
		"""Start the localization loop"""
		self.running = False
		self.game_state = 'locale'
		self.load_settings()
		self.menu.disable()
		return
	
	def exit_to_main_menu(self):
		"""Start the main menu loop"""
		self.running = False
		self.game_state='menu'
		self.load_settings()
		self.menu.disable()
		return
	
if __name__ == "__main__":
	game = Game()
	game.run()
