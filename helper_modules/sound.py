import pygame

pygame.init()


class Sound:
    soundMode = None
    bgMusic1 = pygame.mixer.music.load(r'sound/background_music/main_music.wav')
    bgMusic2 = pygame.mixer.music.load(r'sound/background_music/Hero_Down.mp3')
    spider_death = pygame.mixer.Sound(r'sound/mob_death/SpiderDeath.wav')
    btnClick = pygame.mixer.Sound(r'sound/sound_effects/button_click.wav')
    towerConstruct = pygame.mixer.Sound(r'sound/sound_effects/TowerConstruct.wav')

    basicTwShot = pygame.mixer.Sound(r'sound/tower_shots/Basic.wav')
    darkTwShot = pygame.mixer.Sound(r'sound/tower_shots/Dark.wav')
    fireTwShot = pygame.mixer.Sound(r'sound/tower_shots/Fire.wav')
    iceTwShot = pygame.mixer.Sound(r'sound/tower_shots/Ice.wav')
    poisonTwShot = pygame.mixer.Sound(r'sound/tower_shots/Poison.wav')








