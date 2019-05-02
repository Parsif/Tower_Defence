import pygame

import helper_modules.game_dsp as GD
from helper_modules.board_matrix import board1_img, board2_img, board3_img, BoardTypes
from helper_modules.sound import Sound


class Button:
    """
        Docstring
    """
    def __init__(self, width, height, x, y, color=(100, 100, 0)):
        self.__colorOrig = color
        self.__color = color
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y

    def draw(self, screen, font_size, text='',  outLine=None):
        pygame.draw.rect(screen, self.__color, (self.__x, self.__y, self.__width, self.__height))
        if text != '':
            font = pygame.font.SysFont('impact', font_size)
            text = font.render(text, 1, (0, 0, 0))
            screen.blit(text, (self.__x + (self.__width / 2 - text.get_width() / 2),
                                           self.__y + (self.__height / 2 - text.get_height() / 2)))

    def set_color(self, color=None):
        if color is None:
            self.__color = self.__colorOrig
        else:
            self.__color = color

    def is_hovered(self, m_pos):
        if self.__x < m_pos[0] < self.__x + self.__width:
            if self.__y < m_pos[1] < self.__y + self.__height:
                return True

        return False


class MapChoice:
    """
        Docstring
    """

    def __init__(self, screen):
        self._bgImage = pygame.image.load(r'images/menu/main_menu_background.png')
        self.__screen = screen
        self.__headerFont = pygame.font.SysFont('impact', 80)
        self.__txtColor = (0, 0, 0)
        self.is__exit = False
        self.__playBtn = Button(200, 75, 750, 650)
        self.__backBtn = Button(200, 75, 50, 650)

        self.__firstMapBtn = Button(200, 200, 100, 250)
        self.__secondMapBtn = Button(200, 200, 400, 250)
        self.__thirdMapBtn = Button(200, 200, 700, 250)

        self.__soundMod = True

    def show_menu(self):
        is_running = True
        is_btn1_pressed = False
        is_btn2_pressed = False
        is_btn3_pressed = False

        while is_running and not self.is__exit:
            self.__screen.blit(self._bgImage, (0, 0))
            # self.__show_text()
            self.__firstMapBtn.draw(self.__screen, 40)
            self.__secondMapBtn.draw(self.__screen, 40)
            self.__thirdMapBtn.draw(self.__screen, 40)
            self.__playBtn.draw(self.__screen, 40, 'Play')
            self.__backBtn.draw(self.__screen, 40, 'Back')

            self.__screen.blit(board1_img, (100, 250))
            self.__screen.blit(board2_img, (400, 250))
            self.__screen.blit(board3_img, (700, 250))

            dsp = self.__headerFont.render('Choose Map', 1, self.__txtColor)
            self.__screen.blit(dsp, (self.__screen.get_width() / 3, 100))

            if is_btn1_pressed:
                pygame.draw.rect(self.__screen, (0, 0, 255), (98, 248, 204, 204), 2)
            elif is_btn2_pressed:
                pygame.draw.rect(self.__screen, (0, 0, 255), (398, 248, 204, 204), 2)
            elif is_btn3_pressed:
                pygame.draw.rect(self.__screen, (0, 0, 255), (698, 248, 204, 204), 2)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self.__playBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return True

                    elif self.__backBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return False

                    elif self.__firstMapBtn.is_hovered(m_pos):
                        is_btn1_pressed = True
                        BoardTypes.choice = 1
                        is_btn2_pressed = False
                        is_btn3_pressed = False
                        Sound.btnClick.play()

                    elif self.__secondMapBtn.is_hovered(m_pos):
                        is_btn2_pressed = True
                        BoardTypes.choice = 2

                        is_btn1_pressed = False
                        is_btn3_pressed = False

                        Sound.btnClick.play()

                    elif self.__thirdMapBtn.is_hovered(m_pos):
                        is_btn3_pressed = True
                        BoardTypes.choice = 3

                        is_btn1_pressed = False
                        is_btn2_pressed = False

                        Sound.btnClick.play()

                if event.type == pygame.QUIT:
                    self.is__exit = True
                    return True

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    if self.__playBtn.is_hovered(m_pos):
                        self.__playBtn.set_color((255, 255, 0))
                    else:
                        self.__playBtn.set_color((100, 100, 0))

                    if self.__backBtn.is_hovered(m_pos):
                        self.__backBtn.set_color((255, 0, 0))
                    else:
                        self.__backBtn.set_color((100, 100, 0))

            pygame.display.update()


