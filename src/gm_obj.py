import pygame
from random import randint
from src.game_board import GameBoard
from src.cell import BasicTower, FireTower, IceTower, DarkTower, PoisonTower
from src import mob_module
from src.controllers import Button
from helper_modules.sound import Sound



class GameObject:
    """
        Docstring
    """
    def __init__(self):
        self.is_exit = None
        self.__txtFont = pygame.font.SysFont('impact', 20)
        self.__screen = pygame.display.set_mode((1000, 800))
        self.__bgMusic = Sound.bgMusic2
        self.__GB = GameBoard()
        self.__Castle = self.__GB.get_castle
        self.__towers = self.__GB.get_towers  # just placeholders for tower
        self.__start = self.__GB.get_start
        self.__path = []
        for st in self.__start:
            self.__path.append(self.__GB.get_path(st))
        self.mobs = []

        self.__hpBtn = Button(125, 50, 865, 10)
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
                self.__dead_mobs.append(mob)

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
        hp = self.__Castle.get_hp
        self.__hpBtn.draw(self.__screen, 20, f'Castle HP: {hp}')

    def __choose_tower(self, tower):
        coord = tower.get_coord
        is_running = True
        basicBtn = Button(60, 25, coord['x'] * tower.SIZE - 72, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        fireBtn = Button(60, 25, coord['x'] * tower.SIZE - 11, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        iceBtn = Button(60, 25, coord['x'] * tower.SIZE + 50, coord['y'] * tower.SIZE - 30, (255, 255, 0))
        darkBtn = Button(60, 25, coord['x'] * tower.SIZE - 72, coord['y'] * tower.SIZE + 40, (255, 255, 0))
        poisonBtn = Button(60, 25, coord['x'] * tower.SIZE - 11, coord['y'] * tower.SIZE + 40, (255, 255, 0))


        while is_running:
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
                    if basicBtn.is_hovered(m_pos):
                        basicBtn.set_color((0, 0, 200))
                    else:
                        basicBtn.set_color()

                    if fireBtn.is_hovered(m_pos):
                        fireBtn.set_color((0, 0, 200))
                    else:
                        fireBtn.set_color()

                    if iceBtn.is_hovered(m_pos):
                        iceBtn.set_color((0, 0, 200))
                    else:
                        iceBtn.set_color()

                    if darkBtn.is_hovered(m_pos):
                        darkBtn.set_color((0, 0, 200))
                    else:
                        darkBtn.set_color()

                    if poisonBtn.is_hovered(m_pos):
                        poisonBtn.set_color((0, 0, 200))
                    else:
                        poisonBtn.set_color()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if basicBtn.is_hovered(m_pos):
                        if Sound.soundMode:
                            Sound.btnClick.play()
                        return BasicTower(tower)

                    elif fireBtn.is_hovered(m_pos):
                        if Sound.soundMode:
                            Sound.btnClick.play()

                        return FireTower(tower)

                    elif iceBtn.is_hovered(m_pos):
                        if Sound.soundMode:
                            Sound.btnClick.play()
                        return IceTower(tower)

                    elif darkBtn.is_hovered(m_pos):
                        if Sound.soundMode:
                            Sound.btnClick.play()

                        return DarkTower(tower)

                    elif poisonBtn.is_hovered(m_pos):
                        if Sound.soundMode:
                            Sound.btnClick.play()

                        return PoisonTower(tower)

                    else:
                        return None

            pygame.display.update()


    def towers_hover(self, m_pos):
        for tower in self.__towers:
            if tower.is_hovered(m_pos):
                tower.set_color((255, 0, 0))
            else:
                tower.set_color()

    def tower_click(self, m_pos):
        for tower in self.__towers:
            if tower.is_hovered(m_pos):
                # draw radius square
                coord = tower.get_coord
                pygame.draw.rect(self.__screen, (255, 0, 0), (coord['x'] * tower.SIZE - tower.SIZE * 2,
                                                              coord['y'] * tower.SIZE - tower.SIZE * 2,
                                                              tower.SIZE * 5, tower.SIZE * 5), 2)
                tmp = tower
                del tower
                newTower = self.__choose_tower(tmp)
                if newTower is None:
                    return None
                newTower.set_build_cnt()
                self.__fire_towers.append(newTower)

        for tower in self.__fire_towers:
            self.__towers.append(tower)

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





GmObj = GameObject()
