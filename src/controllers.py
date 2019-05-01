import pygame

import helper_modules.game_dsp as GD
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


class MenuObject:
    """
        Docstring
    """

    def __init__(self, screen):
        self._bgImage = pygame.image.load(r'images/menu/main_menu_background.png')
        self._screen = screen
        self.__headerFont = pygame.font.SysFont('impact', 80)
        self.__font = pygame.font.SysFont('impact', 24)
        self.__txtColor = (0, 0, 0)
        self._is__exit = False
        self._playBtn = Button(200, 75, 200, 525)
        self._exitBtn = Button(200, 75, 200, 625)
        self._soundBtn = Button(200, 75, 500, 525)
        self.__soundMod = True

    @property
    def get_is_exit(self):
        return self._is__exit

    def __show_text(self):
        header = self.__headerFont.render('Tower Defence!', 1, self.__txtColor)
        self._screen.blit(header, (self._screen.get_width() / 4, 75))

        marginTop = 175
        for txt_row in GD.desc:
            dsp = self.__font.render(txt_row, 1, self.__txtColor)
            self._screen.blit(dsp, (self._screen.get_width() / 5, marginTop))
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

    def show_menu(self):
        is_running = True
        while is_running and not self._is__exit:
            Sound.soundMode = self.__soundMod
            if self.__soundMod:
                sound_str = 'on'
            else:
                sound_str = 'off'
            self._screen.blit(self._bgImage, (0, 0))
            self.__show_text()
            self._exitBtn.draw(self._screen, 40, 'Exit')
            self._playBtn.draw(self._screen, 40, 'Play')
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
                        self.__soundMod = not self.__soundMod

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
                        print(Sound.soundMode)
                        Sound.soundMode = not Sound.soundMode
                        print(Sound.soundMode)

                if event.type == pygame.QUIT:
                    self._is__exit = True
                    is_running = False
                    break

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    self._btns_hovered(m_pos)

            pygame.display.update()
