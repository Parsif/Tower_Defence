import pygame


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
        self._SIZE = 40

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
        coord = self._coord['x'] * self._SIZE, self._coord['y'] * self._SIZE
        screen.blit(self.__image, coord)

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
        self._image = None

    def draw(self, screen):
        coord = self._coord['x'] * self._SIZE, self._coord['y'] * self._SIZE
        pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

    def set_color(self, color=(255, 100, 100)):
        self._color = color

    def is_hovered(self, m_pos):
        coord = self._coord['x'] * self._SIZE, self._coord['y'] * self._SIZE
        if coord[0] < m_pos[0] < coord[0] + self._SIZE:
            if coord[1] < m_pos[1] < coord[1] + self._SIZE:
                return True

        return False

    def _find_mob(self, mobs):
        mobs_in_range = []
        for mob in mobs:
            rngX = abs(mob.rect.x - self._coord['x'] * self._SIZE)
            rngY = abs(mob.rect.y - self._coord['y'] * self._SIZE)
            if rngX <= 80 and rngY <= 80:
                mobs_in_range.append({'mob': mob, 'range': rngX + rngY})

        if len(mobs_in_range) > 0:
            mobs_in_range.sort(key=lambda m: m['range'])
            return mobs_in_range[0]['mob']

        return None


class BasicTower(Tower):
    SPEED = 10  # less is faster

    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self.__image = pygame.image.load(r'images/tower/basicTower1.png')
        self.__damage = 20
        self.__cost = 100
        self.__fireCnt = self.SPEED
        self.__Particle = Particle(self._coord['x'] * self._SIZE + self._SIZE // 2,
                                   self._coord['y'] * self._SIZE + self._SIZE // 2)

    def draw(self, screen):
        coord = self._coord['x'] * self._SIZE, self._coord['y'] * self._SIZE
        screen.blit(self.__image, coord)

    def fire(self, screen, mobs):
        self.__fireCnt += 1

        if self.__fireCnt % self.SPEED != 0:
            return None

        near_mob = self._find_mob(mobs)
        if near_mob is None:
            return None

        near_mob.take_damage(self.__damage)
        self.__Particle.draw(screen)



