import pygame

from helper_modules.sound import Sound
from src.controllers import MenuObject
from src.game_object import GameObject


# from pygame.locals import *


def main():
    pygame.init()
    GmObj = GameObject()
    GmObj.set_up_game()
    Menu = MenuObject(GmObj.get_screen)
    Menu.show_menu()
    GmObj.is_exit = Menu.get_is_exit
    if GmObj.is_exit:
        return None

    # all_obj = pygame.sprite.Group()
    clock = pygame.time.Clock()
    is_running = True
    i = 0
    if Sound.soundMode:
        GmObj.play_music()

    GmObj.spawn_mob()
    while is_running:
        clock.tick(25)
        GmObj.draw_board()
        GmObj.draw_pause_btn()
        GmObj.show_cst_hp()
        GmObj.show_player_coins()
        GmObj.draw_mobs()
        GmObj.draw_dead_mb()
        GmObj.tw_fire()
        GmObj.show_shot()

        if i == 15:
            GmObj.spawn_mob()
            i = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                GmObj.tower_click(m_pos)
                GmObj.is_exit = GmObj.pause_btn_click(m_pos)

            if event.type == pygame.MOUSEMOTION:
                m_pos = pygame.mouse.get_pos()
                GmObj.towers_hover(m_pos)
                GmObj.pause_btn_hovered(m_pos)

        if GmObj.is_exit:
            break
        GmObj.build_towers()
        pygame.display.update()
        GmObj.update_mobs()
        i += 1

    pygame.quit()


if __name__ == '__main__':
    main()
