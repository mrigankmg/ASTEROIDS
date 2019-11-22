import sys
import pygame as pyg
import math

pyg.init()

WIDTH = 1280
HEIGHT = 720
BACKGROUND_COLOR   = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
PLAYER_COLOR = (245, 66, 66)
TEXT_POS = (68, 25)
PLAYER_POS = [(WIDTH//2 - 18, HEIGHT//2 + 24), (WIDTH//2, HEIGHT//2 - 24), (WIDTH//2 + 18, HEIGHT//2 + 24)]
PLAYER_PIVOT_POS = (WIDTH//2, HEIGHT//2+8)
PLAYER_ANGLE = 0
PLAYER_VELOCITY = 4
PLAYER_ROTATIONAL_VELOCITY = 0.1

screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption('Asteroids Neural Network')
font = pyg.font.Font('freesansbold.ttf', 28)
text = font.render('SCORE:', True, TEXT_COLOR, BACKGROUND_COLOR)
textRect = text.get_rect()
textRect.center = (TEXT_POS[0], TEXT_POS[1])
game_over = False

def rotate(clockwise=True):
    global PLAYER_POS
    if not clockwise:
        s = math.sin(-PLAYER_ROTATIONAL_VELOCITY)
        c = math.cos(-PLAYER_ROTATIONAL_VELOCITY)
    else:
        s = math.sin(PLAYER_ROTATIONAL_VELOCITY)
        c = math.cos(PLAYER_ROTATIONAL_VELOCITY)
    PLAYER_POS = [(PLAYER_POS[0][0] - PLAYER_PIVOT_POS[0], PLAYER_POS[0][1] - PLAYER_PIVOT_POS[1]), (PLAYER_POS[1][0] - PLAYER_PIVOT_POS[0], PLAYER_POS[1][1] - PLAYER_PIVOT_POS[1]), (PLAYER_POS[2][0] - PLAYER_PIVOT_POS[0], PLAYER_POS[2][1] - PLAYER_PIVOT_POS[1])]
    rotated_player_pos = []
    for i in PLAYER_POS:
        xnew = i[0] * c - i[1] * s;
        ynew = i[0] * s + i[1] * c;
        rotated_player_pos.append((xnew + PLAYER_PIVOT_POS[0], ynew + PLAYER_PIVOT_POS[1]))
    PLAYER_POS = rotated_player_pos

while not game_over:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit()
    keys_pressed = pyg.key.get_pressed()
    if keys_pressed[pyg.K_ESCAPE]:
        sys.exit()
    else:
        if keys_pressed[pyg.K_UP]:
            PLAYER_POS = [(PLAYER_POS[0][0], PLAYER_POS[0][1] - PLAYER_VELOCITY), (PLAYER_POS[1][0], PLAYER_POS[1][1] - PLAYER_VELOCITY), (PLAYER_POS[2][0], PLAYER_POS[2][1] - PLAYER_VELOCITY)]
            PLAYER_PIVOT_POS = (PLAYER_PIVOT_POS[0], PLAYER_PIVOT_POS[1] - PLAYER_VELOCITY)
        if keys_pressed[pyg.K_DOWN]:
            PLAYER_POS = [(PLAYER_POS[0][0], PLAYER_POS[0][1] + PLAYER_VELOCITY), (PLAYER_POS[1][0], PLAYER_POS[1][1] + PLAYER_VELOCITY), (PLAYER_POS[2][0], PLAYER_POS[2][1] + PLAYER_VELOCITY)]
            PLAYER_PIVOT_POS = (PLAYER_PIVOT_POS[0], PLAYER_PIVOT_POS[1] + PLAYER_VELOCITY)
        if keys_pressed[pyg.K_RIGHT]:
            PLAYER_POS = [(PLAYER_POS[0][0] + PLAYER_VELOCITY, PLAYER_POS[0][1]), (PLAYER_POS[1][0] + PLAYER_VELOCITY, PLAYER_POS[1][1]), (PLAYER_POS[2][0] + PLAYER_VELOCITY, PLAYER_POS[2][1])]
            PLAYER_PIVOT_POS = (PLAYER_PIVOT_POS[0] + PLAYER_VELOCITY, PLAYER_PIVOT_POS[1])
        if keys_pressed[pyg.K_LEFT]:
            PLAYER_POS = [(PLAYER_POS[0][0] - PLAYER_VELOCITY, PLAYER_POS[0][1]), (PLAYER_POS[1][0] - PLAYER_VELOCITY, PLAYER_POS[1][1]), (PLAYER_POS[2][0] - PLAYER_VELOCITY, PLAYER_POS[2][1])]
            PLAYER_PIVOT_POS = (PLAYER_PIVOT_POS[0] - PLAYER_VELOCITY, PLAYER_PIVOT_POS[1])
        if keys_pressed[pyg.K_d]:
            rotate()
        if keys_pressed[pyg.K_a]:
            rotate(clockwise=False)
        if keys_pressed[pyg.K_SPACE]:
            pass
    screen.fill(BACKGROUND_COLOR)
    pyg.draw.polygon(screen, PLAYER_COLOR, PLAYER_POS)
    screen.blit(text, textRect)
    pyg.display.flip()
