import pygame
import system
import utility

image_dir = system.IMAGES_FOLDER + "range_attack/"
images_haduken = utility.load_images_by_dir_right(image_dir)
images_haduken_len = len(images_haduken[0])


class RangeAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, player_direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = images_haduken[player_direction][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.haduken_direction = player_direction
        self.start_x = x
        self.start_y = y
        self.rect.centery = y
        self.rect.centerx = x
        self.last_frame = False
        self.image_counter = 0
        if player_direction == 0:
            self.speed_x = -system.HADUKEN_SPEED
        else:
            self.speed_x = system.HADUKEN_SPEED

    def update(self):
        self.rect.centerx += self.speed_x
        if self.rect.left < 0 or self.rect.right > system.WIN_WIDTH:
            self.kill()
        if not self.last_frame:
            self.start_animation()

    def start_animation(self):
        self.image_counter += 1 * system.HADUKEN_SPEED_ANIMATION
        im_counter = int(self.image_counter) % images_haduken_len
        self.image = images_haduken[self.haduken_direction][im_counter]
        self.mask = pygame.mask.from_surface(self.image)
        if im_counter == images_haduken_len - 1:
            self.last_frame = True
