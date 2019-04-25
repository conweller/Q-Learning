import pygame
from pygame.locals import *

background_colour = (255, 255, 255)
pygame.init()
InfoObject = pygame.display.Info()
display_width = InfoObject.current_w
display_height = InfoObject.current_h
gameDisplay = pygame.display.set_mode(
    (display_width, display_height), pygame.RESIZABLE)
gameDisplay.fill(background_colour)

running = True
while running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
