#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import system
import player
import enemy
import weapon
import enemy_weapon



def main():
	pygame.init() # Инициация PyGame, обязательная строчка 
	screen = pygame.display.set_mode(system.DISPLAY) # Создаем окошко
	pygame.display.set_caption("JointProject") # Пишем в шапку
	background = pygame.Surface((system.WIN_WIDTH,system.WIN_HEIGHT)) 
	background.fill(pygame.Color(system.BACKGROUND_COLOR))
	
	all_sprites = pygame.sprite.Group()
	#weapons_sprites = pygame.sprite.Group()
	enemys_sprites = pygame.sprite.Group()
	enemy_bullet_sprites = pygame.sprite.Group()    
	
	hero = player.Player(55,55)
	all_sprites.add(hero)

	for i in range(4):
		mob = enemy.Enemy(all_sprites, enemys_sprites, enemy_bullet_sprites)
		all_sprites.add(mob)
		enemys_sprites.add(mob)
				
	timer = pygame.time.Clock()  
	
	font = pygame.font.SysFont("Arial", 18)
	def update_fps():
		fps = str(int(timer.get_fps()))
		fps_text = font.render(fps, 1, pygame.Color("coral"))
		return fps_text
	
	running = True
	while running:
		timer.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_x:
					hero.shoot(all_sprites, weapons_sprites)                

		screen.blit(background, (0,0))
		screen.blit(update_fps(), (10,0))
		all_sprites.update()

		hero_bullets_hits = pygame.sprite.spritecollide(hero, enemy_bullet_sprites, False)

		if hero_bullets_hits :
			if hero.isReflecting():
				for bullet in hero_bullets_hits :
					bullet.reflect_direction(hero.getCenter())
			else: 
				running = False

		all_sprites.draw(screen)

		pygame.display.update()
		

if __name__ == "__main__":
	main()
