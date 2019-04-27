import pygame
from pygame.locals import *
from game_board import GameBoard
import mob_module


class GameObject:
    """
        Docstring
    """
    def __init__(self):
        self.__screen = pygame.display.set_mode((800, 800))
        self.__GB = GameBoard()
        print(self.__GB.get_start()['x'])
        self.mobs = [mob_module.Skeleton(self.__GB.get_start())]

    @staticmethod
    def set_up_game():
        logo = pygame.image.load(r'images/logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Tower Defence")

    def clean_screen(self):
        self.__screen.fill((0, 0, 0))

    def init_board(self):
        self.__GB.draw_board(self.__screen)

    def draw_mobs(self):
        for mob in self.mobs:
            mob.draw_mob(self.__screen)


def main():
    pygame.init()
    GameObject.set_up_game()
    gm_obj = GameObject()

    start_ticks = pygame.time.get_ticks()  # starter tick
    is_running = True
    while is_running:
        gm_obj.init_board()
        gm_obj.draw_mobs()

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
        if seconds > 2:  # if more than 10 seconds close the game
            gm_obj.mobs[0].move()
            start_ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if event.type == pygame.KEYDOWN:
                gm_obj.mobs[0].move()

            pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
