import pygame

from helper_modules.sound import Sound
from src.controllers import MenuObject
from src.game_object import GameObject


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    GameObject.set_up_game()
    Menu = MenuObject(screen)
    Menu.show_menu()
    if Menu.get_is_exit:
        return None
    GmObj = GameObject(screen)

    GmObj.is_exit = Menu.get_is_exit
    if GmObj.is_exit:
        return None

    clock = pygame.time.Clock()
    is_running = True
    spawnCnt = 0
    SPAWN_RATE = 20
    if Sound.soundMode:
        GmObj.play_music()

    GmObj.spawn_mob()
    while is_running:
        clock.tick(25)
        GmObj.draw_board()
        GmObj.draw_pause_btn()
        tmp = GmObj.show_cst_hp()
        if tmp is None:
            if Sound.soundMode and GmObj.is_music_played:
                pygame.mixer.music.unpause()
            elif Sound.soundMode:
                GmObj.play_music()

        elif tmp:
            GmObj.restart()
            Menu.show_menu()
            GmObj = GameObject(screen)
            if Menu.get_is_exit:
                break
            if Sound.soundMode:
                GmObj.play_music()
            continue
        else:
            break

        GmObj.show_player_coins()
        GmObj.draw_mobs()
        GmObj.draw_dead_mb()
        GmObj.tw_fire()
        GmObj.show_shot()

        if spawnCnt == SPAWN_RATE:
            tmp = GmObj.spawn_mob()
            if tmp is None:
                if Sound.soundMode and GmObj.is_music_played:
                    pygame.mixer.music.unpause()
                elif Sound.soundMode:
                    GmObj.play_music()

            elif tmp:
                GmObj.restart()
                Menu.show_menu()
                GmObj = GameObject(screen)
                if Menu.get_is_exit:
                    break
                if Sound.soundMode:
                    GmObj.play_music()
                continue
            else:
                break
            spawnCnt = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                GmObj.is_exit = GmObj.pause_btn_click(m_pos)
                GmObj.tower_click(m_pos)

            if event.type == pygame.MOUSEMOTION:
                m_pos = pygame.mouse.get_pos()
                GmObj.towers_hover(m_pos)
                GmObj.pause_btn_hovered(m_pos)


        if GmObj.is_exit:
            break
        GmObj.build_towers()
        pygame.display.update()
        GmObj.update_mobs()
        spawnCnt += 1

    pygame.quit()


if __name__ == '__main__':
    main()
