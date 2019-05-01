import pygame

from helper_modules import tower_img
from helper_modules.sound import Sound


class Particle:
    speed = 15

    def __init__(self, x, y):
        self.__x, self.__y = x, y
        self.__radius = 8
        self.__color = (0, 0, 255)

    def set_coord(self, x, y):
        self.__x = x
        self.__y = y

    def update(self, dx, dy):
        self.__x += dx
        self.__y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.__color, (self.__x, self.__y), self.__radius)


class Cell:
    """
        Docstring
    """

    def __init__(self, cell_type, coord):
        self._cellType = cell_type
        self._coord = coord
        self._image = None
        self.SIZE = 40

        if self._cellType == 0:
            self._image = pygame.image.load(r'images/wasteland.jpg').convert()

        elif self._cellType == 1:
            self._image = pygame.image.load(r'images/road.jpg').convert()

        elif self._cellType == 2:
            pass

        elif self._cellType == 5000:
            self._image = pygame.image.load(r'images/castle.jpg').convert()

        elif self._cellType == -5000:
            self._image = pygame.image.load(r'images/portal.jpg').convert()

        else:
            raise Exception('Unknown type of cell')

    def draw(self, screen):
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self._image, coord)

    @property
    def get_coord(self):
        return self._coord


class Castle(Cell):
    def __init__(self, cell_type, coord):
        Cell.__init__(self, cell_type, coord)
        self.__HP = 10

    def set_hp(self, hp):
        self.__HP = hp

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
        self._shotCnt = 0
        self._shotDx = 0
        self._shotDy = 0
        self._SHOT_STEPS = 3  # number of particle positions
        self._Particle = Particle(self._coord['x'] * self.SIZE + self.SIZE // 2,
                                  self._coord['y'] * self.SIZE + self.SIZE // 3)

    def draw(self, screen):
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])

    def set_color(self, color=(255, 100, 100)):
        self._color = color

    def set_build_cnt(self):
        self._buildCnt = 1

    @property
    def get_build_cnt(self):
        return self._buildCnt

    @property
    def get_shot_cnt(self):
        return self._shotCnt

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
            hmr_margin_top = self.SIZE / 2
            coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE

            if self._buildCnt in range(1, 5):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[0],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))
                if Sound.soundMode:
                    Sound.towerConstruct.play()

            elif self._buildCnt in range(6, 10):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])

                screen.blit(tower_img.hmrStrikes[1],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))

            elif self._buildCnt in range(11, 15):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])

                screen.blit(tower_img.hmrStrikes[2],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))

            elif self._buildCnt in range(16, 20):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])

                screen.blit(tower_img.hmrStrikes[3],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))

            elif self._buildCnt in range(21, 25):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[0],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))

            elif self._buildCnt in range(26, 30):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])

                screen.blit(tower_img.hmrStrikes[1],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))

            elif self._buildCnt in range(31, 35):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])

                screen.blit(tower_img.hmrStrikes[2],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))

            elif self._buildCnt in range(36, 40):
                pygame.draw.rect(screen, self._color, [coord[0], coord[1], self.SIZE, self.SIZE])

                screen.blit(tower_img.hmrStrikes[3],
                            (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE - hmr_margin_top))

            screen.blit(tower_img.wood, (self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE + 5))
            self._buildCnt += 1
        else:
            self._buildCnt = 0


