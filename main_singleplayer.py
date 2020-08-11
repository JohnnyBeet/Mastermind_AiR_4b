import pygame.freetype
from src.game_classes import Board, colors
from src.logbox import LogBox
from src.game_setting import GameSettingMenu
import sys

pygame.init()
# TODO: przenieść parametry init elementów gry do pliku SP_CONFIG.txt w formacie JSON
screen_size = width, height = 800, 900
background = colors["black"]
pygame.display.set_caption("Mastermind")
game_font = pygame.freetype.Font("gfx/ARCADECLASSIC.ttf", 18)
screen = pygame.display.set_mode(screen_size)

PEG_NUM = None
ROW_NUM = None

menu = GameSettingMenu((100, 100), colors["aqua"], screen, (600, 600))
mouse_logic_list = [False, True]

while not(PEG_NUM and ROW_NUM):
    """ Pętla menu wyboru parametrów gry """
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
        menu.draw()
        mouse_logic_list = menu.check(pygame.mouse.get_pos(), mouse_logic_list)
        PEG_NUM, ROW_NUM = menu.return_game_settings()
        pygame.display.flip()


board = Board((100, 20), (600, 850), (200, 100, 50), screen, PEG_NUM, ROW_NUM)
logbox = LogBox((210, 700), (350, 100), (0, 0, 0), (255, 255, 255), screen, 4)

winning_pegs_cn = [list(colors.keys())[list(colors.values()).index(i)] for i in board.winning_pegs]  # RGB -> color name
print(winning_pegs_cn)  # just for testing purposes

mouse_logic_list = [False, True]  # [ LPM został wciśnięty , LPM został wciśnięty a później opuszczony ]
end_game = False

while True:
    """ Główna pętla gry """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_logic_list = [True, False]
                if end_game:
                    sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if not pygame.mouse.get_pressed()[0] and mouse_logic_list[0]:
                mouse_logic_list = [True, True]

    screen.fill(background)
    board.draw()
    mouse_logic_list = board.interact(pygame.mouse.get_pos(), mouse_logic_list)
    mouse_logic_list = board.button.click_button(board, pygame.mouse.get_pos(), mouse_logic_list)
    logbox.load_text(board.get_message())
    logbox.print_text(game_font)
    end_game = not(mouse_logic_list[0] or mouse_logic_list[1])  # po wygraniu gra sie konczy po jednym LPM
    pygame.display.flip()
