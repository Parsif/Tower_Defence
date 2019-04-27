import pygame


class Cell:
    """
        Docstring
    """

    def __init__(self, cell_type, coord):
        self.__cellType = cell_type   # cell_type -> integer
        self._coord = coord          # coord -> tuple
        self.__image = None
        self.__color = (0, 0, 0)
        self.drawMode = 1

    def set_texture(self, towerPower=None):
        if self.__cellType == 0:
            self.__image = pygame.image.load(r'images/wasteland.jpg').convert()

        elif self.__cellType == 1:
            self.__image = pygame.image.load(r'images/road.jpg').convert()

        elif self.__cellType == 2 and towerPower is not None:
            self.__color = (255, 15 * towerPower, 15 * towerPower)

        elif self.__cellType == 5000:
            self.__image = pygame.image.load(r'images/castle.jpg').convert()

        elif self.__cellType == -5000:
            self.__image = pygame.image.load(r'images/portal.jpg').convert()

        else:
            raise Exception('Unknown type of cell')

    def draw_cell(self, screen, cellType):

        coord = self._coord[0] * 40, self._coord[1] * 40
        if cellType == 1:
            screen.blit(self.__image, coord)
        else:
            pygame.draw.rect(screen, self.__color, [coord[0], coord[1], 40, 40])

    def get_coord(self):
        return self._coord


class Tower(Cell):
    def __init__(self, cell_type, coord):
        Cell.__init__(self, cell_type, coord)
        self.__power = 0
        self.range = 2
        self.drawMode = 2

    def calc_power(self):
        x, y = self.get_coord()

        # top
        if GameBoard.BOARD_CELLS[x][y - self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x + 1][y - self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x + 2][y - self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x - 1][y - self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x - 2][y - self.range] == 1:
            self.__power += 1

        # right
        if GameBoard.BOARD_CELLS[x + self.range][y - 1] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x + self.range][y] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x + self.range][y + 1] == 1:
            self.__power += 1

        # bottom
        if GameBoard.BOARD_CELLS[x][y + self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x + 1][y + self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x + 2][y + self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x - 1][y + self.range] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x - 2][y + self.range] == 1:
            self.__power += 1

        # left
        if GameBoard.BOARD_CELLS[x - self.range][y - 1] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x - self.range][y] == 1:
            self.__power += 1
        if GameBoard.BOARD_CELLS[x - self.range][y + 1] == 1:
            self.__power += 1

        return self.__power


class GameBoard:
    """
       Docstring
    """
    BOARD_CELLS = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -5000, 0],  # 1
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 3
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 4
        [0, 1, 0, 1, 0, 2, 2, 2, 2, 0, 1, 0, 2, 2, 2, 2, 2, 0, 1, 0],  # 5
        [0, 1, 0, 1, 0, 2, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 6
        [0, 1, 0, 1, 0, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],  # 7
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],  # 8
        [0, 1, 0, 1, 1, 1, 1, 1, 5000, 0, 2, 2, 2, 2, 2, 0, 0, 1, 1, 0],  # 9
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0],  # 10
        [0, 1, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 11
        [0, 1, 0, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 12
        [0, 1, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 13
        [0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0],  # 14
        [0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0],  # 15
        [0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0],  # 16
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 17
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 18
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 19
    ]

    def __init__(self):
        self.cells = []
        self.start = (0, 0)             # start -> tuple
        self.end = (0, 0)                 # end -> tuple

    def __parse_board(self):
        i = 0
        for row in self.BOARD_CELLS:
            j = 0
            for cell in row:
                if cell == 2:
                    tw = Tower(cell, (i, j))
                    twPow = tw.calc_power()
                    tw.set_texture(twPow)
                    self.cells.append(tw)
                else:
                    cl = Cell(cell, (i, j))
                    cl.set_texture()
                    self.cells.append(cl)
                j += 1
            i += 1

    def draw_board(self, screen):
        self.__parse_board()
        for cell in self.cells:
            cell.draw_cell(screen, cell.drawMode)

