import pygame

from helper_modules import tower_img
from helper_modules.sound import Sound


class Particle:
    speed = 15

    def __init__(self, x, y):
        self.__x, self.__y = x, y
        self.__radius = 10
        self.__color = (0, 0, 255)

    def update(self):
        if self.__x < 800:
            self.__x += self.speed
            return True

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.__color, (self.__x, self.__y), self.__radius)


class Cell:
    """
        Docstring
    """

    def __init__(self, cell_type, coord):
        self._cellType = cell_type
        self._coord = coord
        self.__image = None
        self.SIZE = 40

        if self._cellType == 0:
            self.__image = pygame.image.load(r'images/wasteland.jpg').convert()

        elif self._cellType == 1:
            self.__image = pygame.image.load(r'images/road.jpg').convert()

        elif self._cellType == 2:
            pass

        elif self._cellType == 5000:
            self.__image = pygame.image.load(r'images/castle.jpg').convert()

        elif self._cellType == -5000:
            self.__image = pygame.image.load(r'images/portal.jpg').convert()

        else:
            raise Exception('Unknown type of cell')

    def draw(self, screen):
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self.__image, coord)

    @property
    def get_coord(self):
        return self._coord


class Castle(Cell):
    def __init__(self, cell_type, coord):
        Cell.__init__(self, cell_type, coord)
        self.__HP = 100

    @property
    def get_hp(self):
        return self.__HP

    def take_damage(self, damage):
        self.__HP -= damage


class Tower(Cell):
    def __init__(self, cell_type, coord):
        Cell.__init__(self, cell_type, coord)
        self.__power = 0
        self.range = 2
        self._color = (255, 100, 100)
        self._buildCnt = 0
        self._Particle = Particle(self._coord['x'] * self.SIZE + self.SIZE // 2,
                                  self._coord['y'] * self.SIZE + self.SIZE // 3)

    def draw(self, screen):
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

    def set_color(self, color=(255, 100, 100)):
        self._color = color

    def set_build_cnt(self):
        self._buildCnt = 1

    @property
    def get_build_cnt(self):
        return self._buildCnt

    def is_hovered(self, m_pos):
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        if coord[0] < m_pos[0] < coord[0] + self.SIZE:
            if coord[1] < m_pos[1] < coord[1] + self.SIZE:
                return True

        return False

    def _find_mob(self, mobs):
        mobs_in_range = []
        for mob in mobs:
            rngX = abs(mob.rect.x - self._coord['x'] * self.SIZE)
            rngY = abs(mob.rect.y - self._coord['y'] * self.SIZE)
            if rngX <= 80 and rngY <= 80:
                mobs_in_range.append({'mob': mob, 'range': rngX + rngY})

        if len(mobs_in_range) > 0:
            mobs_in_range.sort(key=lambda m: m['range'])
            return mobs_in_range[0]['mob']

        return None

    def build(self, screen):
        if 1 <= self._buildCnt <= 40:

            if self._buildCnt in range(1, 5):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])
                screen.blit(tower_img.hmrStrikes[0], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))
                if Sound.soundMode:
                    Sound.towerConstruct.play()

            elif self._buildCnt in range(6, 10):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

                screen.blit(tower_img.hmrStrikes[1], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))

            elif self._buildCnt in range(11, 15):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

                screen.blit(tower_img.hmrStrikes[2], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))

            elif self._buildCnt in range(16, 20):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

                screen.blit(tower_img.hmrStrikes[3], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))

            elif self._buildCnt in range(21, 25):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])
                screen.blit(tower_img.hmrStrikes[0], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))

            elif self._buildCnt in range(26, 30):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

                screen.blit(tower_img.hmrStrikes[1], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))

            elif self._buildCnt in range(31, 35):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

                screen.blit(tower_img.hmrStrikes[2], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))

            elif self._buildCnt in range(36, 40):
                coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

                screen.blit(tower_img.hmrStrikes[3], (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - 20))

            screen.blit(tower_img.wood, (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE + 5))
            self._buildCnt += 1
        else:
            self._buildCnt = 0


class BasicTower(Tower):
    SPEED = 10  # less is faster

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self.__image = tower_img.basicTw1
        self.__DAMAGE = 20
        self.__COST = 100
        self.__fireCnt = self.SPEED

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self.__image, coord)

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        if Sound.soundMode:
            Sound.basicTwShot.play()
        near_mob.take_damage(self.__DAMAGE)
        self._Particle.draw(screen)


class FireTower(Tower):
    SPEED = 15  # less is faster

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self.__image = tower_img.fireTw1
        self.__DAMAGE = 15
        self.__COST = 100
        self.__fireCnt = self.SPEED
        self.__FIRE_DAMAGE = 5
        self.__EFFECT = {'type': 'fire', 'damage': self.__FIRE_DAMAGE}

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self.__image, coord)

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        if Sound.soundMode:
            Sound.fireTwShot.play()
        near_mob.take_damage(self.__DAMAGE, self.__EFFECT)
        self._Particle.draw(screen)


class IceTower(Tower):
    SPEED = 15  # less is faster

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self.__image = tower_img.iceTw1
        self.__DAMAGE = 20
        self.__COST = 100
        self.__fireCnt = self.SPEED
        self.__SLOW = 7
        self.__EFFECT = {'type': 'ice', 'slow': self.__SLOW}

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self.__image, coord)

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        if Sound.soundMode:
            Sound.iceTwShot.play()
        near_mob.take_damage(self.__DAMAGE, self.__EFFECT)
        self._Particle.draw(screen)


class DarkTower(Tower):
    SPEED = 10  # less is faster

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self.__image = tower_img.darkTw1
        self.__DAMAGE = 30
        self.__COST = 100
        self.__fireCnt = self.SPEED
        self.__FIRE_DAMAGE = 5
        # self.__EFFECT = {'type': 'fire', 'damage': self.__FIRE_DAMAGE}

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self.__image, coord)

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        if Sound.soundMode:
            Sound.darkTwShot.play()
        near_mob.take_damage(self.__DAMAGE)
        self._Particle.draw(screen)


class PoisonTower(Tower):
    SPEED = 15  # less is faster

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self.__image = tower_img.poisonTw1
        self.__DAMAGE = 20
        self.__COST = 100
        self.__fireCnt = self.SPEED
        self.__POISON_DAMAGE = 7
        self.__EFFECT = {'type': 'poison', 'poison': self.__POISON_DAMAGE}

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self.__image, coord)

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        if Sound.soundMode:
            Sound.poisonTwShot.play()
        near_mob.take_damage(self.__DAMAGE, self.__EFFECT)
        self._Particle.draw(screen)


towers = (BasicTower, FireTower, IceTower, DarkTower, PoisonTower)
