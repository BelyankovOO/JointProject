"""JointProject NinjaSamurai."""
import pygame
import math


class CooldownAnimation():
    """
    Cooldown animation class.

    :param image: image of cooldown
    :param copy_of_image: copy of cooldown image
    :cooldown_time: time of cooldown
    :position_on_screen: coordinates
    """

    def __init__(self, image, copy_of_image, cooldown_time, position_on_screen):
        """Init CooldownAnimation class."""
        pygame.sprite.Sprite.__init__(self)
        self.start_image = copy_of_image
        self.image = image
        self.rect = self.image.get_rect()
        self.alpha_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.alpha_surface.set_alpha(128)
        self.rect.x = position_on_screen[0]
        self.rect.y = position_on_screen[1]
        self.cooldown_time = cooldown_time
        self.angle_of_rotation = 270
        self.checker = [False, False, False, False]
        self.radius = math.ceil(math.sqrt((self.rect.width / 2)**2 + (self.rect.height / 2)**2))
        self.key_points = [(self.rect.width / 2, self.rect.height / 2), (self.rect.width / 2,
                                    self.rect.height / 2 - self.radius)]

    def update(self, cooldown_anim_started, cooldown_checker):
        """Update Cooldown Animation Class."""
        if cooldown_anim_started:
            if self.angle_of_rotation - 360 <= 270:
                self.angle_of_rotation = 270 + (1 - cooldown_checker / self.cooldown_time) * 360
                if self.angle_of_rotation - 360 >= 45 and not self.checker[0]:
                    self.key_points.append((self.get_x_coordinate(self.radius, 315),
                                            self.get_y_coordinate(self.radius, 315)))
                    self.checker[0] = True
                if self.angle_of_rotation - 360 >= 135 and not self.checker[1]:
                    self.key_points.append((self.get_x_coordinate(self.radius, 45),
                                            self.get_y_coordinate(self.radius, 45)))
                    self.checker[1] = True
                if self.angle_of_rotation - 360 >= 225 and not self.checker[2]:
                    self.key_points.append((self.get_x_coordinate(self.radius, 135),
                                            self.get_y_coordinate(self.radius, 135)))
                    self.checker[2] = True
                if self.angle_of_rotation - 360 >= 315 and not self.checker[3]:
                    self.key_points.append((self.get_x_coordinate(self.radius, 225),
                                            self.get_y_coordinate(self.radius, 225)))
                    self.checker[3] = True
                self.key_points.append((self.get_x_coordinate(self.radius, self.angle_of_rotation),
                    self.get_y_coordinate(self.radius, self.angle_of_rotation)))
                pygame.draw.polygon(self.alpha_surface, (255, 255, 255), self.key_points)
                self.key_points.pop()
                self.image.blit(self.start_image, (0, 0))
                self.image.blit(self.alpha_surface, (0, 0))
            else:
                self.image.blit(self.start_image, (0, 0))
        else:
            self.image.blit(self.start_image, (0, 0))
            self.angle_of_rotation = 270
            self.key_points = [(self.rect.width / 2, self.rect.height / 2), (self.rect.width / 2,
                                    self.rect.height / 2 - self.radius)]
            self.checker = [False, False, False, False]
            self.alpha_surface = pygame.Surface((self.rect.width, self.rect.height))
            self.alpha_surface.set_alpha(128)

    def draw(self, screen):
        """
        Draw cooldown.

        :param screen: main screen
        """
        screen.blit(self.image, self.rect)

    def get_x_coordinate(self, radius, angle):
        """
        Get x coordinate for circle.

        :param radius: radius of circle
        :param angle: angle
        """
        return self.rect.width / 2 + radius * math.cos(angle * math.pi / 180)

    def get_y_coordinate(self, radius, angle):
        """
        Get y coordinate for circle.

        :param radius: radius of circle
        :param angle: angle
        """
        return self.rect.height / 2 + radius * math.sin(angle * math.pi / 180)
