import pygame

import helper_modules.game_dsp as GD
from helper_modules.board_matrix import board1_img, board2_img, BoardTypes
from helper_modules.sound import Sound


class Button:
    """
        Docstring
    """
    def __init__(self, width, height, x, y, color=(100, 100, 0)):
        self._colorOrig = color
        self._color = color
        self._width = width
        self._height = height
        self._x = x
        self._y = y

    def draw(self, screen, font_size, text='',  outLine=None):
        pygame.draw.rect(screen, self._color, (self._x, self._y, self._width, self._height))
        if text != '':
            font = pygame.font.SysFont('impact', font_size)
            text = font.render(text, 1, (0, 0, 0))
            screen.blit(text, (self._x + (self._width / 2 - text.get_width() / 2),
                               self._y + (self._height / 2 - text.get_height() / 2)))

    def set_color(self, color=None):
        if color is None:
            self._color = self._colorOrig
        else:
            self._color = color

    def is_hovered(self, m_pos):
        if self._x < m_pos[0] < self._x + self._width:
            if self._y < m_pos[1] < self._y + self._height:
                return True

        return False


class MapChoice:
    """
        Docstring
    """

    def __init__(self, screen):
        self.bgImage = pygame.image.load(
            r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/menu/main_menu_background.png')
        self._screen = screen
        self._headerFont = pygame.font.SysFont('impact', 80)
        self._txtFont = pygame.font.SysFont('impact', 40)
        self._txtColor = (0, 0, 0)
        self.is_exit = False
        self._playBtn = Button(200, 75, 750, 650)
        self._backBtn = Button(200, 75, 50, 650)

        self._firstMapBtn = Button(200, 200, 100, 250)
        self._secondMapBtn = Button(200, 200, 400, 250)
        self._thirdMapBtn = Button(200, 200, 700, 250)

        self._soundMod = True

    def show_menu(self):
        is_running = True
        is_btn1_pressed = False
        is_btn2_pressed = False
        is_btn3_pressed = False

        while is_running and not self.is_exit:
            self._screen.blit(self.bgImage, (0, 0))
            # self.__show_text()
            self._firstMapBtn.draw(self._screen, 40)
            self._secondMapBtn.draw(self._screen, 40)
            self._thirdMapBtn.draw(self._screen, 40)
            self._playBtn.draw(self._screen, 40, 'Play')
            self._backBtn.draw(self._screen, 40, 'Back')

            self._screen.blit(board1_img, (100, 250))
            self._screen.blit(board2_img, (400, 250))
            # self._screen.blit(board3_img, (730, 280))
            mapTxt1 = self._txtFont.render('Random', 1, self._txtColor)
            self._screen.blit(mapTxt1, (735, 300))

            mapTxt2 = self._txtFont.render('Generated', 1, self._txtColor)
            self._screen.blit(mapTxt2, (720, 350))

            dsp = self._headerFont.render('Choose Map', 1, self._txtColor)
            self._screen.blit(dsp, (self._screen.get_width() / 3, 100))

            if is_btn1_pressed:
                pygame.draw.rect(self._screen, (0, 0, 255), (98, 248, 204, 204), 2)
            elif is_btn2_pressed:
                pygame.draw.rect(self._screen, (0, 0, 255), (398, 248, 204, 204), 2)
            elif is_btn3_pressed:
                pygame.draw.rect(self._screen, (0, 0, 255), (698, 248, 204, 204), 2)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self._playBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return True

                    elif self._backBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return False

                    elif self._firstMapBtn.is_hovered(m_pos):
                        is_btn1_pressed = True
                        BoardTypes.choice = 1
                        is_btn2_pressed = False
                        is_btn3_pressed = False
                        Sound.btnClick.play()

                    elif self._secondMapBtn.is_hovered(m_pos):
                        is_btn2_pressed = True
                        BoardTypes.choice = 2

                        is_btn1_pressed = False
                        is_btn3_pressed = False

                        Sound.btnClick.play()

                    elif self._thirdMapBtn.is_hovered(m_pos):
                        is_btn3_pressed = True
                        BoardTypes.choice = 3

                        is_btn1_pressed = False
                        is_btn2_pressed = False

                        Sound.btnClick.play()

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
        self._backToMenu = Button(200, 75, 200, 525)
        self._exitBtn = Button(200, 75, 200, 625)
        self._soundBtn = Button(200, 75, 500, 525)
        self._profileBtn = Button(200, 75, 500, 625)

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

        if self._backToMenu.is_hovered(m_pos):
            self._backToMenu.set_color((0, 255, 0))
        else:
            self._backToMenu.set_color((100, 100, 0))

        if self._soundBtn.is_hovered(m_pos):
            self._soundBtn.set_color((50, 50, 200))
        else:
            self._soundBtn.set_color((100, 100, 0))

        if self._profileBtn.is_hovered(m_pos):
            self._profileBtn.set_color((50, 50, 200))
        else:
            self._profileBtn.set_color((100, 100, 0))

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
            self._backToMenu.draw(self.screen, 40, 'Play')
            self._soundBtn.draw(self.screen, 40, f'Sound {sound_str}')
            self._profileBtn.draw(self.screen, 40, 'Profile')

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self._exitBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        self.is_exit = True
                        break

                    elif self._backToMenu.is_hovered(m_pos):
                        Sound.btnClick.play()
                        MC = MapChoice(self.screen)
                        if MC.show_menu():
                            self.is_exit = MC.is_exit
                            is_running = False
                            break

                    elif self._soundBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        Sound.soundMode = not Sound.soundMode

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