class BasicTower(Tower):
    SPEED = 10  # less is faster
    COST = 25

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self._image = tower_img.basicTw1
        self._DAMAGE = 20
        self.__fireCnt = self.SPEED

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self._image, coord)

    def show_shot(self, screen):
        if 1 <= self._shotCnt <= self._SHOT_STEPS:
            self._Particle.update(self._shotDx, self._shotDy)
            self._Particle.draw(screen)
            self._shotCnt += 1

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self._shotDx = (x - self._coord['x'] * self.SIZE) // self._SHOT_STEPS
        self._shotDy = (y - self._coord['y'] * self.SIZE) // self._SHOT_STEPS

        self._shotCnt = 1
        self._Particle.set_coord(self._coord['x'] * self.SIZE + self.SIZE // 2,
                                 self._coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.basicTwShot.play()
        near_mob.take_damage(self._DAMAGE)
        self._Particle.draw(screen)


class FireTower(Tower):
    SPEED = 15  # less is faster
    COST = 50

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self._image = tower_img.fireTw1
        self._DAMAGE = 15
        self.__fireCnt = self.SPEED
        self._FIRE_DAMAGE = 20
        self._FIRE_LAST_FOR = 30
        self._EFFECT = {'type': 'fire', 'damage': self._FIRE_DAMAGE, 'last': self._FIRE_LAST_FOR}

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self._image, coord)

    def show_shot(self, screen):
        if 1 <= self._shotCnt <= self._SHOT_STEPS:
            self._Particle.update(self._shotDx, self._shotDy)
            self._Particle.draw(screen)
            self._shotCnt += 1

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self._shotDx = (x - self._coord['x'] * self.SIZE) // self._SHOT_STEPS
        self._shotDy = (y - self._coord['y'] * self.SIZE) // self._SHOT_STEPS

        self._shotCnt = 1
        self._Particle.set_coord(self._coord['x'] * self.SIZE + self.SIZE // 2,
                                 self._coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.fireTwShot.play()
        near_mob.take_damage(self._DAMAGE, self._EFFECT)
        self._Particle.draw(screen)


class IceTower(Tower):
    SPEED = 15  # less is faster
    COST = 75

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self._image = tower_img.iceTw1
        self._DAMAGE = 20
        self.__fireCnt = self.SPEED
        self._SLOW = 7
        self._SLOW_LAST_FOR = 25
        self._EFFECT = {'type': 'ice', 'slow': self._SLOW, 'last': self._SLOW_LAST_FOR}

    @property
    def get_cost(self):
        return self.COST


    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self._image, coord)

    def show_shot(self, screen):
        if 1 <= self._shotCnt <= self._SHOT_STEPS:
            self._Particle.update(self._shotDx, self._shotDy)
            self._Particle.draw(screen)
            self._shotCnt += 1

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self._shotDx = (x - self._coord['x'] * self.SIZE) // self._SHOT_STEPS
        self._shotDy = (y - self._coord['y'] * self.SIZE) // self._SHOT_STEPS
        self._shotCnt = 1
        self._Particle.set_coord(self._coord['x'] * self.SIZE + self.SIZE // 2,
                                 self._coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.iceTwShot.play()
        near_mob.take_damage(self._DAMAGE, self._EFFECT)
        self._Particle.draw(screen)


class DarkTower(Tower):
    SPEED = 10  # less is faster
    COST = 100

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self._image = tower_img.darkTw1
        self._DAMAGE = 50
        self.__fireCnt = self.SPEED
        self._FIRE_DAMAGE = 5

    # self.__EFFECT = {'type': 'fire', 'damage': self.__FIRE_DAMAGE}

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self._image, coord)

    def show_shot(self, screen):
        if 1 <= self._shotCnt <= self._SHOT_STEPS:
            self._Particle.update(self._shotDx, self._shotDy)
            self._Particle.draw(screen)
            self._shotCnt += 1

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self._shotDx = (x - self._coord['x'] * self.SIZE) // self._SHOT_STEPS
        self._shotDy = (y - self._coord['y'] * self.SIZE) // self._SHOT_STEPS

        self._shotCnt = 1
        self._Particle.set_coord(self._coord['x'] * self.SIZE + self.SIZE // 2,
                                 self._coord['y'] * self.SIZE + self.SIZE // 3)
        if Sound.soundMode:
            Sound.darkTwShot.play()
        near_mob.take_damage(self._DAMAGE)


class PoisonTower(Tower):
    SPEED = 15  # less is faster
    COST = 125

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self._image = tower_img.poisonTw1
        self._DAMAGE = 20
        self.__fireCnt = self.SPEED
        self._POISON_DAMAGE = 7
        self.__EFFECT = {'type': 'poison', 'poison': self._POISON_DAMAGE}

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self._coord['x'] * self.SIZE, self._coord['y'] * self.SIZE
        screen.blit(self._image, coord)

    def show_shot(self, screen):
        if 1 <= self._shotCnt <= self._SHOT_STEPS:
            self._Particle.update(self._shotDx, self._shotDy)
            self._Particle.draw(screen)
            self._shotCnt += 1

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self._shotDx = (x - self._coord['x'] * self.SIZE) // self._SHOT_STEPS
        self._shotDy = (y - self._coord['y'] * self.SIZE) // self._SHOT_STEPS

        self._shotCnt = 1
        self._Particle.set_coord(self._coord['x'] * self.SIZE + self.SIZE // 2,
                                 self._coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.poisonTwShot.play()
        near_mob.take_damage(self._DAMAGE, self.__EFFECT)
        self._Particle.draw(screen)


class BasicTower2(BasicTower):
    SPEED = 10  # less is faster
    COST = BasicTower.COST * 2

    def __init__(self, tower):
        BasicTower.__init__(self, tower)
        self._image = tower_img.basicTw2
        self._DAMAGE = 40


class FireTower2(FireTower):
    SPEED = 15  # less is faster
    COST = FireTower.COST * 2

    def __init__(self, tower):
        FireTower.__init__(self, tower)
        self._image = tower_img.fireTw2
        self._DAMAGE = 100
        self._FIRE_DAMAGE = 0


class IceTower2(IceTower):
    SPEED = 15  # less is faster
    COST = IceTower.COST * 2

    def __init__(self, tower):
        IceTower.__init__(self, tower)
        self._image = tower_img.iceTw2
        self._DAMAGE = 50
        self._SLOW = 7


class DarkTower2(DarkTower):
    SPEED = 20
    COST = DarkTower.COST * 2

    def __init__(self, tower):
        DarkTower.__init__(self, tower)
        self._image = tower_img.darkTw2
        self._DAMAGE = 100


class PoisonTower2(PoisonTower):
    SPEED = 15  # less is faster
    COST = PoisonTower.COST * 2

    def __init__(self, tower):
        PoisonTower.__init__(self, tower)
        self._image = tower_img.poisonTw2
        self._DAMAGE = 30
        self._POISON_DAMAGE = 15


tw_lvl1 = (BasicTower, FireTower, IceTower, DarkTower, PoisonTower)

tw_lvl2 = (BasicTower2, FireTower2, IceTower2, DarkTower2, PoisonTower2)
