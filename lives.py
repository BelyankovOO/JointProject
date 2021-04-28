"""JointProject NinjaSamurai."""
import pygame
import system

image_live = pygame.image.load(system.IMAGES_FOLDER + "lives/live.png")


class Lives():
    """Class of lives in corner."""

    def __init__(self):
        """Init lives."""
        self.number_of_lives = system.NUMBER_OF_LIVES
        self.image = image_live

    def draw(self, screen):
        """
        Draw lives.

        :param screen: main screen
        """
        for offset in range(self.number_of_lives):
            self.live_rect = self.image.get_rect()
            self.live_rect.x = system.LIVE_POSITION_WIDHT + 30 * offset
            self.live_rect.y = system.LIVE_POSITION_HEIGHT
            screen.blit(self.image, self.live_rect)

    def decrease_number_of_lives(self):
        """Minus one live."""
        self.number_of_lives -= 1

    def increase_number_of_lives(self):
        """Plus one live."""
        if self.number_of_lives < system.MAX_NUMBER_OF_LIVES:
            self.number_of_lives += 1

    def check_number_of_of_lives(self):
        """Get numner of lives."""
        return self.number_of_lives
