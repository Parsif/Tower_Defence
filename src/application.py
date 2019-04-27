import pygame
from pygame.locals import *
from game_board import GameBoard


class GameObject:
    """
        Docstring
    """
    def __init__(self):
        self.__screen = pygame.display.set_mode((800, 800))
        self.__GB = GameBoard()

    @staticmethod
    def set_up_game():
        logo = pygame.image.load(r'images/logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Tower Defence")

    def clean_screen(self):
        self.__screen.fill((0, 0, 0))

    def init_board(self):
        self.__GB.draw_board(self.__screen)


def main():
    pygame.init()
    GameObject.set_up_game()
    GmObj = GameObject()

    isRunning = True
    while isRunning:
        GmObj.init_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break

            pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