class MenuObject:
    """
        Docstring
    """

    def __init__(self, screen):
        self._bgImage = pygame.image.load(r'images/menu/main_menu_background.png')
        self._screen = screen
        self._headerFont = pygame.font.SysFont('impact', 80)
        self.__font = pygame.font.SysFont('impact', 24)
        self._txtColor = (0, 0, 0)
        self._is__exit = False
        self.__backToMenu = Button(200, 75, 200, 525)
        self.__exitBtn = Button(200, 75, 200, 625)
        self._soundBtn = Button(200, 75, 500, 525)

    @property
    def get_is_exit(self):
        return self._is__exit

    def __show_text(self):
        header = self._headerFont.render('Tower Defence!', 1, self._txtColor)
        self._screen.blit(header, (self._screen.get_width() / 4, 75))

        marginTop = 175
        for txt_row in GD.desc:
            dsp = self.__font.render(txt_row, 1, self._txtColor)
            self._screen.blit(dsp, (self._screen.get_width() / 5, marginTop))
            marginTop += 50

    def _btns_hovered(self, m_pos):
        if self.__exitBtn.is_hovered(m_pos):
            self.__exitBtn.set_color((255, 0, 0))
        else:
            self.__exitBtn.set_color((100, 100, 0))

        if self.__backToMenu.is_hovered(m_pos):
            self.__backToMenu.set_color((0, 255, 0))
        else:
            self.__backToMenu.set_color((100, 100, 0))

        if self._soundBtn.is_hovered(m_pos):
            self._soundBtn.set_color((50, 50, 200))
        else:
            self._soundBtn.set_color((100, 100, 0))

    def show_menu(self):
        is_running = True
        while is_running and not self._is__exit:
            if Sound.soundMode:
                sound_str = 'on'
            else:
                sound_str = 'off'
            self._screen.blit(self._bgImage, (0, 0))
            self.__show_text()
            self.__exitBtn.draw(self._screen, 40, 'Exit')
            self.__backToMenu.draw(self._screen, 40, 'Play')
            self._soundBtn.draw(self._screen, 40, f'Sound {sound_str}')

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self.__exitBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        self._is__exit = True
                        break

                    elif self.__backToMenu.is_hovered(m_pos):
                        Sound.btnClick.play()
                        MC = MapChoice(self._screen)
                        if MC.show_menu():
                            self._is__exit = MC.is__exit
                            is_running = False
                            break

                    elif self._soundBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        Sound.soundMode = not Sound.soundMode

                if event.type == pygame.QUIT:
                    self._is__exit = True
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

    def __init__(self, screen):
        MenuObject.__init__(self, screen)
        self._playBtn = Button(200, 75, self._screen.get_width() / 2 - 100, 175)
        self._exitBtn = Button(200, 75, self._screen.get_width() / 2 - 100, 325)
        self._soundBtn = Button(200, 75, self._screen.get_width() / 2 - 100, 475)

    def show_menu(self):
        is_running = True
        while is_running and not self._is__exit:
            if Sound.soundMode:
                sound_str = 'on'
            else:
                sound_str = 'off'
            self._screen.blit(self._bgImage, (0, 0))
            self._exitBtn.draw(self._screen, 40, 'Exit')
            self._playBtn.draw(self._screen, 40, 'Resume')
            self._soundBtn.draw(self._screen, 40, f'Sound {sound_str}')

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self._exitBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        self._is__exit = True
                        break

                    elif self._playBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        is_running = False
                        break

                    elif self._soundBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        Sound.soundMode = not Sound.soundMode

                if event.type == pygame.QUIT:
                    self._is__exit = True
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

    def __init__(self, screen, bg_image, text):
        MenuObject.__init__(self, screen)
        self._bgImage = bg_image
        self.text = text
        self._txtColor = (255, 255, 255)
        self.__backToMenu = Button(200, 75, 100, 700)
        self.__exitBtn = Button(200, 75, 700, 700)

    def show_menu(self):
        is_running = True
        while is_running and not self._is__exit:

            self._screen.blit(self._bgImage, (0, 0))
            self.__exitBtn.draw(self._screen, 40, 'Exit')
            self.__backToMenu.draw(self._screen, 40, 'Menu')

            header = self._headerFont.render(self.text, 1, self._txtColor)
            self._screen.blit(header, (self._screen.get_width() / 2.5, 75))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self.__exitBtn.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return False

                    elif self.__backToMenu.is_hovered(m_pos):
                        Sound.btnClick.play()
                        return True

                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    if self.__exitBtn.is_hovered(m_pos):
                        self.__exitBtn.set_color((255, 0, 0))
                    else:
                        self.__exitBtn.set_color()

                    if self.__backToMenu.is_hovered(m_pos):
                        self.__backToMenu.set_color((255, 255, 0))
                    else:
                        self.__backToMenu.set_color()

            pygame.display.update()
