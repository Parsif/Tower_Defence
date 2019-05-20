from copy import deepcopy
from random import randint

import pygame

from helper_modules.sound import Sound
from src import mobs
from src.cell import tw_lvl1, tw_lvl2, Tower
from src.controllers import Button
from src.controllers import EndGameMenu
from src.controllers import PauseMenu
from src.game_board import GameBoard


class GameObject:
    """
        Docstring
    """

    def __init__(self, screen, Player):
        self.Player = Player
        self.is_exit = None
        self._txtFont = pygame.font.SysFont('impact', 20)
        self._screen = screen
        self._GB = GameBoard()
        self._Castle = self._GB.get_castle
        self._start = self._GB.get_start
        self._path = []
        for st in self._start:
            self._path.append(self._GB.get_path(st))
        if self._GB.BM.is_generated:
            self._GB.clean_board()
            self._GB.set_towers()
        self.__towers = deepcopy(self._GB.get_towers)  # just placeholders for tower
        self.mobs = []

        self._hpBtn = Button(125, 50, 865, 10)
        self._pauseBtn = Button(60, 60, 0, 0)
        self._coinsBtn = Button(125, 50, 865, 65)

        self._fire_towers = []  # tower which can fire
        self._dead_mobs = []
        self.is_music_played = False
        self.waveCnt = 0

    @staticmethod
    def set_up_game():
        logo = pygame.image.load(r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Tower Defence")

    @property
    def get_screen(self):
        return self._screen

    def clean_screen(self):
        self._screen.fill((0, 0, 0))

    def draw_board(self):
        self._GB.draw(self._screen, self.__towers)

    def draw_mobs(self):
        for mob in self.mobs:
            mob.draw(self._screen)

    def update_mobs(self):
        i = 0
        for mob in self.mobs:
            if mob.get_hp < 0:
                self.mobs.pop(i)
                self.Player.increase_coins(mob.get_cost)
                self._dead_mobs.append(mob)

            if mob.is_end_reached:
                self.mobs.pop(i)
                self._Castle.take_damage(1)
            else:
                i += 1
                mob.update()

    def spawn_mob(self):
        index = randint(0, len(self._start) - 1)  # portal number
        if self.waveCnt < 30:
            self.mobs.append(mobs.Spider(self._start[index], self._path[index]))
        elif 30 <= self.waveCnt < 50:
            pass
        elif 50 <= self.waveCnt < 70:
            self.mobs.append(mobs.Turtle(self._start[index], self._path[index]))
        elif 70 <= self.waveCnt < 90:
            pass
        elif 90 <= self.waveCnt < 95:
            self.mobs.append(mobs.Dragon(self._start[index], self._path[index]))
        elif self.waveCnt > 95 and len(self.mobs) == 0:
            gmPlayed = self.Player.userDoc['gmPlayed'] + 1
            self.Player.db_collection.update_one({'email': self.Player.email}, {'$set': {'gmPlayed': gmPlayed}})
            gmWon = self.Player.userDoc['gmWon'] + 1
            self.Player.db_collection.update_one({'email': self.Player.email}, {'$set': {'gmWon': gmWon}})
            pygame.mixer.music.pause()
            DF = EndGameMenu(self._screen, self.Player, pygame.image.load(
                r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/menu/main_menu_background.png'), 'Victory')
            return DF.show_menu()

        self.waveCnt += 1

    def play_music(self):
        pygame.mixer.music.play(-1)
        self.is_music_played = True

    def restart(self):
        self.mobs.clear()
        self.__towers = deepcopy(self._GB.get_towers)
        self._fire_towers.clear()
        self._dead_mobs.clear()
        self._Castle.set_hp(20)
        self.Player.set_coins_default()

    def show_cst_hp(self):
        hp = self._Castle.get_hp
        if hp <= 0:
            gmPlayed = self.Player.userDoc['gmPlayed'] + 1
            self.Player.db_collection.update_one({'email': self.Player.email}, {'$set': {'gmPlayed': gmPlayed}})

            gmLoose = self.Player.userDoc['gmLoose'] + 1
            self.Player.db_collection.update_one({'email': self.Player.email}, {'$set': {'gmLoose': gmLoose}})

            pygame.mixer.music.pause()
            DF = EndGameMenu(self._screen, self.Player, pygame.image.load(
                r'C:/Users/Влад/PycharmProjects/Tower_Defence/images/menu/defeat_menu_background.jpg'), 'Defeat')
            return DF.show_menu()

        self._hpBtn.draw(self._screen, 20, f'Castle HP: {hp}')

    def show_player_coins(self):
        self._coinsBtn.draw(self._screen, 20, f'Coins: {self.Player.get_coins}')

    def draw_pause_btn(self):
        self._pauseBtn.draw(self._screen, 16, 'Pause')

    def __change_tw_state(self, tower, upgrade=None):
        coord = tower.get_coord
        upgradeBtn = None
        if upgrade is not None:
            upgradeBtn = Button(75, 25, coord['x'] * tower.SIZE + 23, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        sellBtn = Button(75, 25, coord['x'] * tower.SIZE - 55, coord['y'] * tower.SIZE - 30, (255, 255, 0))

        while True:
            if upgradeBtn is not None:
                upgradeBtn.draw(self._screen, 13, f'Upgrade: {upgrade.COST}')

            sellBtn.draw(self._screen, 13, f'Sell: {tower.COST // 2}')
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

                        tmp_index = self._fire_towers.index(tower)
                        del self._fire_towers[tmp_index]

                        self.__towers.append(Tower(2, {'x': coord['x'], 'y': coord['y']}))
                        self.Player.increase_coins(tower.COST // 2)
                        if Sound.soundMode:
                            Sound.towerSell.play()

                    if upgrade is not None:
                        if upgradeBtn.is_hovered(m_pos):
                            if self.Player.get_coins - upgrade.COST >= 0:
                                self.Player.decrease_coins(upgrade.COST)
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
            basicBtn.draw(self._screen, 11, f'Basic: {tw_lvl1[0].COST}')
            fireBtn.draw(self._screen, 11, f'Fire: {tw_lvl1[1].COST}')
            iceBtn.draw(self._screen, 11, f'Ice: {tw_lvl1[2].COST}')
            darkBtn.draw(self._screen, 11, f'Dark: {tw_lvl1[3].COST}')
            poisonBtn.draw(self._screen, 11, f'Poison: {tw_lvl1[4].COST}')

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
                            if self.Player.get_coins - tw_lvl1[i].COST >= 0:
                                self.Player.decrease_coins(tw_lvl1[i].COST)
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
                pygame.draw.rect(self._screen, (255, 0, 0), (coord['x'] * tower.SIZE - tower.SIZE * 2,
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
                        index_f_tw = self._fire_towers.index(tmp)
                        self.__towers[i] = new_tower
                        self._fire_towers[index_f_tw] = new_tower
                        return None

                new_tower = self.__choose_tower(tmp)
                if new_tower is None:
                    return None

                new_tower.set_build_cnt()
                if new_tower not in self._fire_towers:
                    self.__towers[i] = new_tower
                    self._fire_towers.append(new_tower)

            i += 1

    def tw_fire(self):
        for tower in self._fire_towers:
            if tower.get_build_cnt == 0:
                tower.fire(self._screen, self.mobs)

    def draw_dead_mb(self):
        i = 0
        for mob in self._dead_mobs:
            if mob.get_turns_dead < 3:
                mob.draw_dead(self._screen)
            else:
                self._dead_mobs.pop(i)
            i += 1

    def build_towers(self):
        for tower in self._fire_towers:
            tower.build(self._screen)

    def show_shot(self):
        for tower in self._fire_towers:
            if tower.get_shot_cnt != 0:
                tower.show_shot(self._screen)

    def pause_btn_hovered(self, m_pos):
        if self._pauseBtn.is_hovered(m_pos):
            self._pauseBtn.set_color((255, 0, 0))
        else:
            self._pauseBtn.set_color()

    def pause_btn_click(self, m_pos):
        if self._pauseBtn.is_hovered(m_pos):
            pygame.mixer.music.pause()
            pm = PauseMenu(self._screen, self.Player)
            pm.show_menu()
            if Sound.soundMode:
                pygame.mixer.music.unpause()
            return pm.get_is_exit

        return False
