import pygame


class Mob(pygame.sprite.Sprite):
    def __init__(self, start):
        pygame.sprite.Sprite.__init__(self)
        self._coord = start
        self.image = None
        self._path = None

    def draw_mob(self, screen):
        screen.blit(self.image, (self._coord['x'] * 40, self._coord['y'] * 40))


class Skeleton(Mob):
    def __init__(self, start):
        Mob.__init__(self, start)
        self.image = pygame.image.load(r'images/s1.jpg').convert()
        self.rect = self.image.get_rect(center=(self._coord['x'], self._coord['y']))

    def move(self):
        if self._coord['x'] < 20:
            self._coord['x'] += 1


