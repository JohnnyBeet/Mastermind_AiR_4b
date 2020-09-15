import sys
import pygame.freetype
from menu import main
from src.game_setting import GameSettingMenu
from src.logbox import LogBox
from src.game_classes import Board, data, save_class, CheckButton, Peg
from src.settings_loading import (
    menu_configs,
    board_configs,
    logbox_configs,
    game_configs,
    colors
)

""" Główny plik gry uruchamiany z menu. Obsługuje zarówno tryb klasyczny jak i słowny Mastermind """

GAME_MODE = 'Peg'  # wstawienie tutaj 'Letter' uruchamia tryb słowny, a 'Peg' tryb z kolorami


def play_game(save, back, check_b, is_loaded=1):
    """ Ta funkcja jest konieczna do odpalenia gry z poziomu menu, uzycie exec() na tym pliku
        nie dawalo oczekiwanych rezultatow. """
    global GAME_MODE
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
    if is_loaded:
        save_class.load_game(screen)
    elif not is_loaded:

        menu = GameSettingMenu(
            menu_configs["pos"], colors["aqua"], screen, menu_configs["size"]
        )

        menu.draw()  # pygame.Rect trójkątnych przycisków pojawiają się dopiero po narysowaniu
        clickable_rects_menu = menu.rects
        elements_menu = menu.elements
        engaged_rect = None
        while not (peg_num and row_num):
            """ Pętla menu wyboru parametrów gry """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        for rect in clickable_rects_menu:
                            if rect.collidepoint(x, y):
                                engaged_rect = rect
                    else:
                        engaged_rect = None
                if event.type == pygame.MOUSEBUTTONUP:
                    if engaged_rect:
                        x, y = pygame.mouse.get_pos()
                        if not pygame.mouse.get_pressed()[0] and engaged_rect.collidepoint(x, y):
                            for element in elements_menu:
                                if element.rect == engaged_rect:
                                    element.change()
                                    engaged_rect = None

                screen.fill(background)
                menu.draw()
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

    if is_loaded:
        peg_num = save_class.n_pegs
        row_num = save_class.rows
        GAME_MODE = save_class.game_type

    board = Board(
        board_configs["pos"],
        board_configs["size"],
        board_configs["color"],
        screen,
        peg_num,
        row_num,
        GAME_MODE  # wstawienie tutaj 'Letter' uruchamia tryb słowny, a 'Peg' tryb z kolorami
    )

    if is_loaded:
        board.rows_of_pegs = save_class.rows_of_pegs
        board.winning_pegs = save_class.winning_code
        board.active_row = save_class.active_row

    logbox = LogBox(
        logbox_configs["pos"],
        logbox_configs["size"],
        logbox_configs["background_color"],
        logbox_configs["text_color"],
        screen,
        logbox_configs["number_of_messages_displayed"],
    )

    if is_loaded:
        logbox.texts = save_class.texts

    end_game = False
    engaged_rect_lmb = None
    engaged_rect_rmb = None

    while True:
        """ Główna pętla gry """

        clickable_rects = board.rects
        elements = board.elements

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if save.is_pointing(pos):
                    save_class.save_game(board.active_row, board.n_pegs, board.n_rows, GAME_MODE, board.rows_of_pegs,
                                         board.winning_pegs)
                    save_class.save_logbox(logbox.texts)
                elif back.is_pointing(pos):
                    pygame.display.quit()
                    main()
                elif end_game:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    for rect in clickable_rects:
                        if rect.collidepoint(x, y):
                            engaged_rect_lmb = rect
                            engaged_rect_rmb = None

                elif pygame.mouse.get_pressed()[2]:
                    for rect in clickable_rects:
                        if rect.collidepoint(x, y):
                            engaged_rect_rmb = rect
                            engaged_rect_lmb = None
                else:
                    engaged_rect_lmb = None
                    engaged_rect_rmb = None

            if event.type == pygame.MOUSEBUTTONUP:
                if engaged_rect_lmb:
                    x, y = pygame.mouse.get_pos()
                    if not pygame.mouse.get_pressed()[0] and engaged_rect_lmb.collidepoint(x, y):
                        for element in elements:
                            if element.rect == engaged_rect_lmb:
                                if isinstance(element, CheckButton):
                                    end_game = element.change(board)
                                else:
                                    element.change()
                                engaged_rect_lmb = None
                elif engaged_rect_rmb:
                    x, y = pygame.mouse.get_pos()
                    if not pygame.mouse.get_pressed()[2] and engaged_rect_rmb.collidepoint(x, y):
                        for element in elements:
                            if element.rect == engaged_rect_rmb:
                                if isinstance(element, Peg):
                                    element.change_reversed()
                                engaged_rect_rmb = None

        screen.fill(background)
        board.draw()
        save.draw(screen)
        back.draw(screen)
        check_b.draw(screen)
        logbox.load_text(board.message)
        logbox.print_text(game_font)
        pygame.display.flip()
