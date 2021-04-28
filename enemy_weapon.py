"""JointProject NinjaSamurai."""
import pygame
import system
import math
import utility

images = {'shuriken': [], 'yellow_shuriken': []}
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/shuriken/shuriken0.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/shuriken/shuriken1.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/shuriken/shuriken2.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/shuriken/shuriken3.png"))
images['shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/shuriken/shuriken4.png"))

images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/yellow_shuriken/yellow_shuriken0.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/yellow_shuriken/yellow_shuriken1.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/yellow_shuriken/yellow_shuriken2.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/yellow_shuriken/yellow_shuriken3.png"))
images['yellow_shuriken'].append(pygame.image.load(system.IMAGES_FOLDER + "bullets/yellow_shuriken/yellow_shuriken4.png"))


class EnemyWeapon(pygame.sprite.Sprite):
    """
    Enemy weapon class (suriken).

    :param position: side of screen
    :param y: coordinate of y
    :param enemy_border: border of sprite
    :param player_information: information about player
    """

    def __init__(self, position, y, enemy_border, player_information):
        """Init enemy weapon."""
        pygame.sprite.Sprite.__init__(self)
        self.image = images['shuriken'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        if position == 1:
            norma_vector = utility.vector_normalization((player_information[0] - enemy_border, player_information[1] - y))
            if player_information[2] == 1:
                self.speed_x = math.ceil(norma_vector[0] * system.MAX_ENEMY_WEAPON_SPEED)
                self.speed_y = math.ceil(norma_vector[1] * system.MAX_ENEMY_WEAPON_SPEED)
            elif player_information[2] == 0:
                self.speed_x = math.floor(norma_vector[0] * system.MAX_ENEMY_WEAPON_SPEED)
                self.speed_y = math.floor(norma_vector[1] * system.MAX_ENEMY_WEAPON_SPEED)
            self.rect.right = enemy_border
        elif position == 0:
            norma_vector = utility.vector_normalization((player_information[0] - (system.WIN_WIDTH - enemy_border), player_information[1] - y))
            if player_information[2] == 1:
                self.speed_x = math.ceil(norma_vector[0] * system.MAX_ENEMY_WEAPON_SPEED)
                self.speed_y = math.ceil(norma_vector[1] * system.MAX_ENEMY_WEAPON_SPEED)
            elif player_information[2] == 0:
                self.speed_x = math.floor(norma_vector[0] * system.MAX_ENEMY_WEAPON_SPEED)
                self.speed_y = math.floor(norma_vector[1] * system.MAX_ENEMY_WEAPON_SPEED)
            self.rect.left = system.WIN_WIDTH - enemy_border
        self.start_y = y
        self.rect.centery = y
        self.timer_last = pygame.time.get_ticks()
        self.delta_time = 0
        self.image_num = 0
        self.velocity = math.sqrt(self.speed_x**2 + self.speed_y**2)
        self.can_damage = True
        self.cooldowns = {'can_damage': 0, 'rotation': (system.SHURIKEN_ROTATION / self.velocity)}

    def update(self):
        """Update enemy weapon."""
        now = pygame.time.get_ticks()
        self.delta_time = now - self.timer_last
        self.timer_last = now
        utility.cooldown_tick(self.cooldowns, self.delta_time, {'can_damage': self.reset_can_damage,
                                                                'rotation': self.image_rotation})
        self.crossing()
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

    def crossing(self):
        """Check crossing of suriken and borders of screen."""
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y
            self.can_damage = True
        if self.rect.bottom > system.WIN_HEIGHT:
            self.rect.bottom = system.WIN_HEIGHT
            self.speed_y = -self.speed_y
            self.can_damage = True
        if self.rect.right < 0:
            self.rect.right = 0
            self.speed_x = -self.speed_x
            self.can_damage = True
        if self.rect.left > system.WIN_WIDTH:
            self.rect.left = system.WIN_WIDTH
            self.speed_x = -self.speed_x
            self.can_damage = True

    def reflect_direction(self, colide_point_center):
        """
        Change direction of suriken.

        :param colide_point_center: coordinate of reflected center
        """
        L = [self.speed_x, self.speed_y]
        norm = [self.rect.x - colide_point_center[0], self.rect.y - colide_point_center[1]]
        s_norm = math.sqrt(norm[0]**2 + norm[1]**2)
        s_L = math.sqrt(L[0]**2 + L[1]**2)
        L[0] = L[0] / s_L
        L[1] = L[1] / s_L
        norm[0] = norm[0] / s_norm
        norm[1] = norm[1] / s_norm
        self.speed_x = s_L * norm[0]
        self.speed_y = s_L * norm[1]

    def reset_can_damage(self):
        """Suriken again can damage."""
        self.can_damage = True

    def on_hit(self):
        """Suriken cant damage."""
        self.can_damage = False
        self.cooldowns['can_damage'] = system.SHURIKEN_COOLDOWN_AFTER_REFLECT

    def image_rotation(self):
        """Change image sprite."""
        if self.can_damage:
            self.image_num = (self.image_num + 1) % 5
            self.image = images['shuriken'][self.image_num]
            self.mask = pygame.mask.from_surface(self.image)
            self.cooldowns['rotation'] = (system.SHURIKEN_ROTATION / self.velocity)
        else:
            self.image_num = (self.image_num + 1) % 5
            self.image = images['yellow_shuriken'][self.image_num]
            self.mask = pygame.mask.from_surface(self.image)
            self.cooldowns['rotation'] = (system.SHURIKEN_ROTATION / self.velocity)
