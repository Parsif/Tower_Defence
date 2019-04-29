import pygame

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
        coord = self._coord['x'] * 40, self._coord['y'] * 40
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
        coord = self._coord['x'] * 40, self._coord['y'] * 40
        pygame.draw.rect(screen, self._color, [coord[0], coord[1], 40, 40])

    def set_color(self, color=(255, 100, 100)):
        self._color = color

    def is_hovered(self, m_pos):
        coord = self._coord['x'] * 40, self._coord['y'] * 40
        if coord[0] < m_pos[0] < coord[0] + self._SIZE:
            if coord[1] < m_pos[1] < coord[1] + self._SIZE:
                return True

        return False


class BasicTower(Tower):
    def __init__(self, tower):
        Tower.__init__(self, tower._cellType, tower._coord)
        self.__image = pygame.image.load(r'images/tower/basicTower1.png')
        self.__damage = 30
        self.__cost = 100

    def draw(self, screen):
        coord = self._coord['x'] * 40, self._coord['y'] * 40
        screen.blit(self.__image, coord)

    def fire(self):
        pass

