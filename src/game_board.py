from collections import deque
from copy import deepcopy

from helper_modules import board_matrix
from src.cell import Cell, Tower, Castle


class GameBoard:
    """
       Docstring
    """
    paths = []

    def __init__(self):
        self._cells = []
        self._start = []
        self._end = {'x': 0, 'y': 0}
        self._Castle = None
        self._towers = []
        self.BM = board_matrix.BoardTypes()
        if self.BM.choice == 3:
            self.BM.generate_board()
        self.BOARD_CELLS = self.BM.get_board()
        self._parse_board()
        self._marked_board = []

    @property
    def get_start(self):
        return self._start

    @property
    def get_end(self):
        return self._end

    @property
    def get_castle(self):
        return self._Castle

    @property
    def get_towers(self):
        return self._towers

    def clean_board(self):
        for cell in self._cells:
            cnt = 0
            for path in self.paths:
                if cell.coord not in path:
                    cnt += 1
            if cnt == len(self.paths):
                x, y = cell.coord['x'], cell.coord['y']
                flag = True  # checking portal
                for st in self._start:
                    if x == st['x'] and y == st['y']:
                        flag = False
                if flag:
                    self._cells[x * len(self.BOARD_CELLS[0]) + y] = Cell(0, {'x': x, 'y': y})
                    self._marked_board[x][y] = 0

    def set_towers(self):
        reachable = [1, -5000, 5000]
        for i in range(len(self._marked_board)):
            for j in range(len(self._marked_board[0])):
                if i - 1 >= 0 and self._marked_board[i - 1][j] == 0 and self._marked_board[i][j] not in reachable:
                    if i + 1 < len(self._marked_board) and self._marked_board[i + 1][j] == 0:
                        if j + 1 < len(self._marked_board[0]) and self._marked_board[i][j + 1] == 0:
                            if j - 1 >= 0 and self._marked_board[i][j - 1] == 0:
                                if i - 2 >= 0 and self._marked_board[i - 2][j] > 10:
                                    tw = Tower(2, {'x': i, 'y': j})
                                    self._towers.append(tw)
                                elif i + 2 < len(self._marked_board) and self._marked_board[i + 2][j] > 10:
                                    tw = Tower(2, {'x': i, 'y': j})
                                    self._towers.append(tw)
                                elif j + 2 < len(self._marked_board[0]) and self._marked_board[i][j + 2] > 10:
                                    tw = Tower(2, {'x': i, 'y': j})
                                    self._towers.append(tw)
                                elif j - 2 >= 0 and self._marked_board[i][j - 2] > 10:
                                    tw = Tower(2, {'x': i, 'y': j})
                                    self._towers.append(tw)

    def _parse_board(self):
        i = 0
        for row in self.BOARD_CELLS:
            j = 0
            for cell in row:
                if cell == 5000:
                    self._Castle = Castle(cell, {'x': i, 'y': j})
                    self._cells.append(self._Castle)
                    self._end['x'] = i
                    self._end['y'] = j

                elif cell == 2:
                    tw = Tower(cell, {'x': i, 'y': j})
                    self._towers.append(tw)
                else:
                    if cell == -5000:
                        self._start.append({'x': i, 'y': j})
                    cl = Cell(cell, {'x': i, 'y': j})
                    self._cells.append(cl)
                j += 1
            i += 1

    def draw(self, screen, towers):
        for cell in self._cells:
            cell.draw(screen)
        for tower in towers:
            if tower.get_build_cnt == 0:
                tower.draw(screen)

    def _mark_path(self, start):
        board = deepcopy(self.BOARD_CELLS)
        queue = deque()
        queue.append(start)
        d = 4
        while len(queue) > 0:
            tmp = queue.popleft()
            res = self._is_moving_top(tmp, board)
            if res[0]:
                if res[1] not in queue:
                    queue.append(res[1])
            res = self._is_moving_right(tmp, board)
            if res[0]:
                if res[1] not in queue:
                    queue.append(res[1])
            res = self._is_moving_bottom(tmp, board)
            if res[0]:
                if res[1] not in queue:
                    queue.append(res[1])
            res = self._is_moving_left(tmp, board)
            if res[0]:
                if res[1] not in queue:
                    queue.append(res[1])

            board[tmp['x']][tmp['y']] = d
            d += 1

        self._marked_board = board
        return board

    def get_path(self, start):
        board = self._mark_path(start)
        path = [self._end]
        neighbours = self.__find_neighbours(self._end, board)
        neighbours.sort(key=lambda nb: board[nb['x']][nb['y']])
        cur = neighbours[0]

        while cur['x'] != start['x'] or cur['y'] != start['y']:
            path.append(cur)
            neighbours = self.__find_neighbours(cur, board)
            neighbours.sort(key=lambda nb: board[nb['x']][nb['y']])
            cur = neighbours[0]

        path.reverse()
        self.paths.append(path)

        return path

    @staticmethod
    def _is_moving_top(coord: dict, board) -> tuple:
        if coord['y'] - 1 >= 0 and board[coord['x']][coord['y'] - 1] == 1:
            return (True, {
                'x': coord['x'],
                'y': coord['y'] - 1
            })

        return False, None

    @staticmethod
    def _is_moving_right(coord: dict, board) -> tuple:
        if coord['x'] + 1 < len(board) and board[coord['x'] + 1][coord['y']] == 1:
            return (True, {
                'x': coord['x'] + 1,
                'y': coord['y']
            })

        return False, None

    @staticmethod
    def _is_moving_bottom(coord: dict, board) -> tuple:
        if coord['y'] + 1 < len(board[0]) and board[coord['x']][coord['y'] + 1] == 1:
            return (True, {
                'x': coord['x'],
                'y': coord['y'] + 1
            })

        return False, None

    @staticmethod
    def _is_moving_left(coord: dict, board) -> tuple:
        if coord['x'] - 1 >= 0 and board[coord['x'] - 1][coord['y']] == 1:
            return (True, {
                'x': coord['x'] - 1,
                'y': coord['y']
            })

        return False, None

    @staticmethod
    def __find_neighbours(coord: dict, board: list) -> list:
        x, y = coord['x'], coord['y']
        neighbours = []

        if y + 1 < len(board[0]) and board[x][y + 1] > 2:
            neighbours.append({'x': x, 'y': y + 1})
        if y - 1 >= 0 and board[x][y - 1] > 2:
            neighbours.append({'x': x, 'y': y - 1})
        if x + 1 < len(board) and board[x + 1][y] > 2:
            neighbours.append({'x': x + 1, 'y': y})
        if x - 1 >= 0 and board[x - 1][y] > 2:
            neighbours.append({'x': x - 1, 'y': y})

        return neighbours
