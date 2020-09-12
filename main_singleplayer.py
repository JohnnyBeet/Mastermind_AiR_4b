import sys
import pygame.freetype
from src.game_setting import GameSettingMenu
from src.logbox import LogBox
from src.game_classes import Board, data
from src.settings_loading import (
    menu_configs,
    board_configs,
    logbox_configs,
    game_configs,
    colors
)

""" Główny plik gry uruchamiany z menu. Obsługuje zarówno tryb klasyczny jak i słowny Mastermind """

# TODO: przydałoby się również ładować i zapisywać poprzednio wybrany tryb gry (można skorzystać z json_data["_type"]
#  w pliku save_load_test.py)
# if loaded: #loaded bedzie klasa utworzona przy wczytywaniu gry
#     GAME_MODE = loaded.game_type
GAME_MODE = 'Peg'  # wstawienie tutaj 'Letter' uruchamia tryb słowny, a 'Peg' tryb z kolorami


def play_game(is_loaded=0):
    """ Ta funkcja jest konieczna do odpalenia gry z poziomu menu, uzycie exec() na tym pliku
        nie dawalo oczekiwanych rezultatow. """

    pygame.init()
    screen_size = game_configs["screen_size"]
    background = colors["black"]
    pygame.display.set_caption(game_configs["display_caption"])
    game_font = pygame.freetype.Font(
        game_configs["font_path"], game_configs["font_size"]
    )
    screen = pygame.display.set_mode(screen_size)
    peg_num = None
    row_num = None

    if not is_loaded:

        menu = GameSettingMenu(
            menu_configs["pos"], colors["aqua"], screen, menu_configs["size"]
        )

        menu.draw()  # pygame.Rect trójkątnych przycisków pojawiają się dopiero po narysowaniu
        clickable_rects = menu.rects
        mouse_logic_list = [False, True]
        while not (peg_num and row_num):
            """ Pętla menu wyboru parametrów gry """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_logic_list = [True, False]
                if event.type == pygame.MOUSEBUTTONUP:
                    first_check = False
                    second_check = False
                    if not pygame.mouse.get_pressed()[0] and mouse_logic_list[0]:
                        first_check = True
                    for rect in clickable_rects:
                        x, y = pygame.mouse.get_pos()
                        if rect.collidepoint(x, y):
                            second_check = True
                            break
                    if first_check and second_check:
                        mouse_logic_list = [True, True]
                    else:
                        mouse_logic_list = [False, True]

                screen.fill(background)
                menu.draw()
                mouse_logic_list = menu.check(pygame.mouse.get_pos(), mouse_logic_list)
                peg_num, row_num = menu.return_game_settings()
                pygame.display.flip()

    # dwa ify zapisujące statystyki rozegranych meczy w obu trybach
    if GAME_MODE == "Letter":
        data.played_matches += 1
        data.win_percentage = round((data.won_matches / data.played_matches) * 100)
        data.word_version += 1
        data.save_stats()
    elif GAME_MODE == "Peg":
        data.played_matches += 1
        data.win_percentage = round((data.won_matches / data.played_matches) * 100)
        data.normal_mastermind += 1
        data.save_stats()

    # TODO: board można tworzyć z zapisanych parametrów w następujący sposób:
    # if is_loaded:
        # peg_num = loaded.n_pegs
        # row_num = loaded.rows

    board = Board(
        board_configs["pos"],
        board_configs["size"],
        board_configs["color"],
        screen,
        peg_num,
        row_num,
        GAME_MODE  # wstawienie tutaj 'Letter' uruchamia tryb słowny, a 'Peg' tryb z kolorami
    )
    # TODO: sugestia, metoda load_game zwraca również struktury loaded_rows_of_pegs, loaded_winning_pegs,
    #  loaded_active_row, zatem wystarczy zrobić następującą podmianę aby wznowić już wcześniej zapisaną planszę board:
    # if is_loaded:
    #   board.rows_of_pegs = loaded.rows_of_pegs
    #   board.winning_pegs = loaded.winning_code
    #   board.active_row = loaded.active_row

    # TODO: logi z logbox'a też powinny być zapisywane i odczytywane
    logbox = LogBox(
        logbox_configs["pos"],
        logbox_configs["size"],
        logbox_configs["background_color"],
        logbox_configs["text_color"],
        screen,
        logbox_configs["number_of_messages_displayed"],
    )
    # można je podmienić następująco:
    # if is_loaded:
    #   logbox.texts = loaded_texts

    clickable_rects = board.rects
    mouse_logic_list = [
        False,
        True,
    ]  # [ LPM został wciśnięty , LPM został wciśnięty a później opuszczony ]
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
                first_check = False
                second_check = False
                if not pygame.mouse.get_pressed()[0] and mouse_logic_list[0]:
                    first_check = True
                for rect in clickable_rects:
                    x, y = pygame.mouse.get_pos()
                    if rect.collidepoint(x, y):
                        second_check = True
                        break
                if first_check and second_check:
                    mouse_logic_list = [True, True]
                else:
                    mouse_logic_list = [False, True]

        screen.fill(background)
        board.draw()
        mouse_logic_list = board.change(pygame.mouse.get_pos(), mouse_logic_list)
        mouse_logic_list = board.button.click_button(
            board, pygame.mouse.get_pos(), mouse_logic_list
        )
        logbox.load_text(board.message)
        logbox.print_text(game_font)
        lmb, rmb = mouse_logic_list
        end_game = not (lmb or rmb)  # po wygraniu gra sie konczy po jednym LPM
        pygame.display.flip()
