import pygame

pygame.init()


class Sound:
    soundMode = None
    bgMusic1 = pygame.mixer.music.load(r'sound/background_music/main_music.wav')
    spider_death = pygame.mixer.Sound(r'sound/mob_death/SpiderDeath.wav')
    btnClick = pygame.mixer.Sound(r'sound/sound_effects/button_click.wav')







