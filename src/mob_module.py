import pygame
import spider_imgs


class Mob(pygame.sprite.Sprite):
    def __init__(self, start):
        pygame.sprite.Sprite.__init__(self)
        self._start = start
        self._path = None
        self.image = None


class Spider(Mob):
    def __init__(self, start):
        Mob.__init__(self, start)
        self.__imageCnt = 0
        self.image = spider_imgs.spider_down[0]
        self.rect = self.image.get_rect(topleft=(self._start['x'] * 40, self._start['y'] * 40))


    def update(self, *args):
        print(f"X: {self.rect.x}, Y: {self.rect.y}")
        if self.rect.y < 400:
            self.rect.move_ip(0, 20)

        self.__imageCnt += 1
        if self.__imageCnt == 8:
            self.__imageCnt = 0
        self.image = spider_imgs.spider_down[self.__imageCnt]

    def draw(self, screen):
        screen.blit(self.image, self.rect)



