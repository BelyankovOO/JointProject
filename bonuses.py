"""JointProject NinjaSamurai."""
import random
import pygame
import system
import utility

image_bonus_resize = (30, 30)


class BonusBase(pygame.sprite.Sprite):
    """
    Bonus base class.

    :param hero: controlled model
    :param image_dir: image directory
    """

    def __init__(self, hero, image_dir):
        """Bonus Base class init."""
        pygame.sprite.Sprite.__init__(self)
        self.hero = hero
        self.images_bonus = utility.load_images_by_dir_right(image_dir)
        self.images_bonus_len = len(self.images_bonus[0])
        self.image = self.images_bonus[0][0]
        self.image = pygame.transform.scale(self.image, image_bonus_resize)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.bot_y, self.top_y = 500, 600
        self.left_x, self.right_x = 0, system.WIN_WIDTH \
            - self.image.get_width()
        self.rect.y = -self.image.get_width()
        self.rect.x = random.randint(self.left_x, self.right_x)
        self.create_time = pygame.time.get_ticks()
        self.is_taken = False
        self.drawable = True
        self.last_update = pygame.time.get_ticks()
        self.speed_y = system.BONUS_START_SPEED

    def action(self):
        """Act of current bonus."""
        pass

    def take_bonus(self):
        """Bonus take."""
        self.is_taken = True
        self.action()

    def update(self):
        """Bonus update."""
        if self.rect.bottom > system.WIN_HEIGHT:
            self.speed_y = 0
        self.rect.y += self.speed_y
        now = pygame.time.get_ticks()
        second_after_create = (now - self.create_time) / 1000
        if self.is_taken:
            self.kill()
        elif system.BONUS_HIDE_TIME * system.BONUS_BLINKING_BARRIER \
                <= second_after_create < system.BONUS_HIDE_TIME and \
                now % system.BONUS_BLINKING_FREQUENCY == 0:
            self.drawable = not self.drawable
        elif second_after_create >= system.BONUS_HIDE_TIME:
            self.kill()

    def draw(self, screen):
        """
        Bonus draw.

        :param screen: main screen
        """
        if self.drawable:
            screen.blit(self.image, self.rect)


class LifeBonus(BonusBase):
    """
    Discrete bonus class.

    :param bonus_sprite: sprite of discrete bonus
    :param hero: controlled model
    """

    def __init__(self, bonus_sprites, hero):
        """Life bonus init."""
        self.image_dir = system.IMAGES_FOLDER + "bonus/heart/"
        super().__init__(hero, self.image_dir)

    def action(self):
        """Discrete action of bonus."""
        self.hero.getLifeBonus()


class InvulnerableBonus(BonusBase):
    """
    Discrete bonus class.

    :param bonus_sprite: sprite of discrete bonus
    :param hero: controlled model
    """

    def __init__(self, bonus_sprites, hero):
        """Invulnerable bonus init."""
        self.image_dir = system.IMAGES_FOLDER + "bonus/shield/"
        super().__init__(hero, self.image_dir)

    def action(self):
        """Discrete action of bonus."""
        self.hero.getInvulnerableBonus()
