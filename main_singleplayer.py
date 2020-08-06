from src.classes import *  # wczytuje wszystko z classes.py zatem może nie trzeba tego reworkować na "dobre praktyki"
from src.logbox import *  # tak samo jak wyżej
import sys

pygame.init()
screen_size = width, height = 600, 800
background = colors["black"]
pygame.display.set_caption("Mastermind")
game_font = pygame.freetype.Font("gfx/ARCADECLASSIC.ttf", 18)
screen = pygame.display.set_mode(screen_size)
board = Board((20, 20), (500, 700), (200, 100, 50), screen, 4, 8)
logbox = LogBox((50, 550), (350, 100), (0, 0, 0), (255, 255, 255), screen, 4)
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
    board.change_message()
    mouse_logic_list = board.interact(pygame.mouse.get_pos(), mouse_logic_list)
    mouse_logic_list = board.button.click_button(board, pygame.mouse.get_pos(), mouse_logic_list)
    logbox.load_text(board.get_message())
    logbox.print_text(game_font)
    pygame.display.flip()
