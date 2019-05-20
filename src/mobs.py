import pygame

from helper_modules import spider_imgs, dragon_imgs, turtle_imgs
from helper_modules import tower_img
from helper_modules.sound import Sound


class Mob(pygame.sprite.Sprite):
    """
        Docstring
    """

    def __init__(self, start, path):
        pygame.sprite.Sprite.__init__(self)
        self._start = start
        self._path = path
        self.images = []
        self._coord = {'x': 0, 'y': 0}
        self.is_end_reached = False

        self._imageCnt = 0
        self.__pathCnt = 0
        self.__stepCnt = -1
        self.__animCnt = 4
        self._imageSource = spider_imgs.spider_up

        self._turns_dead = 0
        self._fireCnt = 0
        self._iceCnt = 0
        self._fireDgm = 0

        self._SPEED = 0  # less is better
        self._speedCnt = 0
        self._iceSlow = 0
        self._fireLastFor = 100
        self._iceLastFor = 100

    @property
    def get_turns_dead(self):
        return self._turns_dead

    def __take_a_step(self):
        self.__animCnt += 1
        if self.__animCnt % 4 == 0:
            self.__pathCnt += 1
            return None
        if len(self._path) == self.__pathCnt:
            self.is_end_reached = True
            self.__pathCnt += 1
            return None

        self._coord = self._path[self.__pathCnt]

    def _next_img(self):
        pass

    def __move(self):
        dx = self._coord['x'] * 40 - self.rect.x
        dy = self._coord['y'] * 40 - self.rect.y

        if dx == 40 or dx == -40:
            self.rect.move_ip(dx / 4, 0)

        elif dx == 30 or dx == -30:
            self.rect.move_ip(dx / 3, 0)

        elif dx == 20 or dx == -20:
            self.rect.move_ip(dx / 2, 0)

        elif dx == 10 or dx == -10:
            self.rect.move_ip(dx, 0)

        elif dy == 40 or dy == -40:
            self.rect.move_ip(0, dy / 4)

        elif dy == 30 or dy == -30:
            self.rect.move_ip(0, dy / 3)

        elif dy == 20 or dy == -20:
            self.rect.move_ip(0, dy / 2)

        elif dy == 10 or dy == -10:
            self.rect.move_ip(0, dy)

    def update(self, *args):
        self._speedCnt += 1
        if self._speedCnt % (self._SPEED + self._iceSlow) == 0:
            self.images.clear()
            self.__take_a_step()
            self.__move()
            self._next_img()

            self._imageCnt += 1
            if self._imageCnt == len(self._imageSource):
                self._imageCnt = 0
            self.images.append(self._imageSource[self._imageCnt])

        if 1 <= self._fireCnt < self._fireLastFor:
            self.images.append(tower_img.fire)
            self._fireCnt += 1
        else:
            self._fireCnt = 0
            self._fireDgm = 0

        if 1 <= self._iceCnt < self._iceLastFor:
            self.images.append(tower_img.ice)
            self._iceCnt += 1
        else:
            self._iceCnt = 0
            self._iceSlow = 0

    def draw(self, screen):
        for img in self.images:
            screen.blit(img, self.rect)


class Spider(Mob):
    def __init__(self, start, path):
        Mob.__init__(self, start, path)
        self.image = spider_imgs.spider_down[0]
        self.rect = self.image.get_rect(topleft=(self._start['x'] * 40, self._start['y'] * 40))
        self.__hp = 130
        self._SPEED = 6
        self._speedCnt = self._SPEED
        self.__COST = 10

    @property
    def get_cost(self):
        return self.__COST

    def _next_img(self):
        dx = self._coord['x'] * 40 - self.rect.x
        dy = self._coord['y'] * 40 - self.rect.y

        if dx > 0:
            self._imageSource = spider_imgs.spider_right

        elif dx < 0:
            self._imageSource = spider_imgs.spider_left

        elif dy > 0:
            self._imageSource = spider_imgs.spider_down

        elif dy < 0:
            self._imageSource = spider_imgs.spider_up

    def draw_dead(self, screen):
        self.image = spider_imgs.spider_dead[0]
        screen.blit(self.image, self.rect)
        self._turns_dead += 1

    def take_damage(self, damage, effect=None):
        self.__hp -= damage
        if self.__hp <= 0 and Sound.soundMode:
            Sound.spider_death.play()

        elif effect is not None:
            if effect['type'] == 'fire':
                self._fireCnt = 1
                self._fireDgm = effect['damage']
                self._fireLastFor = effect['last']
            elif effect['type'] == 'ice':
                self._iceCnt = 1
                self._iceSlow = effect['slow']
                self._iceLastFor = effect['last']
            # elif effect['type'] == 'poison':
            #     self._iceCnt = 1

    def update(self, *args):
        super().update()
        if 1 <= self._fireCnt < 6:
            self.take_damage(self._fireDgm)

    @property
    def get_hp(self):
        return self.__hp


