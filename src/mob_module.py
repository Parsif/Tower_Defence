import pygame
import spider_imgs


class Mob(pygame.sprite.Sprite):
    """
        Docstring
    """
    def __init__(self, start, path):
        pygame.sprite.Sprite.__init__(self)
        self.__imageCnt = 0
        self.__path_cnt = 0
        self._start = start
        self._path = path
        self.image = None

    def __take_a_step(self):
        if len(self._path) == self.__path_cnt:
            return None

        return self._path[self.__path_cnt]

    def update(self, *args):
        coord = self.__take_a_step()
        if coord is None:
            return
        self.rect.x, self.rect.y = coord['x'] * 40, coord['y'] * 40
        self.__path_cnt += 1
        self.__imageCnt += 1
        if self.__imageCnt == 8:
            self.__imageCnt = 0
        self.image = spider_imgs.spider_down[self.__imageCnt]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Spider(Mob):
    def __init__(self, start, path):
        Mob.__init__(self, start, path)
        self.__stepCnt = -1
        self.image = spider_imgs.spider_down[0]
        self.rect = self.image.get_rect(topleft=(self._start['x'] * 40, self._start['y'] * 40))





