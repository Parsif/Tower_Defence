from random import randint

import pygame

pygame.init()


class Sound:
    soundMode = True
    num = randint(1, 5)
    if num == 1:
        bgMusic1 = pygame.mixer.music.load(
            r'C:/Users\Влад/PycharmProjects/Tower_Defence/sound/background_music/main_music.wav')
    elif num == 2:
        bgMusic2 = pygame.mixer.music.load(
            r'C:/Users\Влад/PycharmProjects/Tower_Defence/sound/background_music/Hero_Down.mp3')
    elif num == 3:
        bgMusic3 = pygame.mixer.music.load(
            r'C:/Users\Влад/PycharmProjects/Tower_Defence/sound/background_music/Anamalie.mp3')

    elif num == 4:
        bgMusic4 = pygame.mixer.music.load(
            r'C:/Users\Влад/PycharmProjects/Tower_Defence/sound/background_music/Fall_of_the_Solar_King2.wav')
    else:
        bgMusic5 = pygame.mixer.music.load(
            r'C:/Users\Влад/PycharmProjects/Tower_Defence/sound/background_music/Amazing_Plan_Silent_Film_Dark.mp3')

    spider_death = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/mob_death/SpiderDeath.wav')
    orc_death = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/mob_death/OrcDeath.wav')
    lizard_death = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/mob_death/LizardDeath.wav')
    dragon_death = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/mob_death/DragonDeath.wav')
    turtle_death = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/mob_death/TurtleDeath.wav')
    wolf_death = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/mob_death/WolfDeath.wav')

    btnClick = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/sound_effects/button_click.wav')
    towerConstruct = pygame.mixer.Sound(
        r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/sound_effects/TowerConstruct.wav')
    towerSell = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/sound_effects/TowerSell.wav')

    basicTwShot = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/tower_shots/Basic.wav')
    darkTwShot = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/tower_shots/Dark.wav')
    fireTwShot = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/tower_shots/Fire.wav')
    iceTwShot = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/tower_shots/Ice.wav')
    poisonTwShot = pygame.mixer.Sound(r'C:/Users/Влад/PycharmProjects/Tower_Defence/sound/tower_shots/Poison.wav')
