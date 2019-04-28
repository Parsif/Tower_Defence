import pygame
from collections import deque
import board_matrix


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

        coord = self._coord['x'] * 40, self._coord['y'] * 40
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
        coord = self.get_coord()
        x = coord['x']
        y = coord['y']

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
    BOARD_CELLS = board_matrix.BOARD_CELLS

    def __init__(self):
        self.__cells = []
        self.__start = {'x': 0, 'y': 0}
        self.__end = {'x': 0, 'y': 0}
        self.__parse_board()

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end

    def __parse_board(self):
        i = 0
        for row in self.BOARD_CELLS:
            j = 0
            for cell in row:
                if cell == -5000:
                    self.__start['x'] = i
                    self.__start['y'] = j
                elif cell == 5000:
                    self.__end['x'] = i
                    self.__end['y'] = j

                if cell == 2:
                    tw = Tower(cell, {'x': i, 'y': j})
                    tw_pow = tw.calc_power()
                    tw.set_texture(tw_pow)
                    self.__cells.append(tw)
                else:
                    cl = Cell(cell, {'x': i, 'y': j})
                    cl.set_texture()
                    self.__cells.append(cl)
                j += 1
            i += 1

    def draw_board(self, screen):
        for cell in self.__cells:
            cell.draw_cell(screen, cell.drawMode)

    def __mark_path(self):
        board = self.BOARD_CELLS
        queue = deque()
        queue.append(self.__start)
        d = 4
        while len(queue) > 0:
            tmp = queue.popleft()
            res = self.__is_moving_top(tmp)
            if res[0]:
                queue.append(res[1])
            res = self.__is_moving_right(tmp)
            if res[0]:
                queue.append(res[1])
            res = self.__is_moving_bottom(tmp)
            if res[0]:
                queue.append(res[1])
            res = self.__is_moving_left(tmp)
            if res[0]:
                queue.append(res[1])

            board[tmp['x']][tmp['y']] = d
            d += 1

        return board

    def get_path(self):
        board = self.__mark_path()
        path = [self.__end]
        neighbours = self.__find_neighbours(self.__end, board)
        neighbours.sort(key=lambda nb: board[nb['x']][nb['y']])
        cur = neighbours[0]

        while cur['x'] != self.__start['x'] or cur['y'] != self.__start['y']:
            path.append(cur)
            neighbours = self.__find_neighbours(cur, board)
            neighbours.sort(key=lambda nb: board[nb['x']][nb['y']])
            cur = neighbours[0]

        path.reverse()
        return path

    def __is_moving_top(self, coord: dict) -> tuple:
        if self.BOARD_CELLS[coord['x']][coord['y'] - 1] == 1:
            return (True, {
                'x': coord['x'],
                'y': coord['y'] - 1
            })

        return False, None

    def __is_moving_right(self, coord: dict) -> tuple:
        if self.BOARD_CELLS[coord['x'] + 1][coord['y']] == 1:
            return (True, {
                'x': coord['x'] + 1,
                'y': coord['y']
            })

        return False, None

    def __is_moving_bottom(self, coord: dict) -> tuple:
        if self.BOARD_CELLS[coord['x']][coord['y'] + 1] == 1:
            return (True, {
                'x': coord['x'],
                'y': coord['y'] + 1
            })

        return False, None

    def __is_moving_left(self, coord: dict) -> tuple:
        if self.BOARD_CELLS[coord['x'] - 1][coord['y']] == 1:
            return (True, {
                'x': coord['x'] - 1,
                'y': coord['y']
            })

        return False, None

    @staticmethod
    def __find_neighbours(coord: dict, board: list) -> list:
        x, y = coord['x'], coord['y']
        neighbours = []

        if y + 1 < len(board) and board[x][y + 1] > 2:
            neighbours.append({'x': x, 'y': y + 1})
        if y - 1 > 0 and board[x][y - 1] > 2:
            neighbours.append({'x': x, 'y': y - 1})
        if x + 1 < len(board) and board[x + 1][y] > 2:
            neighbours.append({'x': x + 1, 'y': y})
        if x - 1 > 0 and board[x - 1][y] > 2:
            neighbours.append({'x': x - 1, 'y': y})

        return neighbours
