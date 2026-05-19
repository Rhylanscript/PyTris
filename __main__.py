'''
PyTris - A Tetris clone made in Python using Pygame

Made by Rhylan M
Version 2.3

'''

# imports
import pygame
import sys

# import local modules
from src.core.game import Game
from src.core.backend import Backend
from src.config.settings import *

# colour consts
DARK_BLUE = (45, 45, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (60, 85, 160)

# initialise pygame
pygame.init()
title_font = pygame.font.Font(None, 40)
sub_font = pygame.font.Font(None, 30)

# create pygame surfaces
score_surface = title_font.render("Score", True, WHITE)
highscore_surface = title_font.render("Highscore", True, WHITE)
next_surface = title_font.render("Next", True, WHITE)
game_over_surface = title_font.render("Game Over", True, WHITE)
game_over_surface_2 = sub_font.render("Press Space", True, WHITE)
paused_surface = title_font.render("Paused", True, WHITE)

# create pygame rects
score_rect = pygame.Rect(320, 55, 170, 60)
highscore_rect = pygame.Rect(320, 210, 170, 60)
next_rect = pygame.Rect(320, 350, 170, 180)

# setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyTris")
clock = pygame.time.Clock()

# setup icon
icon = pygame.image.load("PyTris.png")
pygame.display.set_icon(icon)

# create objects
backend = Backend()
game = Game(backend)

# other setup for mainloop
highscore = backend.get_highscore()
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 500)

# paused variables
paused = False
flicker = False

# mainloop
while True:

    # check pygame events
    for event in pygame.event.get():

        # check for window close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # handle keypresses
        if event.type == pygame.KEYDOWN:

            # game controls
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game.game_over == False:
                game.move_left()
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game.game_over == False:
                game.move_right()
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and game.game_over == False:
                game.rotate()

            # if game over and space pressed, reset game
            if event.key == pygame.K_SPACE:
                if game.game_over:
                    game.game_over = False
                    game.reset()
                else:
                    game.drop_block()

            # swap blocks if c pressed
            if event.key == pygame.K_c:
                game.swap_blocks()
                pygame.time.delay(50)

            if event.key == pygame.K_r:
                game.game_over = True
                game.reset()
                game.game_over = False

            # check for pause / unpause
            if event.key == pygame.K_p:
                paused = not paused

            # if escape pressed, close window
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit() 

        # custom event update to base when to move tetronimo is moved down
        if event.type == GAME_UPDATE:
            if not paused and not game.game_over:
                game.move_down()
            flicker = not flicker

    # clear screen
    screen.fill(DARK_BLUE)

    # score surfaces
    score_value_surface = title_font.render(str(round(game.score)), True, WHITE)
    highscore_value_surface = title_font.render(str(round(highscore)), True, WHITE)

    # blit text on screen
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(highscore_surface, (337, 170, 50, 50))
    screen.blit(next_surface, (375, 315, 50, 50))

    # only blit if game is over
    if game.game_over:
        if flicker:
            screen.blit(game_over_surface, (330, 545, 50, 50))
            screen.blit(game_over_surface_2, (345, 580, 35, 35))

    # draw rects for gui
    pygame.draw.rect(screen, LIGHT_BLUE, score_rect, 0, 10)
    pygame.draw.rect(screen, LIGHT_BLUE, highscore_rect, 0, 10)
    pygame.draw.rect(screen, LIGHT_BLUE, next_rect, 0, 10)

    # blit score text
    screen.blit(
        score_value_surface, (
            score_value_surface.get_rect(
                centerx = score_rect.centerx, centery = score_rect.centery
            )
        )
    )
    screen.blit(
        highscore_value_surface, (
            highscore_value_surface.get_rect(
                centerx = highscore_rect.centerx, centery = highscore_rect.centery
            )
        )
    )

    # highscore management
    if highscore < game.score:
        highscore = round(game.score)
        backend.update(int(game.score))

    # draw game screen
    game.draw(screen)

    # paused handling
    if paused:

        # draw 50% opacity black rect over the screen
        paused_rect = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        paused_rect.fill((0, 0, 0, 128))
        screen.blit(paused_rect, (0, 0))

        # alternate between drawing the paused text and hiding it 
        # by using the flicker flag
        if flicker:
            rect = paused_surface.get_rect(center=(size * (cols / 2) + grid_offset, size * (rows / 2) + grid_offset))
            screen.blit(paused_surface, rect)

    # update display
    pygame.display.update()
    clock.tick(60)