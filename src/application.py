import pygame
from pygame.locals import *
from game_board import GameBoard
import mob_module


class GameObject:
    """
        Docstring
    """
    def __init__(self):
        self.__screen = pygame.display.set_mode((1000, 800))
        self.__bgMusic = pygame.mixer.music.load(r'sound/background_music/main_music.wav')
        self.__GB = GameBoard()
        print(self.__GB.get_start()['x'])
        self.__path = self.__GB.get_path()
        self.__start = self.__GB.get_start()
        self.mobs = []

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
            mob.draw(self.__screen)

    def update_mobs(self):
        for mob in self.mobs:
            mob.update()

    def spawn_mob(self):
        self.mobs.append(mob_module.Spider(self.__start, self.__path))

    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)

# def show_menu():



def main():
    pygame.init()
    GameObject.set_up_game()
    gm_obj = GameObject()
    all_obj = pygame.sprite.Group()
    clock = pygame.time.Clock()
    is_running = True
    i = 0
    gm_obj.play_music()
    gm_obj.spawn_mob()
    while is_running:
        clock.tick(10)
        gm_obj.init_board()
        gm_obj.draw_mobs()
        gm_obj.update_mobs()
        if i == 10:
            gm_obj.spawn_mob()
            i = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if event.type == pygame.KEYDOWN:
                gm_obj.mobs[0].update()

        pygame.display.update()
        i += 1

    pygame.quit()


if __name__ == '__main__':

    main()
