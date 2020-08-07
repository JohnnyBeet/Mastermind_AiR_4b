from src.classes import *  # wczytuje wszystko z classes.py zatem może nie trzeba tego reworkować na "dobre praktyki"
from src.logbox import *  # tak samo jak wyżej
import sys


def get_code_lenght():
    # TODO: convert from TUI -> GUI
    available_range = [str(x) for x in range(3, 11)]
    code_lenght = input("Podaj dlugosc zgadywanego kodu(z zakresu od 3 do 10 znaków): ")
    while code_lenght not in available_range:
        print("Nieporawna dlugosc kodu!")
        code_lenght = input("Podaj dlugosc zgadywanego kodu(z zakresu od 3 do 10 znaków): ")
    return int(code_lenght)


def set_difficulty_lvl(code_lenght):
    # TODO: convert from TUI -> GUI
    available_diff_lvls = {"easy": 4 * code_lenght, "medium": 3 * code_lenght, "hard": 2 * code_lenght,
                           "impossible": code_lenght}
    print("Wybierz poziom trudnosci gry:")
    for i in available_diff_lvls.keys():
        print("{} - {} prób".format(i, available_diff_lvls[i]))
    diff = input("Wskaż poziom trudności na którym chcesz grać: ")
    while diff not in available_diff_lvls.keys():
        print("Niepoprawny poziom trudności!")
        diff = input("Wskaż poziom trudności na którym chcesz grać: ")
    return available_diff_lvls[diff]


pygame.init()
# TODO: przenieść parametry init elementów gry do pliku SP_CONFIG.txt w formacie JSON
screen_size = width, height = 600, 800
background = colors["black"]
pygame.display.set_caption("Mastermind")
game_font = pygame.freetype.Font("gfx/ARCADECLASSIC.ttf", 18)
screen = pygame.display.set_mode(screen_size)
PEG_NUM = get_code_lenght()
ROW_NUM = set_difficulty_lvl(PEG_NUM)
board = Board((20, 20), (500, 700), (200, 100, 50), screen, PEG_NUM, ROW_NUM)
logbox = LogBox((50, 550), (350, 100), (0, 0, 0), (255, 255, 255), screen, 4)
winning_pegs_cn = [list(colors.keys())[list(colors.values()).index(i)] for i in board.winning_pegs]  # RGB -> color name
print(winning_pegs_cn)  # just for testing purposes
mouse_logic_list = [False, True]  # [ LPM został wciśnięty , LPM został wciśnięty a później opuszczony ]
end_game = False
while True:
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
