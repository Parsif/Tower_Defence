import pygame
import helper_modules.game_dsp as GD

class Button:
    """
        Docstring
    """
    def __init__(self, width, height, x, y, color=(100, 100, 0)):
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

    def set_color(self, color):
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
        self.__bgImage = pygame.image.load(r'images/menu/main_menu_background.png')
        self.__screen = screen
        self.__headerFont = pygame.font.SysFont('impact', 80)
        self.__font = pygame.font.SysFont('impact', 24)
        self.__txtColor = (0, 0, 0)
        self.__is__exit = False
        self.__playBtn = Button(200, 75, 200, 525)
        self.__exitBtn = Button(200, 75, 200, 625)
        self.__soundBtn = Button(200, 75, 500, 525)
        self.__soundMod = True

    @property
    def get_is_exit(self):
        return self.__is__exit

    @property
    def get_sound_mod(self):
        return self.__soundMod

    def __show_text(self):
        header = self.__headerFont.render('Tower Defence!', 1, self.__txtColor)
        self.__screen.blit(header, (self.__screen.get_width() / 4, 75))

        marginTop = 175
        for txt_row in GD.desc:
            dsp = self.__font.render(txt_row, 1, self.__txtColor)
            self.__screen.blit(dsp, (self.__screen.get_width() / 5, marginTop))
            marginTop += 50

    def __btns_hovered(self, m_pos):
        if self.__exitBtn.is_hovered(m_pos):
            self.__exitBtn.set_color((255, 0, 0))
        else:
            self.__exitBtn.set_color((100, 100, 0))

        if self.__playBtn.is_hovered(m_pos):
            self.__playBtn.set_color((0, 255, 0))
        else:
            self.__playBtn.set_color((100, 100, 0))

        if self.__soundBtn.is_hovered(m_pos):
            self.__soundBtn.set_color((50, 50, 200))
        else:
            self.__soundBtn.set_color((100, 100, 0))

    def show_menu(self):
        is_running = True
        while is_running and not self.__is__exit:
            if self.__soundMod:
                sound_str = 'on'
            else:
                sound_str = 'off'
            self.__screen.blit(self.__bgImage, (0, 0))
            self.__show_text()
            self.__exitBtn.draw(self.__screen, 40, 'Exit')
            self.__playBtn.draw(self.__screen, 40, 'Play')
            self.__soundBtn.draw(self.__screen, 40, f'Sound {sound_str}')

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self.__exitBtn.is_hovered(m_pos):
                        self.__is__exit = True
                        break
                    elif self.__playBtn.is_hovered(m_pos):
                        is_running = False
                        break

                    elif self.__soundBtn.is_hovered(m_pos):
                        self.__soundMod = not self.__soundMod

                if event.type == pygame.QUIT:
                    self.__is__exit = True
                    is_running = False
                    break

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    self.__btns_hovered(m_pos)

            pygame.display.update()
