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

    def __init__(self, cell_type, coord, startX=0, startY=0):
        self.cellType = cell_type
        self.coord = {'x': coord['x'], 'y': coord['y']}
        self.image = None
        self.SIZE = 40
        self.startX = startX
        self.startY = startY
        self.color = (0, 0, 0)

        if self.cellType == 0:
            self.image = pygame.image.load(
                r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/wasteland.jpg').convert()

        elif self.cellType == 1:
            self.image = pygame.image.load(r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/road.jpg').convert()

        elif self.cellType == 2:
            pass

        elif self.cellType == 5000:
            self.image = pygame.image.load(r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/castle.jpg').convert()

        elif self.cellType == -5000:
            self.image = pygame.image.load(r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/portal.jpg').convert()

        else:
            raise Exception('Unknown type of cell')

    def draw(self, screen):
        coord = self.coord['x'] * self.SIZE + self.startX, self.coord['y'] * self.SIZE + self.startY
        screen.blit(self.image, coord)

    def is_hovered(self, m_pos):
        coord = self.coord['x'] * self.SIZE + self.startX, self.coord['y'] * self.SIZE + self.startY
        if coord[0] < m_pos[0] < coord[0] + self.SIZE:
            if coord[1] < m_pos[1] < coord[1] + self.SIZE:
                return True

        return False

    def set_color(self, color=(0, 100, 200)):
        self.color = color

    @property
    def get_coord(self):
        return self.coord


class EmptyCell(Cell):
    def __init__(self, cell_type, coord, startX=0, startY=0):
        Cell.__init__(self, cell_type, coord, startX, startY)
        self.color = (0, 100, 200)

    def draw(self, screen):
        coord = self.coord['x'] * self.SIZE + self.startX, self.coord['y'] * self.SIZE + self.startY
        pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])




class Castle(Cell):
    def __init__(self, cell_type, coord):
        Cell.__init__(self, cell_type, coord)
        self._HP = 10

    def set_hp(self, hp):
        self._HP = hp

    @property
    def get_hp(self):
        return self._HP

    def take_damage(self, damage):
        self._HP -= damage


class Tower(Cell):
    def __init__(self, cell_type, coord):
        Cell.__init__(self, cell_type, coord)
        self._power = 0
        self.range = 2
        self.color = (255, 100, 100)
        self.buildCnt = 0
        self.shotCnt = 0
        self.shotDx = 0
        self.shotDy = 0
        self.SHOT_STEPS = 3  # number of particle positions
        self.Particle = Particle(self.coord['x'] * self.SIZE + self.SIZE // 2,
                                 self.coord['y'] * self.SIZE + self.SIZE // 3)

    def draw(self, screen):
        coord = self.coord['x'] * self.SIZE + self.startX, self.coord['y'] * self.SIZE + self.startY
        pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])

    def set_color(self, color=(255, 100, 100)):
        self.color = color

    def set_build_cnt(self):
        self.buildCnt = 1

    @property
    def get_build_cnt(self):
        return self.buildCnt

    @property
    def get_shot_cnt(self):
        return self.shotCnt

    def is_hovered(self, m_pos):
        coord = self.coord['x'] * self.SIZE + self.startX, self.coord['y'] * self.SIZE + self.startY
        if coord[0] < m_pos[0] < coord[0] + self.SIZE:
            if coord[1] < m_pos[1] < coord[1] + self.SIZE:
                return True

        return False

    def _find_mob(self, mobs):
        mobs_in_range = []
        for mob in mobs:
            rngX = abs(mob.rect.x - self.coord['x'] * self.SIZE)
            rngY = abs(mob.rect.y - self.coord['y'] * self.SIZE)
            if rngX <= 80 and rngY <= 80:
                mobs_in_range.append({'mob': mob, 'range': rngX + rngY})

        if len(mobs_in_range) > 0:
            mobs_in_range.sort(key=lambda m: m['range'])
            return mobs_in_range[0]['mob']

        return None

    def build(self, screen):
        if 1 <= self.buildCnt <= 56:
            hmr_margin_top = self.SIZE / 2
            coord = self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE

            if self.buildCnt in range(1, 10):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[0],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))
                if Sound.soundMode:
                    Sound.towerConstruct.play()

            elif self.buildCnt in range(10, 20):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[2],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))

            elif self.buildCnt in range(20, 30):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[4],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))

            elif self.buildCnt in range(30, 40):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[6],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))

            elif self.buildCnt in range(40, 50):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[0],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))

            elif self.buildCnt in range(50, 60):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[2],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))

            elif self.buildCnt in range(60, 70):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[4],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))

            elif self.buildCnt in range(70, 80):
                pygame.draw.rect(screen, self.color, [coord[0], coord[1], self.SIZE, self.SIZE])
                screen.blit(tower_img.hmrStrikes[6],
                            (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE - hmr_margin_top))







            screen.blit(tower_img.wood, (self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE + 5))
            self.buildCnt += 1
        else:
            self.buildCnt = 0


