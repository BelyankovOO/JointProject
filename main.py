#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import pygame_menu
import system
import player
import enemy
import weapon
import enemy_weapon

sound_dir = system.SOUNDS_FOLDER+"background/"

class Game():
	def __init__(self):
		pygame.init() # Инициация PyGame, обязательная строчка 
		self.screen = pygame.display.set_mode(system.DISPLAY) # Создаем окошко
		pygame.display.set_caption("JointProject") # Пишем в шапку
		self.background = pygame.Surface((system.WIN_WIDTH,system.WIN_HEIGHT)) 
		self.background.fill(pygame.Color(system.BACKGROUND_COLOR))
		self.timer = pygame.time.Clock()  
		self.font = pygame.font.SysFont("Arial", 18)
		self.game_states = ['menu','game','game_over']
		self.game_state = 'menu'
		self.game_exit = False
		self.background_music = pygame.mixer.music.load(sound_dir+"background.mp3")
		pygame.mixer.music.set_volume(0.02)
		return
		
	def run(self):
		while (not self.game_exit):
			if self.game_state=='menu':
				self.menu_loop()
			elif self.game_state=='game':
				self.game_loop()
			elif self.game_state=='game_over':
				self.game_over_loop()
		return
		
	def update_fps(self):
		fps = str(int(self.timer.get_fps()))
		fps_text = self.font.render(fps, 1, pygame.Color("coral"))
		return fps_text
		
	def game_loop(self):
		all_sprites = pygame.sprite.Group()
		#weapons_sprites = pygame.sprite.Group()
		enemys_sprites = pygame.sprite.Group()
		enemy_bullet_sprites = pygame.sprite.Group()    
		self.background.fill(pygame.Color(system.BACKGROUND_COLOR))
		hero = player.Player(self.screen)
		#all_sprites.add(hero)
		r,g,b,_	= pygame.Color(system.BACKGROUND_COLOR)
		for i in range(4):
			mob = enemy.Enemy(all_sprites, enemys_sprites, enemy_bullet_sprites)
			all_sprites.add(mob)
			enemys_sprites.add(mob)

		pygame.mixer.music.play(loops=-1)	
		
		self.running = True
		
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
			
			hero.update()
			all_sprites.update()
			
			all_sprites.draw(self.screen)
			if hero.drawable:
				self.screen.blit(hero.image, hero.rect)
			pygame.display.update()
			
			hero_bullets_hits = pygame.sprite.spritecollide(hero, enemy_bullet_sprites, False, collided=pygame.sprite.collide_mask)

			if hero_bullets_hits:
				if hero.is_reflecting:
					for bullet in hero_bullets_hits :
						if bullet.can_damage:
							bullet.reflect_direction(hero.getCenter())
							bullet.on_hit()
				elif not hero.isInvulnerable():
					for bullet in hero_bullets_hits :
						if bullet.can_damage:
							hero.getDamage()
							bullet.kill()

			if not hero.isAlive():
				self.running = False
				self.game_state='game_over'
				break	
			
		return

	def menu_loop(self):
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(h, w, 'Hi', theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button('Play', self.start_the_game)
		self.menu.add.button('Quit', self.set_game_exit)
		self.menu.mainloop(self.screen)
		return
	
	def game_over_loop(self):
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(h, w, 'Game OVER', theme=pygame_menu.themes.THEME_SOLARIZED)
		self.menu.add.button('Restart', self.start_the_game)
		self.menu.add.button('Go to main menu', self.exit_to_main_menu)
		self.menu.add.button('Quit', self.set_game_exit)
		self.menu.mainloop(self.screen)
		return
	
	def pause_menu_loop(self):
		w, h = pygame.display.get_surface().get_size()
		self.menu = pygame_menu.Menu(h, w, 'Pause', theme=pygame_menu.themes.THEME_SOLARIZED)
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
	
	def set_game_exit(self):
		self.running = False
		self.game_exit=True
		self.menu.disable()
		return
	
	def exit_to_main_menu(self):
		self.running = False
		self.game_state='menu'
		self.menu.disable()
		return
	
if __name__ == "__main__":
	game = Game()
	game.run()
