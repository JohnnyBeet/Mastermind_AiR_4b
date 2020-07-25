from src.classes import *
import sys


pygame.init()
size = width, height = 600, 1000
background = colors["black"]
pygame.display.set_caption("Mastermind")
screen = pygame.display.set_mode(size)
board = Board((20, 20), (500, 700), (200, 100, 50), screen, 4, 8)
print(board.winning_pegs)  # just for testing purposes
mouse_logic_list = [False, True]  # [ LPM został wciśnięty , LPM został wciśnięty a później opuszczony ]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_logic_list = [True, False]
        if event.type == pygame.MOUSEBUTTONUP:
            if not pygame.mouse.get_pressed()[0] and mouse_logic_list[0]:
                mouse_logic_list = [True, True]
    screen.fill(background)
    board.draw()
    mouse_logic_list = board.interact(pygame.mouse.get_pos(), mouse_logic_list)
    mouse_logic_list = board.button.click_button(board, pygame.mouse.get_pos(), mouse_logic_list)
    pygame.display.flip()
