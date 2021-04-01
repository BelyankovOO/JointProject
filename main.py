#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import system
import player
import enemy
import weapon

def main():
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(system.DISPLAY) # Создаем окошко
    pygame.display.set_caption("JointProject") # Пишем в шапку
    background = pygame.Surface((system.WIN_WIDTH,system.WIN_HEIGHT)) 
    background.fill(pygame.Color(system.BACKGROUND_COLOR))

    all_sprites = pygame.sprite.Group()
    weapons_sprites = pygame.sprite.Group()
    enemys_sprites = pygame.sprite.Group()    
    
    hero = player.Player(55,55) # создаем героя по (x,y) координатам
    all_sprites.add(hero)
   
    for i in range(4):
        mob = enemy.Enemy()
        all_sprites.add(mob)
        enemys_sprites.add(mob)
                
    timer = pygame.time.Clock()  
    
    running = True
    while running:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    hero.shoot(all_sprites, weapons_sprites)

        screen.blit(background, (0,0)) # Каждую итерацию необходимо всё перерисовывать
          
        all_sprites.update()

        weapons_hits = pygame.sprite.groupcollide(enemys_sprites, weapons_sprites, True, False)
        for hit in weapons_hits:
            mob = enemy.Enemy()
            all_sprites.add(mob)
            enemys_sprites.add(mob)

        hero_bullets_hits = pygame.sprite.spritecollide(hero, enemys_sprites, False)
        
        if hero_bullets_hits :
            if hero.isReflecting():
                for bullet in hero_bullets_hits :
                    bullet.reflect_direction(hero.getCenter())
            else: #закоментить что не было конца игры
                running = False

        all_sprites.draw(screen)

        pygame.display.update() # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    main()