class Turtle(Mob):
    def __init__(self, start, path):
        Mob.__init__(self, start, path)
        self.image = turtle_imgs.turtle_down[0]
        self.rect = self.image.get_rect(topleft=(self._start['x'] * 40, self._start['y'] * 40))
        self.__hp = 400
        self._SPEED = 8
        self._speedCnt = self._SPEED
        self.__COST = 50

    @property
    def get_cost(self):
        return self.__COST

    def _next_img(self):
        dx = self._coord['x'] * 40 - self.rect.x
        dy = self._coord['y'] * 40 - self.rect.y

        if dx > 0:
            self._imageSource = turtle_imgs.turtle_right

        elif dx < 0:
            self._imageSource = turtle_imgs.turtle_left

        elif dy > 0:
            self._imageSource = turtle_imgs.turtle_down

        elif dy < 0:
            self._imageSource = turtle_imgs.turtle_up

    def draw_dead(self, screen):
        self.image = turtle_imgs.turtle_dead[0]
        screen.blit(self.image, self.rect)
        self._turns_dead += 1

    def take_damage(self, damage, effect=None):
        self.__hp -= damage
        if self.__hp <= 0 and Sound.soundMode:
            Sound.turtle_death.play()

        elif effect is not None:
            if effect['type'] == 'fire':
                self._fireCnt = 1
                self._fireDgm = effect['damage']
                self._fireLastFor = effect['last']
            elif effect['type'] == 'ice':
                self._iceCnt = 1
                self._iceSlow = effect['slow']
                self._iceLastFor = effect['last']
            # elif effect['type'] == 'poison':
            #     self._iceCnt = 1

    def update(self, *args):
        super().update()
        if 1 <= self._fireCnt < 6:
            self.take_damage(self._fireDgm)

    @property
    def get_hp(self):
        return self.__hp


class Dragon(Mob):
    def __init__(self, start, path):
        Mob.__init__(self, start, path)
        self.image = dragon_imgs.dragon_down[0]
        self.rect = self.image.get_rect(topleft=(self._start['x'] * 40, self._start['y'] * 40))
        self.__hp = 2000
        self._SPEED = 10
        self._speedCnt = self._SPEED
        self.__COST = 500

    @property
    def get_cost(self):
        return self.__COST

    def _next_img(self):
        dx = self._coord['x'] * 40 - self.rect.x
        dy = self._coord['y'] * 40 - self.rect.y

        if dx > 0:
            self._imageSource = dragon_imgs.dragon_right

        elif dx < 0:
            self._imageSource = dragon_imgs.dragon_left

        elif dy > 0:
            self._imageSource = dragon_imgs.dragon_down

        elif dy < 0:
            self._imageSource = dragon_imgs.dragon_up

    def draw_dead(self, screen):
        self.image = dragon_imgs.dragon_dead[0]
        screen.blit(self.image, self.rect)
        self._turns_dead += 1

    def take_damage(self, damage, effect=None):
        self.__hp -= damage
        if self.__hp <= 0 and Sound.soundMode:
            Sound.dragon_death.play()

        elif effect is not None:
            if effect['type'] == 'fire':
                self._fireCnt = 1
                self._fireDgm = effect['damage']
                self._fireLastFor = effect['last']
            elif effect['type'] == 'ice':
                self._iceCnt = 1
                self._iceSlow = effect['slow']
                self._iceLastFor = effect['last']
            # elif effect['type'] == 'poison':
            #     self._iceCnt = 1

    def update(self, *args):
        super().update()
        if 1 <= self._fireCnt < 6:
            self.take_damage(self._fireDgm)

    @property
    def get_hp(self):
        return self.__hp
