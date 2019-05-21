import pygame

import helper_modules.game_dsp as GD
from helper_modules.board_matrix import board1_img, board2_img, BoardTypes
from helper_modules.sound import Sound
from src.cell import Cell, EmptyCell, Tower, Castle


class Button:
    """
        Docstring
    """
    def __init__(self, width, height, x, y, color=(100, 100, 0)):
        self._colorOrig = color
        self._color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.is_pressed = None


    def draw(self, screen, font_size, text='',  outLine=None):
        pygame.draw.rect(screen, self._color, (self.x, self.y, self.width, self.height))
        if text != '':
            font = pygame.font.SysFont('impact', font_size)
            text = font.render(text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def set_color(self, color=None):
        if color is None:
            self._color = self._colorOrig
        else:
            self._color = color

    def is_hovered(self, m_pos):
        if self.x < m_pos[0] < self.x + self.width:
            if self.y < m_pos[1] < self.y + self.height:
                return True

        return False


class MapEditor:
    def __init__(self, screen, player):
        self._cells = []
        self._Player = player
        self._screen = screen
        self.is_exit = False
        self._saveBtn = Button(200, 75, 775, 25)
        self._backBtn = Button(200, 75, 25, 25)
        self._bgImg = pygame.image.load(
            r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/menu/main_menu_background.png')

    def parse_board(self):
        empty_board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 12
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 13
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 14
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 16
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 17
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 18
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 19
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 20
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 21
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 22
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 23
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 24
        ]
        for i in range(len(empty_board)):
            for j in range(len(empty_board[0])):

                tmp = self._cells[i * len(empty_board[0]) + j]
                if type(tmp) is Tower:
                    empty_board[i][j] = 2

                else:
                    empty_board[i][j] = tmp.cellType

        return empty_board

    def valid_board(self):
        pass

    def _choose_cell(self, cell):
        coord = cell.get_coord
        towerBtn = Button(60, 25, coord['x'] * cell.SIZE + cell.startX - 72, coord['y'] * cell.SIZE + cell.startY - 30,
                          (255, 255, 0))
        roadBtn = Button(60, 25, coord['x'] * cell.SIZE + cell.startX - 11, coord['y'] * cell.SIZE + cell.startY - 30,
                         (255, 255, 0))
        portalBtn = Button(60, 25, coord['x'] * cell.SIZE + cell.startX + 50, coord['y'] * cell.SIZE + cell.startY - 30,
                           (255, 255, 0))
        wstBtn = Button(60, 25, coord['x'] * cell.SIZE + cell.startX - 72, coord['y'] * cell.SIZE + cell.startY + 40,
                        (255, 255, 0))
        cstBtn = Button(60, 25, coord['x'] * cell.SIZE + cell.startX - 11, coord['y'] * cell.SIZE + cell.startY + 40,
                        (255, 255, 0))
        btns = [towerBtn, roadBtn, portalBtn, wstBtn, cstBtn]

        while True:
            towerBtn.draw(self._screen, 11, 'Tower')
            roadBtn.draw(self._screen, 11, 'Road')
            portalBtn.draw(self._screen, 11, 'Portal')
            wstBtn.draw(self._screen, 11, 'Wasteland')
            cstBtn.draw(self._screen, 11, 'Castle')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_exit = True
                    return None

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if btn.is_hovered(m_pos):
                            btn.set_color((0, 0, 200))
                        else:
                            btn.set_color()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if towerBtn.is_hovered(m_pos):
                        return 2
                    elif roadBtn.is_hovered(m_pos):
                        return 1
                    elif wstBtn.is_hovered(m_pos):
                        return 0
                    elif portalBtn.is_hovered(m_pos):
                        return -5000
                    elif cstBtn.is_hovered(m_pos):
                        return 5000

                    cell.set_color()
                    return None

            pygame.display.update()

    def draw_emtpy(self):
        for i in range(25):
            for j in range(20):
                self._cells.append(EmptyCell(0, {'x': i, 'y': j}))
        is_running = True
        while is_running and not self.is_exit:
            self._screen.blit(self._bgImg, (0, 0))
            for cell in self._cells:
                cell.draw(self._screen)
            self._saveBtn.draw(self._screen, 40, 'Save')
            self._backBtn.draw(self._screen, 40, 'Back')

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()

                    if self._saveBtn.is_hovered(m_pos):
                        board = self.parse_board()
                        self._Player.db_collection.update_one({'email': self._Player.email},
                                                              {'$push': {'boards': board}})

                        return self._cells

                    if self._backBtn.is_hovered(m_pos):
                        return True

                    for i in range(len(self._cells)):
                        if self._cells[i].is_hovered(m_pos):
                            choice = self._choose_cell(self._cells[i])
                            if choice == 0:
                                self._cells[i] = Cell(0, self._cells[i].coord)
                            elif choice == 1:
                                self._cells[i] = Cell(1, self._cells[i].coord)
                            elif choice == 2:
                                self._cells[i] = Tower(0, self._cells[i].coord)
                            elif choice == 5000:
                                flag = True  # checking for only one Castle
                                for cell in self._cells:
                                    if type(cell) is Castle:
                                        flag = False
                                if flag:
                                    self._cells[i] = Castle(5000, self._cells[i].coord)
                            elif choice == -5000:
                                self._cells[i] = Cell(-5000, self._cells[i].coord)
                            else:
                                break

                if event.type == pygame.QUIT:
                    self.is_exit = True
                    return False

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()

                    for cell in self._cells:
                        if type(cell) is EmptyCell:
                            if cell.is_hovered(m_pos):
                                cell.set_color((255, 0, 255))
                            else:
                                cell.set_color()

                    if self._saveBtn.is_hovered(m_pos):
                        self._saveBtn.set_color((255, 255, 0))
                    else:
                        self._saveBtn.set_color((100, 100, 0))

                    if self._backBtn.is_hovered(m_pos):
                        self._backBtn.set_color((255, 0, 0))
                    else:
                        self._backBtn.set_color((100, 100, 0))

            pygame.display.update()


class MapChoice:
    """
        Docstring
    """

    def __init__(self, screen, player):
        self._player = player
        self.bgImage = pygame.image.load(
            r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/menu/main_menu_background.png')
        self._screen = screen
        self._headerFont = pygame.font.SysFont('impact', 80)
        self._txtFont = pygame.font.SysFont('impact', 40)
        self._txtColor = (0, 0, 0)
        self.is_exit = False
        self._playBtn = Button(200, 75, 750, 700)
        self._backBtn = Button(200, 75, 50, 700)

        self._firstMapBtn = Button(200, 200, 100, 150)
        self._secondMapBtn = Button(200, 200, 400, 150)
        self._thirdMapBtn = Button(200, 200, 700, 150)

        self._soundMod = True

    def show_menu(self):
        is_running = True
        self._firstMapBtn.is_pressed = False
        self._secondMapBtn.is_pressed = False
        self._thirdMapBtn.is_pressed = False

        boards = self._player.userDoc['boards']
        btns = [
            self._firstMapBtn, self._secondMapBtn, self._thirdMapBtn,
        ]
        print(len(boards))
        print(len(BoardTypes.boards))

        tmpX, tmpY = 100, 450
        for board in boards:
            BoardTypes.boards.append(board)
            btns.append(Button(200, 200, tmpX, tmpY))
            tmpX += 300

        print(len(BoardTypes.boards))

        while is_running and not self.is_exit:
            self._screen.blit(self.bgImage, (0, 0))
            self._playBtn.draw(self._screen, 40, 'Play')
            self._backBtn.draw(self._screen, 40, 'Back')

            cnt = 0
            for btn in btns:
                cnt += 1
                btn.draw(self._screen, 40)
                if cnt <= 3:
                    continue
                mapTxt = self._txtFont.render(f'Map {cnt}', 1, self._txtColor)
                self._screen.blit(mapTxt, (btn.x + 50, btn.y + 70))

            self._screen.blit(board1_img, (100, 150))
            self._screen.blit(board2_img, (400, 150))

            mapTxt1 = self._txtFont.render('Random', 1, self._txtColor)
            self._screen.blit(mapTxt1, (735, 200))

            mapTxt2 = self._txtFont.render('Generated', 1, self._txtColor)
            self._screen.blit(mapTxt2, (720, 250))

            dsp = self._headerFont.render('Choose Map', 1, self._txtColor)
            self._screen.blit(dsp, (self._screen.get_width() / 3, 20))

            for btn in btns:
                if btn.is_pressed:
                    pygame.draw.rect(self._screen, (0, 0, 255), (btn.x - 2, btn.y - 2, 204, 204), 2)
                    self._screen.blit(mapTxt1, (735, 200))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self._playBtn.is_hovered(m_pos):
                        BT = BoardTypes()
                        BT.generate_board()
                        if btns[2].is_pressed:
                            BoardTypes.is_generated = True

                        Sound.btnClick.play()
                        return True

                    elif self._backBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return False

                    i = 0
                    for button in btns:
                        if button.is_hovered(m_pos):
                            Sound.btnClick.play()
                            for btn in btns:
                                btn.is_pressed = False
                            button.is_pressed = True
                            BoardTypes.choice = i
                        i += 1

                if event.type == pygame.QUIT:
                    self.is_exit = True
                    return True

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    if self._playBtn.is_hovered(m_pos):
                        self._playBtn.set_color((255, 255, 0))
                    else:
                        self._playBtn.set_color((100, 100, 0))

                    if self._backBtn.is_hovered(m_pos):
                        self._backBtn.set_color((255, 0, 0))
                    else:
                        self._backBtn.set_color((100, 100, 0))

            pygame.display.update()


class Profile:
    """
        Docstring
    """

    def __init__(self, screen, player):
        self._player = player
        self.bgImage = pygame.image.load(
            r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/menu/main_menu_background.png')
        self._screen = screen
        self._headerFont = pygame.font.SysFont('impact', 80)
        self._txtFont = pygame.font.SysFont('impact', 50)

        self._txtColor = (0, 0, 0)
        self.is_exit = False
        self.backBtn = Button(200, 75, 150, 650)

        self._soundMod = True

    def show_menu(self):
        is_running = True

        while is_running and not self.is_exit:
            self._screen.blit(self.bgImage, (0, 0))

            self.backBtn.draw(self._screen, 40, 'Back')

            header = self._headerFont.render('Profile', 1, self._txtColor)
            self._screen.blit(header, (self._screen.get_width() / 2.3, 50))

            header = self._txtFont.render(f'Games played: {self._player.userDoc["gmPlayed"]}', 1, self._txtColor)
            self._screen.blit(header, (self._screen.get_width() / 8, 170))

            header = self._txtFont.render(f'Games won: {self._player.userDoc["gmWon"]}', 1, self._txtColor)
            self._screen.blit(header, (self._screen.get_width() / 8, 250))

            header = self._txtFont.render(f'Games loose: {self._player.userDoc["gmLoose"]}', 1, self._txtColor)
            self._screen.blit(header, (self._screen.get_width() / 8, 330))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self.backBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return False

                if event.type == pygame.QUIT:
                    self.is_exit = True
                    return True

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    if self.backBtn.is_hovered(m_pos):
                        self.backBtn.set_color((255, 0, 0))
                    else:
                        self.backBtn.set_color((100, 100, 0))

            pygame.display.update()


class MenuObject:
    """
        Docstring
    """

    def __init__(self, screen, player):
        self._player = player
        self.bgImage = pygame.image.load(
            r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/menu/main_menu_background.png')
        self.screen = screen
        self.headerFont = pygame.font.SysFont('impact', 80)
        self._font = pygame.font.SysFont('impact', 24)
        self.txtColor = (0, 0, 0)
        self.is_exit = False
        self._playBtn = Button(200, 75, 100, 525)
        self._exitBtn = Button(200, 75, 100, 625)
        self._soundBtn = Button(200, 75, 400, 525)
        self._profileBtn = Button(200, 75, 400, 625)
        self._createMapBtn = Button(200, 75, 700, 525)



    @property
    def get_is_exit(self):
        return self.is_exit

    def __show_text(self):
        header = self.headerFont.render('Tower Defence!', 1, self.txtColor)
        self.screen.blit(header, (self.screen.get_width() / 4, 75))

        marginTop = 175
        for txt_row in GD.desc:
            dsp = self._font.render(txt_row, 1, self.txtColor)
            self.screen.blit(dsp, (self.screen.get_width() / 5, marginTop))
            marginTop += 50

    def _btns_hovered(self, m_pos):
        if self._exitBtn.is_hovered(m_pos):
            self._exitBtn.set_color((255, 0, 0))
        else:
            self._exitBtn.set_color((100, 100, 0))

        if self._playBtn.is_hovered(m_pos):
            self._playBtn.set_color((0, 255, 0))
        else:
            self._playBtn.set_color((100, 100, 0))

        if self._soundBtn.is_hovered(m_pos):
            self._soundBtn.set_color((50, 50, 200))
        else:
            self._soundBtn.set_color((100, 100, 0))

        if self._profileBtn.is_hovered(m_pos):
            self._profileBtn.set_color((50, 50, 200))
        else:
            self._profileBtn.set_color((100, 100, 0))

        if self._createMapBtn.is_hovered(m_pos):
            self._createMapBtn.set_color((50, 50, 200))
        else:
            self._createMapBtn.set_color((100, 100, 0))

    def show_menu(self):
        is_running = True
        while is_running and not self.is_exit:
            if Sound.soundMode:
                sound_str = 'on'
            else:
                sound_str = 'off'
            self.screen.blit(self.bgImage, (0, 0))
            self.__show_text()
            self._exitBtn.draw(self.screen, 40, 'Exit')
            self._playBtn.draw(self.screen, 40, 'Play')
            self._soundBtn.draw(self.screen, 40, f'Sound {sound_str}')
            self._profileBtn.draw(self.screen, 40, 'Profile')
            self._createMapBtn.draw(self.screen, 40, 'Custom')

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self._exitBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        self.is_exit = True
                        break

                    elif self._playBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        MC = MapChoice(self.screen, self._player)
                        if MC.show_menu():
                            self.is_exit = MC.is_exit
                            is_running = False
                            break

                    elif self._soundBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        Sound.soundMode = not Sound.soundMode

                    elif self._createMapBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        MP = MapEditor(self.screen, self._player)
                        val = MP.draw_emtpy()

                        if not val:
                            self.is_exit = True
                            is_running = False
                            break

                    elif self._profileBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        lg = Profile(self.screen, self._player)
                        if lg.show_menu():
                            self.is_exit = lg.is_exit
                            is_running = False
                            break

                if event.type == pygame.QUIT:
                    self.is_exit = True
                    is_running = False
                    break

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    self._btns_hovered(m_pos)

            pygame.display.update()


class PauseMenu(MenuObject):
    """
         Docstring
    """

    def __init__(self, screen, player):
        MenuObject.__init__(self, screen, player)
        self._playBtn = Button(200, 75, self.screen.get_width() / 2 - 100, 175)
        self._exitBtn = Button(200, 75, self.screen.get_width() / 2 - 100, 325)
        self._soundBtn = Button(200, 75, self.screen.get_width() / 2 - 100, 475)

    def show_menu(self):
        is_running = True
        while is_running and not self.is_exit:
            if Sound.soundMode:
                sound_str = 'on'
            else:
                sound_str = 'off'
            self.screen.blit(self.bgImage, (0, 0))
            self._exitBtn.draw(self.screen, 40, 'Exit')
            self._playBtn.draw(self.screen, 40, 'Resume')
            self._soundBtn.draw(self.screen, 40, f'Sound {sound_str}')

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self._exitBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        self.is_exit = True
                        break

                    elif self._playBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        is_running = False
                        break

                    elif self._soundBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        Sound.soundMode = not Sound.soundMode

                if event.type == pygame.QUIT:
                    self.is_exit = True
                    is_running = False
                    break

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()

                    if self._playBtn.is_hovered(m_pos):
                        self._playBtn.set_color((255, 255, 0))
                    else:
                        self._playBtn.set_color()

                    if self._exitBtn.is_hovered(m_pos):
                        self._exitBtn.set_color((255, 0, 0))
                    else:
                        self._exitBtn.set_color()

                    if self._soundBtn.is_hovered(m_pos):
                        self._soundBtn.set_color((0, 0, 255))
                    else:
                        self._soundBtn.set_color()

            pygame.display.update()


class EndGameMenu(MenuObject):
    """
        Docstring
    """

    def __init__(self, screen, player, bg_image, text):
        MenuObject.__init__(self, screen, player)
        self._bgImage = bg_image
        self.text = text
        self._txtColor = (255, 255, 255)
        self._backToMenu = Button(200, 75, 100, 700)
        self._exitBtn = Button(200, 75, 700, 700)

    def show_menu(self):
        is_running = True
        while is_running and not self.is_exit:

            self.screen.blit(self._bgImage, (0, 0))
            self._exitBtn.draw(self.screen, 40, 'Exit')
            self._backToMenu.draw(self.screen, 40, 'Menu')

            header = self.headerFont.render(self.text, 1, self._txtColor)
            self.screen.blit(header, (self.screen.get_width() / 2.5, 75))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self._exitBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return False

                    elif self._backToMenu.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return True

                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    if self._exitBtn.is_hovered(m_pos):
                        self._exitBtn.set_color((255, 0, 0))
                    else:
                        self._exitBtn.set_color()

                    if self._backToMenu.is_hovered(m_pos):
                        self._backToMenu.set_color((255, 255, 0))
                    else:
                        self._backToMenu.set_color()

            pygame.display.update()
