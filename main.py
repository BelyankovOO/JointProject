#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import os
import pygame
import pygame_menu
import system
import player
import enemy
from leaderboard import Leaderboard
import weapon
import enemy_weapon
import cooldown_animation
import utility
import bonuscreater


sound_dir = system.SOUNDS_FOLDER+"background/"
image_dir = system.IMAGES_FOLDER+"cooldown_animation/"

image_cooldown = utility.load_images_by_dir(image_dir)
copy_of_image_cooldown = utility.load_images_by_dir(image_dir)

class Game():
	def __init__(self):
		pygame.init() # Инициация PyGame, обязательная строчка 
		self.screen = pygame.display.set_mode(system.DISPLAY) # Создаем окошко
		pygame.display.set_caption("JointProject") # Пишем в шапку
		self.background = pygame.Surface((system.WIN_WIDTH,system.WIN_HEIGHT)) 
		self.background.fill(pygame.Color(system.BACKGROUND_COLOR))
		self.timer = pygame.time.Clock()  
		self.font = pygame.font.SysFont("Arial", 18)
		self.game_states = ['menu','game','game_over', 'round_win', 'setting', 'control']
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
		self.load_settings()
		self.sound_in = True
		self.sound_level = 0.02
		self.difficulty = 1
		self.controlButtons={}
		return
		
	def run(self):
		while (not self.game_exit):
			if self.game_state == 'menu':
				self.menu_loop()
			elif self.game_state == 'setting': #rdt
				self.setting_loop()
			elif self.game_state == 'control': #rdt
				self.control_loop()
			elif self.game_state == 'game':
				self.game_loop()
			elif self.game_state == 'game_over':
				self.game_over_loop()
			elif self.game_state == 'round_win':
				self.win_loop()
		return
		
	def update_fps(self):
		fps = str(int(self.timer.get_fps()))
		fps_text = self.font.render(fps, 1, pygame.Color("coral"))
		return fps_text
		
	def game_loop(self):
		all_sprites = pygame.sprite.Group()
		weapons_sprites = pygame.sprite.Group()

		enemys_sprites = pygame.sprite.Group()
		enemy_bullet_sprites = pygame.sprite.Group()
		bonus_sprites = pygame.sprite.Group()
		self.background.fill(pygame.Color(system.BACKGROUND_COLOR))
		hero = player.Player(self.screen)

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
					if event.key == pygame.K_x:
						hero.shoot(all_sprites, weapons_sprites)
					elif event.key == pygame.K_ESCAPE:
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
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu('NinjaSamurai', w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button('Play', self.start_the_game)
		self.menu.add.button('Setting', self.start_setting) #rdt
		self.menu.add.button('Quit', self.set_game_exit)
		self.menu.mainloop(self.screen)
		return

	def load_settings(self):
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
			
			file.close()
		else:
			file = open('profile','w')
			file.write("1\n1\n0.02\nleft\nright\nup\ndown\nspace\n")
			file.close()
			self.load_settings()
	
	def save_settings_to_file(self):
		file = open('profile','w')
		file.write(str(self.difficulty)+'\n')
		file.write(str(int(self.sound_in))+'\n')
		file.write(str(self.sound_level)+'\n')
		file.write(pygame.key.name(self.game_control['Left'])+'\n')
		file.write(pygame.key.name(self.game_control['Right'])+'\n')
		file.write(pygame.key.name(self.game_control['Up'])+'\n')
		file.write(pygame.key.name(self.game_control['Down'])+'\n')
		file.write(pygame.key.name(self.game_control['Space'])+'\n')
		file.close()
		return
	
	def save_setting(self):
		data = self.menu.get_input_data()
		self.difficulty = data['difficulty'][1]
		self.save_settings_to_file()
		self.load_settings()
		self.exit_to_main_menu()
		return

	def change_sound(self, *kwargs):
		self.sound_in = not self.sound_in
		return

	def make_default_value(self):
		self.sound_in = True
		self.difficulty = 1
		self.sound_switch.set_default_value(self.sound_in)
		self.difficulty_selector.set_default_value(self.difficulty)
		self.menu.reset_value()
		return

	def setting_loop(self): #rdt
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu('Setting', w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button('Control', self.start_control)
		items = [('Easy', 'EASY'), ('Medium', 'MEDIUM'), ('Hard', 'HARD')]
		self.difficulty_selector = self.menu.add.selector( 'Select difficulty:\t', items, selector_id='difficulty', default=self.difficulty)
		
		self.sound_switch = self.menu.add.toggle_switch('Sound', self.sound_in, onchange=self.change_sound, toggleswitch_id='sound_in_id')
		self.menu.add.button('Save', self.save_setting)
		self.menu.add.button('Default', self.make_default_value)
		self.menu.add.button('Close', self.exit_to_main_menu)
		self.menu.mainloop(self.screen)
		return

	def save_control(self):
		self.save_settings_to_file()
		self.load_settings()
		self.start_setting()
		return

	def default_control(self):
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
		
	def control_loop(self): #rdt
		w, h = pygame.display.get_surface().get_size()
		
		self.menu = pygame_menu.Menu('Control', w, h, theme=pygame_menu.themes.THEME_SOLARIZED, columns=3, rows=5)
		self.menu.add.label('Run left:')
		self.menu.add.label('Run right:')
		self.menu.add.label('Jump:')
		self.menu.add.label('Charge:')
		self.menu.add.label('Attack:')
		
		self.controlButtons['Left']=self.menu.add.button(pygame.key.name(self.game_control['Left']), self.control_left)
		self.controlButtons['Right']=self.menu.add.button(pygame.key.name(self.game_control['Right']), self.control_right)
		self.controlButtons['Up']=self.menu.add.button(pygame.key.name(self.game_control['Up']), self.control_up)
		self.controlButtons['Down']=self.menu.add.button(pygame.key.name(self.game_control['Down']), self.control_down)
		self.controlButtons['Space']=self.menu.add.button(pygame.key.name(self.game_control['Space']), self.control_space)
		
		self.menu.add.button('Save', self.save_control)
		self.menu.add.button('Default', self.default_control)
		self.menu.add.button('Close', self.start_setting)
		self.menu.mainloop(self.screen)
		return

	def game_over_loop(self):
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu('Game OVER', w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button('Restart', self.start_the_game)
		self.menu.add.button('Go to main menu', self.exit_to_main_menu)
		self.menu.add.button('Quit', self.set_game_exit)
		self.menu.mainloop(self.screen)
		return

	def save_best_score(self, current_text):
		self.leaderboard.save_score(current_text, self.game_time)

	def win_loop(self):
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(f'YOU WIN! YOUR TIME: {int(self.game_time // 60)}.{round(self.game_time % 60)} '
									 f'minutes', w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add_text_input('Name :', maxchar=10, onreturn=self.save_best_score, input_underline_len=20)
		# print(self.menu.get_value())
		self.menu.add.button('Restart', self.start_the_game)
		self.menu.add.button('Leaderboard', self.leaderboard_loop)
		self.menu.add.button('Go to main menu', self.exit_to_main_menu)
		self.menu.add.button('Quit', self.set_game_exit)
		self.menu.mainloop(self.screen)

		return

	def leaderboard_loop(self):
		w, h = pygame.display.get_surface().get_size()
		self.menu.disable()
		self.menu = pygame_menu.Menu(f'LEADERBOARD', w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		table = self.menu.add.table(table_id='LEADERBOARD', font_size=20, font_name='century gothic')
		self.leaderboard.add_leader_table(table)
		self.menu.add.button('Go to main menu', self.exit_to_main_menu)
		self.menu.add.button('Quit', self.set_game_exit)
		self.menu.mainloop(self.screen)
		return
	
	def pause_menu_loop(self):
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu('Pause', w, h, theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button('Resume', self.menu.disable)
		self.menu.add.button('Restart', self.start_the_game)
		self.menu.add.button('Go to main menu', self.exit_to_main_menu)
		self.menu.add.button('Quit', self.set_game_exit)
		self.menu.mainloop(self.screen)
	
	def start_the_game(self):
		self.running = False
		self.game_state='game'
		self.menu.disable()
		return

	def start_setting(self): #rdt
		self.running = False
		self.game_state = 'setting'
		self.load_settings()
		self.menu.disable()
		return

	def start_control(self): #rdt
		self.running = False
		self.game_state = 'control'
		self.load_settings()
		self.menu.disable()
		return

	def set_game_exit(self):
		self.running = False
		self.game_exit=True
		self.menu.disable()
		return
	
	def exit_to_main_menu(self):
		self.running = False
		self.game_state='menu'
		self.load_settings()
		self.menu.disable()
		return
	
if __name__ == "__main__":
	game = Game()
	game.run()
