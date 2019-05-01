from random import randint

import pygame

from helper_modules.sound import Sound
from src import mobs
from src.cell import tw_lvl1, tw_lvl2, Tower
from src.controllers import Button
from src.controllers import PauseMenu
from src.game_board import GameBoard
from src.player import Player


class GameObject:
    """
        Docstring
    """
    def __init__(self):
        self.__Player = Player()
        self.is_exit = None
        self.__txtFont = pygame.font.SysFont('impact', 20)
        self.__screen = pygame.display.set_mode((1000, 800))
        self.__GB = GameBoard()
        self.__Castle = self.__GB.get_castle
        self.__towers = self.__GB.get_towers  # just placeholders for tower
        self.__start = self.__GB.get_start
        self.__path = []
        for st in self.__start:
            self.__path.append(self.__GB.get_path(st))
        self.mobs = []

        self.__hpBtn = Button(125, 50, 865, 10)
        self.__pauseBtn = Button(60, 60, 0, 0)
        self.__coinsBtn = Button(125, 50, 865, 65)

        self.__fire_towers = []  # tower which can fire
        self.__dead_mobs = []

    @staticmethod
    def set_up_game():
        logo = pygame.image.load(r'images/logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Tower Defence")

    @property
    def get_screen(self):
        return self.__screen

    def clean_screen(self):
        self.__screen.fill((0, 0, 0))

    def draw_board(self):
        self.__GB.draw(self.__screen, self.__towers)

    def draw_mobs(self):
        for mob in self.mobs:
            mob.draw(self.__screen)

    def update_mobs(self):
        i = 0
        for mob in self.mobs:
            if mob.get_hp < 0:
                self.mobs.pop(i)
                self.__Player.increase_coins(mob.get_cost)
                self.__dead_mobs.append(mob)

            if mob.is_end_reached:
                self.mobs.pop(i)
                self.__Castle.take_damage(1)
            else:
                i += 1
                mob.update()

    def spawn_mob(self):
        index = randint(0, len(self.__start) - 1)  # portal number
        self.mobs.append(mobs.Spider(self.__start[index], self.__path[index]))

    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)

    def show_cst_hp(self):
        hp = self.__Castle.get_hp
        self.__hpBtn.draw(self.__screen, 20, f'Castle HP: {hp}')

    def show_player_coins(self):
        self.__coinsBtn.draw(self.__screen, 20, f'Coins: {self.__Player.get_coins}')

    def draw_pause_btn(self):
        self.__pauseBtn.draw(self.__screen, 16, 'Pause')

    def __change_tw_state(self, tower, upgrade=None):
        coord = tower.get_coord
        upgradeBtn = None
        if upgrade is not None:
            upgradeBtn = Button(75, 25, coord['x'] * tower.SIZE + 23, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        sellBtn = Button(75, 25, coord['x'] * tower.SIZE - 55, coord['y'] * tower.SIZE - 30, (255, 255, 0))

        while True:
            if upgradeBtn is not None:
                upgradeBtn.draw(self.__screen, 13, f'Upgrade: {upgrade.COST}')

            sellBtn.draw(self.__screen, 13, f'Sell: {tower.COST // 2}')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_exit = True
                    return None

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    if sellBtn.is_hovered(m_pos):
                        sellBtn.set_color((0, 0, 200))
                    else:
                        sellBtn.set_color()

                    if upgrade is not None:
                        if upgradeBtn.is_hovered(m_pos):
                            upgradeBtn.set_color((0, 0, 200))
                        else:
                            upgradeBtn.set_color()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if sellBtn.is_hovered(m_pos):
                        tmp_index = self.__towers.index(tower)
                        del self.__towers[tmp_index]

                        tmp_index = self.__fire_towers.index(tower)
                        del self.__fire_towers[tmp_index]

                        self.__towers.append(Tower(2, {'x': coord['x'], 'y': coord['y']}))
                        self.__Player.increase_coins(tower.COST // 2)
                        if Sound.soundMode:
                            Sound.towerSell.play()

                    if upgrade is not None:
                        if upgradeBtn.is_hovered(m_pos):
                            if self.__Player.get_coins - upgrade.COST >= 0:
                                self.__Player.decrease_coins(upgrade.COST)
                                return upgrade(tower)

                    return None

            pygame.display.update()

    def __choose_tower(self, tower):
        coord = tower.get_coord
        basicBtn = Button(60, 25, coord['x'] * tower.SIZE - 72, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        fireBtn = Button(60, 25, coord['x'] * tower.SIZE - 11, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        iceBtn = Button(60, 25, coord['x'] * tower.SIZE + 50, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        darkBtn = Button(60, 25, coord['x'] * tower.SIZE - 72, coord['y'] * tower.SIZE + 40, (255, 255, 0))
        poisonBtn = Button(60, 25, coord['x'] * tower.SIZE - 11, coord['y'] * tower.SIZE + 40, (255, 255, 0))
        btns = [basicBtn, fireBtn, iceBtn, darkBtn, poisonBtn]

        while True:
            basicBtn.draw(self.__screen, 13, 'Basic')
            fireBtn.draw(self.__screen, 13, 'Fire')
            iceBtn.draw(self.__screen, 13, 'Ice')
            darkBtn.draw(self.__screen, 13, 'Dark')
            poisonBtn.draw(self.__screen, 13, 'Poison')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_exit = True
                    return None

                if event.type == pygame.MOUSEMOTION:
                    m_pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if btn.is_hovered(m_pos):
                            btn.set_color((0, 0, 200))
                        else:
                            btn.set_color()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    for i in range(len(btns)):
                        if btns[i].is_hovered(m_pos):
                            if self.__Player.get_coins - tw_lvl1[i].COST >= 0:
                                self.__Player.decrease_coins(tw_lvl1[i].COST)
                                if Sound.soundMode:
                                    Sound.btnClick.play()
                                return tw_lvl1[i](tower)

                    tower.set_color()
                    return None

            pygame.display.update()

    def towers_hover(self, m_pos):
        for tower in self.__towers:
            if tower.is_hovered(m_pos):
                tower.set_color((255, 0, 0))
            else:
                tower.set_color()

    def tower_click(self, m_pos):
        i = 0
        for tower in self.__towers:
            if tower.is_hovered(m_pos):
                # draw radius square
                coord = tower.get_coord
                pygame.draw.rect(self.__screen, (255, 0, 0), (coord['x'] * tower.SIZE - tower.SIZE * 2,
                                                              coord['y'] * tower.SIZE - tower.SIZE * 2,
                                                              tower.SIZE * 5, tower.SIZE * 5), 2)

                tmp = self.__towers[i]
                for j in range(len(tw_lvl2)):
                    if type(tmp) is tw_lvl2[j]:
                        self.__change_tw_state(tmp)
                        return None

                for j in range(len(tw_lvl1)):
                    if type(tmp) is tw_lvl1[j]:
                        new_tower = self.__change_tw_state(tmp, tw_lvl2[j])
                        if new_tower is None:
                            return None
                        new_tower.set_build_cnt()
                        index_f_tw = self.__fire_towers.index(tmp)
                        self.__towers[i] = new_tower
                        self.__fire_towers[index_f_tw] = new_tower
                        return None

                new_tower = self.__choose_tower(tmp)
                if new_tower is None:
                    return None

                new_tower.set_build_cnt()
                if new_tower not in self.__fire_towers:
                    self.__towers[i] = new_tower
                    self.__fire_towers.append(new_tower)

            i += 1

    def tw_fire(self):
        for tower in self.__fire_towers:
            if tower.get_build_cnt == 0:
                tower.fire(self.__screen, self.mobs)

    def draw_dead_mb(self):
        i = 0
        for mob in self.__dead_mobs:
            if mob.get_turns_dead < 3:
                mob.draw_dead(self.__screen)
            else:
                self.__dead_mobs.pop(i)
            i += 1

    def build_towers(self):
        for tower in self.__fire_towers:
            tower.build(self.__screen)

    def show_shot(self):
        for tower in self.__fire_towers:
            if tower.get_shot_cnt != 0:
                tower.show_shot(self.__screen)

    def pause_btn_hovered(self, m_pos):
        if self.__pauseBtn.is_hovered(m_pos):
            self.__pauseBtn.set_color((255, 0, 0))
        else:
            self.__pauseBtn.set_color()

    def pause_btn_click(self, m_pos):
        if self.__pauseBtn.is_hovered(m_pos):
            pygame.mixer.music.pause()
            pm = PauseMenu(self.__screen)
            pm.show_menu()
            if Sound.soundMode:
                pygame.mixer.music.unpause()
            return pm.get_is_exit

        return False