class BasicTower(Tower):
    SPEED = 30  # less is faster
    COST = 25

    def __init__(self, tower):
        Tower.__init__(self, tower.cellType, tower.coord)
        self.image = tower_img.basicTw1
        self.DAMAGE = 20
        self._fireCnt = self.SPEED

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE
        screen.blit(self.image, coord)

    def show_shot(self, screen):
        if 1 <= self._shotCnt <= self.SHOT_STEPS:
            self.Particle.update(self._shotDx, self._shotDy)
            self.Particle.draw(screen)
            self._shotCnt += 1

    def fire(self, screen, mobs):
        self._fireCnt += 1

        if self._fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self._shotDx = (x - self.coord['x'] * self.SIZE) // self.SHOT_STEPS
        self._shotDy = (y - self.coord['y'] * self.SIZE) // self.SHOT_STEPS

        self._shotCnt = 1
        self.Particle.set_coord(self.coord['x'] * self.SIZE + self.SIZE // 2,
                                self.coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.basicTwShot.play()
        near_mob.take_damage(self.DAMAGE)
        self.Particle.draw(screen)


class FireTower(Tower):
    SPEED = 35  # less is faster
    COST = 50

    def __init__(self, tower):
        Tower.__init__(self, tower.cellType, tower.coord)
        self.image = tower_img.fireTw1
        self.DAMAGE = 15
        self.fireCnt = self.SPEED
        self.FIRE_DAMAGE = 20
        self.FIRE_LAST_FOR = 30
        self.EFFECT = {'type': 'fire', 'damage': self.FIRE_DAMAGE, 'last': self.FIRE_LAST_FOR}

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE
        screen.blit(self.image, coord)

    def show_shot(self, screen):
        if 1 <= self.shotCnt <= self.SHOT_STEPS:
            self.Particle.update(self.shotDx, self.shotDy)
            self.Particle.draw(screen)
            self.shotCnt += 1

    def fire(self, screen, mobs):
        self.fireCnt += 1

        if self.fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self.shotDx = (x - self.coord['x'] * self.SIZE) // self.SHOT_STEPS
        self.shotDy = (y - self.coord['y'] * self.SIZE) // self.SHOT_STEPS

        self.shotCnt = 1
        self.Particle.set_coord(self.coord['x'] * self.SIZE + self.SIZE // 2,
                                self.coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.fireTwShot.play()
        near_mob.take_damage(self.DAMAGE, self.EFFECT)
        self.Particle.draw(screen)


class IceTower(Tower):
    SPEED = 35  # less is faster
    COST = 75

    def __init__(self, tower):
        Tower.__init__(self, tower.cellType, tower.coord)
        self.image = tower_img.iceTw1
        self.DAMAGE = 20
        self.fireCnt = self.SPEED
        self.SLOW = 7
        self.SLOW_LAST_FOR = 25
        self.EFFECT = {'type': 'ice', 'slow': self.SLOW, 'last': self.SLOW_LAST_FOR}

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE
        screen.blit(self.image, coord)

    def show_shot(self, screen):
        if 1 <= self.shotCnt <= self.SHOT_STEPS:
            self.Particle.update(self.shotDx, self.shotDy)
            self.Particle.draw(screen)
            self.shotCnt += 1

    def fire(self, screen, mobs):
        self.fireCnt += 1

        if self.fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self.shotDx = (x - self.coord['x'] * self.SIZE) // self.SHOT_STEPS
        self.shotDy = (y - self.coord['y'] * self.SIZE) // self.SHOT_STEPS
        self.shotCnt = 1
        self.Particle.set_coord(self.coord['x'] * self.SIZE + self.SIZE // 2,
                                self.coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.iceTwShot.play()
        near_mob.take_damage(self.DAMAGE, self.EFFECT)
        self.Particle.draw(screen)


class DarkTower(Tower):
    SPEED = 55  # less is faster
    COST = 100

    def __init__(self, tower):
        Tower.__init__(self, tower.cellType, tower.coord)
        self.image = tower_img.darkTw1
        self.DAMAGE = 100
        self.fireCnt = self.SPEED
        self.FIRE_DAMAGE = 5

    # self.__EFFECT = {'type': 'fire', 'damage': self.__FIRE_DAMAGE}

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE
        screen.blit(self.image, coord)

    def show_shot(self, screen):
        if 1 <= self.shotCnt <= self.SHOT_STEPS:
            self.Particle.update(self.shotDx, self.shotDy)
            self.Particle.draw(screen)
            self.shotCnt += 1

    def fire(self, screen, mobs):
        self.fireCnt += 1

        if self.fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self.shotDx = (x - self.coord['x'] * self.SIZE) // self.SHOT_STEPS
        self.shotDy = (y - self.coord['y'] * self.SIZE) // self.SHOT_STEPS

        self.shotCnt = 1
        self.Particle.set_coord(self.coord['x'] * self.SIZE + self.SIZE // 2,
                                self.coord['y'] * self.SIZE + self.SIZE // 3)
        if Sound.soundMode:
            Sound.darkTwShot.play()
        near_mob.take_damage(self.DAMAGE)


class PoisonTower(Tower):
    SPEED = 30  # less is faster
    COST = 125

    def __init__(self, tower):
        Tower.__init__(self, tower.cellType, tower.coord)
        self.image = tower_img.poisonTw1
        self.DAMAGE = 30
        self.fireCnt = self.SPEED
        self.POISON_DAMAGE = 7
        self._EFFECT = {'type': 'poison', 'poison': self.POISON_DAMAGE}

    @property
    def get_cost(self):
        return self.COST

    def draw(self, screen):
        super().draw(screen)
        coord = self.coord['x'] * self.SIZE, self.coord['y'] * self.SIZE
        screen.blit(self.image, coord)

    def show_shot(self, screen):
        if 1 <= self.shotCnt <= self.SHOT_STEPS:
            self.Particle.update(self.shotDx, self.shotDy)
            self.Particle.draw(screen)
            self.shotCnt += 1

    def fire(self, screen, mobs):
        self.fireCnt += 1

        if self.fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        x, y = near_mob.rect.x, near_mob.rect.y
        self.shotDx = (x - self.coord['x'] * self.SIZE) // self.SHOT_STEPS
        self.shotDy = (y - self.coord['y'] * self.SIZE) // self.SHOT_STEPS

        self.shotCnt = 1
        self.Particle.set_coord(self.coord['x'] * self.SIZE + self.SIZE // 2,
                                self.coord['y'] * self.SIZE + self.SIZE // 3)

        if Sound.soundMode:
            Sound.poisonTwShot.play()
        near_mob.take_damage(self.DAMAGE, self._EFFECT)
        self.Particle.draw(screen)


class BasicTower2(BasicTower):
    SPEED = 25  # less is faster
    COST = BasicTower.COST * 2

    def __init__(self, tower):
        BasicTower.__init__(self, tower)
        self.image = tower_img.basicTw2
        self.DAMAGE = 40


class FireTower2(FireTower):
    SPEED = 30  # less is faster
    COST = FireTower.COST * 2

    def __init__(self, tower):
        FireTower.__init__(self, tower)
        self.image = tower_img.fireTw2
        self.DAMAGE = 20
        self.FIRE_DAMAGE = 30


class IceTower2(IceTower):
    SPEED = 35  # less is faster
    COST = IceTower.COST * 2

    def __init__(self, tower):
        IceTower.__init__(self, tower)
        self.image = tower_img.iceTw2
        self.DAMAGE = 25
        self.SLOW = 15


class DarkTower2(DarkTower):
    SPEED = 55
    COST = DarkTower.COST * 2

    def __init__(self, tower):
        DarkTower.__init__(self, tower)
        self.image = tower_img.darkTw2
        self.DAMAGE = 200


class PoisonTower2(PoisonTower):
    SPEED = 30  # less is faster
    COST = PoisonTower.COST * 2

    def __init__(self, tower):
        PoisonTower.__init__(self, tower)
        self.image = tower_img.poisonTw2
        self.DAMAGE = 60
        self.POISON_DAMAGE = 15


tw_lvl1 = (BasicTower, FireTower, IceTower, DarkTower, PoisonTower)

tw_lvl2 = (BasicTower2, FireTower2, IceTower2, DarkTower2, PoisonTower2)
