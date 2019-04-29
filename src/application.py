import pygame
from src.gm_obj import GameObject
from src.contorllers import MenuObject

# from pygame.locals import *




def main():
    pygame.init()
    GameObject.set_up_game()
    GmObj = GameObject()
    Menu = MenuObject(GmObj.get_screen)
    Menu.show_menu()

    if Menu.get_is_exit:
        return None
    # all_obj = pygame.sprite.Group()
    clock = pygame.time.Clock()
    is_running = True
    i = 0
    if Menu.get_sound_mod:
        GmObj.play_music()
    GmObj.spawn_mob()
    while is_running:
        clock.tick(10)
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                GmObj.tower_click(m_pos)

            if event.type == pygame.MOUSEMOTION:
                m_pos = pygame.mouse.get_pos()
                GmObj.towers_hover(m_pos)

        pygame.display.update()
        i += 1

    pygame.quit()


if __name__ == '__main__':

    main()
