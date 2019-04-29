import pygame
from random import randint
from game_board import GameBoard, Castle
from game_dsp import desc
import mob_module

# from pygame.locals import *


class Button:
    def __init__(self, color, width, height, x, y, text=''):
        self.__color = color
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y
        self.__text = text

    def draw(self, screen, font_size, outLine=None):
        pygame.draw.rect(screen, self.__color, (self.__x, self.__y, self.__width, self.__height))
        if self.__text != '':
            font = pygame.font.SysFont('impact', font_size)
            text = font.render(self.__text, 1, (0, 0, 0))
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
        self.__exitBtn = Button((150, 100, 0), 200, 75, 200, 525, 'Exit')

    def __show_text(self):
        header = self.__headerFont.render('Tower Defence!', 1, self.__txtColor)
        self.__screen.blit(header, (self.__screen.get_width() / 4, 75))

        marginTop = 175
        for txt_row in desc:
            dsp = self.__font.render(txt_row, 1, self.__txtColor)
            self.__screen.blit(dsp, (self.__screen.get_width() / 5, marginTop))
            marginTop += 50


    def show_menu(self):
        is_running = True
        while is_running:
            self.__screen.blit(self.__bgImage, (0, 0))
            self.__show_text()
            self.__exitBtn.draw(self.__screen, 40)
            for event in pygame.event.get():
                m_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__exitBtn.is_hovered(m_pos):
                        is_running = False
                        break

                if event.type == pygame.MOUSEMOTION:
                    if self.__exitBtn.is_hovered(m_pos):
                        self.__exitBtn.set_color((255, 0, 0))
                    else:
                        self.__exitBtn.set_color((150, 100, 0))

            pygame.display.update()


class GameObject:
    """
        Docstring
    """
    def __init__(self):
        self.__txtFont = pygame.font.SysFont('impact', 20)
        self.__screen = pygame.display.set_mode((1000, 800))
        self.__bgMusic = pygame.mixer.music.load(r'sound/background_music/main_music.wav')
        self.__GB = GameBoard()
        self.__Castle = self.__GB.get_castle()
        self.__start = self.__GB.get_start()
        self.__path = []
        for st in self.__start:
            self.__path.append(self.__GB.get_path(st))
        self.mobs = []

    @staticmethod
    def set_up_game():
        logo = pygame.image.load(r'images/logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Tower Defence")

    def get_screen(self):
        return self.__screen

    def clean_screen(self):
        self.__screen.fill((0, 0, 0))

    def init_board(self):
        self.__GB.draw_board(self.__screen)

    def draw_mobs(self):
        for mob in self.mobs:
            mob.draw(self.__screen)

    def update_mobs(self):
        i = 0
        for mob in self.mobs:
            if mob.is_end_reached:
                self.mobs.pop(i)
                self.__Castle.take_damage(1)
            else:
                i += 1
                mob.update()

    def spawn_mob(self):
        index = randint(0, len(self.__start) - 1)
        self.mobs.append(mob_module.Spider(self.__start[index], self.__path[index]))

    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)

    def show_cst_hp(self):
        hp = self.__Castle.get_hp()
        hpBtn = Button((0, 150, 0), 125, 50, 865, 10, f'Castle HP: {hp}')
        hpBtn.draw(self.__screen, 20)


def main():
    pygame.init()
    GameObject.set_up_game()
    GmObj = GameObject()
    Menu = MenuObject(GmObj.get_screen())
    Menu.show_menu()

    # all_obj = pygame.sprite.Group()
    clock = pygame.time.Clock()
    is_running = True
    i = 0
    GmObj.play_music()
    GmObj.spawn_mob()
    while is_running:
        clock.tick(5)
        GmObj.init_board()
        GmObj.draw_mobs()
        GmObj.update_mobs()
        GmObj.show_cst_hp()
        if i == 10:
            GmObj.spawn_mob()
            i = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if event.type == pygame.KEYDOWN:
                GmObj.mobs[0].update()

        pygame.display.update()
        i += 1

    pygame.quit()


if __name__ == '__main__':

    main()
