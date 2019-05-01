import pygame

pygame.init()
dragon_down = []

dragon_down.append(pygame.image.load(r'images/dragon/dragon_down1.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down2.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down3.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down4.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down5.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down6.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down7.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down8.png'))

dragon_down.append(pygame.image.load(r'images/dragon/dragon_down9.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down10.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down11.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down12.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down13.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down14.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down15.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down16.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down17.png'))

dragon_down.append(pygame.image.load(r'images/dragon/dragon_down18.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down19.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down20.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down21.png'))
dragon_down.append(pygame.image.load(r'images/dragon/dragon_down22.png'))

dragon_right = []

dragon_right.append(pygame.image.load(r'images/dragon/dragon_right1.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right2.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right3.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right4.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right5.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right6.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right7.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right8.png'))

dragon_right.append(pygame.image.load(r'images/dragon/dragon_right9.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right10.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right11.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right12.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right13.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right14.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right15.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right16.png'))

dragon_right.append(pygame.image.load(r'images/dragon/dragon_right17.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right18.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right19.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right20.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right21.png'))
dragon_right.append(pygame.image.load(r'images/dragon/dragon_right22.png'))

dragon_up = []

dragon_up.append(pygame.image.load(r'images/dragon/dragon_up1.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up2.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up3.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up4.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up5.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up6.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up7.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up8.png'))

dragon_up.append(pygame.image.load(r'images/dragon/dragon_up9.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up10.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up11.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up12.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up13.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up14.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up15.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up16.png'))

dragon_up.append(pygame.image.load(r'images/dragon/dragon_up17.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up18.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up19.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up20.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up21.png'))
dragon_up.append(pygame.image.load(r'images/dragon/dragon_up22.png'))

dragon_left = []

dragon_left.append(pygame.image.load(r'images/dragon/dragon_left1.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left2.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left3.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left4.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left5.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left6.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left7.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left8.png'))

dragon_left.append(pygame.image.load(r'images/dragon/dragon_left9.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left10.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left11.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left12.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left13.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left14.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left15.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left16.png'))

dragon_left.append(pygame.image.load(r'images/dragon/dragon_left17.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left18.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left19.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left20.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left21.png'))
dragon_left.append(pygame.image.load(r'images/dragon/dragon_left22.png'))

dragon_dead = [pygame.image.load(r'images/dragon/dragon_dead.png')]
