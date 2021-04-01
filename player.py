import pygame
import system
import weapon

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((system.PLAYER_WIDTH, system.PLAYER_HEIGHT))
        self.image.fill(pygame.Color(system.PLAYER_COLOR))
        self.rect = pygame.Rect(x, y, system.PLAYER_WIDTH, system.PLAYER_HEIGHT)
        self.speed_x = 0
        self.speed_y = 0
        self.start_x = x
        self.start_y = y
        self.rect.x = x
        self.rect.y = y
        self.on_ground = False

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            if self.on_ground:
                self.speed_y = -system.PLAYER_JUMP
        if keystate[pygame.K_LEFT]:
            self.speed_x = -system.PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speed_x = system.PLAYER_SPEED
        if not self.on_ground:
            self.speed_y += system.GRAVITY
        self.on_ground = False     
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.crossing()

    def crossing(self):
        if self.rect.right > system.WIN_WIDTH:
            self.rect.right = system.WIN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0
        if self.rect.bottom > system.WIN_HEIGHT:
            self.rect.bottom = system.WIN_HEIGHT
            self.on_ground = True
            self.speed_y = 0  

    def shoot(self, all_sprites, weapon_sprites):
        weapon_x = weapon.Weapon(self.rect.centerx, self.rect.centery)
        all_sprites.add(weapon_x)
        weapon_sprites.add(weapon_x)                      
   
