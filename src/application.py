from tkinter import *

import pygame
import pymongo

from helper_modules.sound import Sound
from src.controllers import MenuObject
from src.game_object import GameObject
from src.player import Player


def valid_info(email, password, root, player):
    client = pymongo.MongoClient(
        "mongodb+srv://Vlad:mandarin2001@cluster0-4fh12.mongodb.net/TD?retryWrites=true")
    db = client['TD']
    users = db['users']
    user = users.find_one({'email': email.get()})
    if user is None:
        return None
    if user['email'] == email.get() and user['password'] == password.get():
        player.isLoggedIn = True
        player.db_collection = users
        player.email = user['email']
        player.userDoc = user
        root.destroy()


def login(player):
    root = Tk()
    root.title(u'Login')
    root.geometry('400x200')
    root.resizable(False, False)
    lbl1 = Label(root, text='Email', font='arial 18')
    email = StringVar()
    email_field = Entry(textvariable=email, width=47)

    lbl2 = Label(root, text='Password', font='arial 18')
    password = StringVar()
    password_field = Entry(show='*', textvariable=password, width=40)
    submit = Button(root, bg="blue", text=u"Login", command=lambda: valid_info(email, password, root, player),
                    font='arial 17')

    lbl1.place(x=0, y=30)
    email_field.place(x=100, y=40)
    lbl2.place(x=0, y=110)
    password_field.place(x=140, y=120)
    submit.place(x=160, y=160)

    root.mainloop()


def main():
    pl = Player()
    login(pl)
    if not pl.isLoggedIn:
        return None

    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    GameObject.set_up_game()
    Menu = MenuObject(screen, pl)
    Menu.show_menu()
    if Menu.get_is_exit:
        return None
    GmObj = GameObject(screen, pl)

    GmObj.is_exit = Menu.get_is_exit
    if GmObj.is_exit:
        return None

    clock = pygame.time.Clock()
    is_running = True
    spawnCnt = 0
    SPAWN_RATE = 30
    if Sound.soundMode:
        GmObj.play_music()

    GmObj.spawn_mob()
    FPS = 80
    while is_running:
        clock.tick(FPS)
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
            GmObj = GameObject(screen, pl)
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

                Menu = MenuObject(screen, pl)
                Menu.show_menu()
                GmObj = GameObject(screen, pl)
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
