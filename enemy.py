import pygame
import system
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((system.ENEMY_WIDTH, system.ENEMY_HEIGHT))
        self.image.fill(pygame.Color(system.ENEMY_COLOR))
        self.x = random.randrange(system.WIN_WIDTH - system.ENEMY_WIDTH)
        self.y = random.randrange(0+system.ENEMY_HEIGHT, system.WIN_HEIGHT-system.ENEMY_HEIGHT)
        self.rect = pygame.Rect(self.x, self.y, system.ENEMY_WIDTH, system.ENEMY_HEIGHT)
        self.speed_x = random.randrange(-8, 8)
        self.speed_y = random.randrange(-8, 8) 

    def update(self):
        self.crossing()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def crossing(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y
        if self.rect.bottom > system.WIN_HEIGHT:
            self.rect.bottom = system.WIN_HEIGHT
            self.speed_y = -self.speed_y
        if self.rect.right < 0:
            self.rect.right = 0
            self.speed_x = -self.speed_x
        if self.rect.left > system.WIN_WIDTH:
            self.rect.left = system.WIN_WIDTH
            self.speed_x = -self.speed_x             


    #def draw(self, screen):
     #   screen.blit(self.image, (self.rect.x, self.rect.y))      


