from bonuses import *

bonuses_list = [InvulnerableBonus, LifeBonus]


class BonusCreater(object):
    def __init__(self, hero, bonus_sprites):
        self.last_ticks = pygame.time.get_ticks()
        self.hero = hero
        self.bonus_sprites = bonus_sprites

    def need_create_bonus(self):
        seconds_passed = (pygame.time.get_ticks() - self.last_ticks) / 1000
        if seconds_passed > system.BONUS_SPAWN_CD:
            self.last_ticks = pygame.time.get_ticks()
            return True
        else:
            return False

    def create_bonus(self):
        if self.need_create_bonus():
            bonus_type = random.choice(bonuses_list)
            bonus_example = bonus_type(self.bonus_sprites, self.hero)
            self.bonus_sprites.add(bonus_example)

    def draw(self, screen):
        for bonus in self.bonus_sprites:
            bonus.draw(screen)
