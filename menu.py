#!/usr/bin/python
# -*- coding: utf-8 -*-

# from Menu.Buttons import Button
from Statistics.statistics import *
from Instructions.instructions import *
from game import main_singleplayer


class Menu:

    """ Główne menu gry """
    def __init__(self):
        self.display_surf = None
        self.size = self.width, self.height = 1024, 576
        self.color = (255, 192, 203)

        pygame.init()

        # narysuj tło
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display_surf.fill(self.color)

        # rysuje tytuł
        self.title = "MASTERMIND"
        font = pygame.font.SysFont('comicsans', 62)
        title = font.render(self.title, 1, (47, 23, 56))
        self.display_surf.blit(title, (self.width/2 - title.get_width()/2, self.height/6 - title.get_height()/6,))

        # rysuje przycisk "Nowa gra"
        self.new_g = Button((0, 100, 200), 442, 160, 140, 60, 24, "New Game")
        self.new_g.draw(self.display_surf)

        # rysuje przycisk "Wczytaj"
        self.load = Button((0, 100, 200), 442, 230, 140, 60, 24, "Load Game")
        self.load.draw(self.display_surf)

        # rysuje przycisk "Statystyki"
        self.stats = Button((0, 100, 200), 442, 300, 140, 60, 24, "High Scores")
        self.stats.draw(self.display_surf)

        # rysuje przycisk "Manuel :P"
        self.info = Button((0, 100, 200), 442, 370, 140, 60, 24, "Instructions")
        self.info.draw(self.display_surf)

        # rysuje przycisk "Wyjscie"
        self.esc = Button((0, 100, 200), 442, 440, 140, 60, 24, "Exit")
        self.esc.draw(self.display_surf)

        pygame.display.update()


class ChooseGame:
    pygame.init()
    """ klasa menu wyboru rozgrywki """
    def __init__(self):
        self.size = self.width, self.height = 1024, 576
        self.color = (255, 192, 203)
        self.background = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background.fill(self.color)
        self.title = "Wybierz tryb gry"

        # rysuje tytuł
        font = pygame.font.SysFont('comicsans', 62)
        title = font.render(self.title, 1, (47, 23, 56))
        self.background.blit(title,
                               (self.width / 2 - title.get_width() / 2, self.height / 6 - title.get_height() / 6,))

        # rysuje przycisk zwykłego masterminda
        self.normal = Button((0, 100, 200), 116, 228, 280, 120, 34, "Klasyczny Mastermind")
        self.normal.draw(self.background)

        # rysuje przycisk trybu słownego
        self.word = Button((0, 100, 200), 628, 228, 280, 120, 34, "Tryb Słowny")
        self.word.draw(self.background)

        # rysuje przycisk powrotu do menu
        self.back = Button((0, 100, 200), 442, 428, 140, 60, 24, "Powrót")
        self.back.draw(self.background)

        pygame.display.update()


def choose_game(save, load, check_b):
    pygame.init()
    is_done = False
    choice = ChooseGame()
    while not is_done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if choice.normal.is_pointing(pos):
                    main_singleplayer.GAME_MODE = "Peg"
                    main_singleplayer.play_game(save, load, check_b, 0)
                elif choice.word.is_pointing(pos):
                    main_singleplayer.GAME_MODE = "Letter"
                    main_singleplayer.play_game(save, load, check_b, 0)
                elif choice.back.is_pointing(pos):
                    is_done = True


def main():
    menu = Menu()
    settings = None
    is_running = True

    while is_running:
        ''' Główna pętla gry i obsługa eventów'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu.esc.is_pointing(pos):
                    is_running = False
                elif menu.stats.is_pointing(pos):
                    display_stats()
                    menu = Menu()
                elif menu.new_g.is_pointing(pos):
                    save = Button((255, 0, 100), 500, 645, 150, 50, 24, 'Zapisz')
                    load = Button((255, 0, 100), 325, 645, 150, 50, 24, 'Wczytaj')
                    check_b = Button((255, 0, 100), 150, 645, 150, 50, 24, 'Sprawdz')
                    choose_game(save, load, check_b)
                    # main_singleplayer.play_game()
                    menu = Menu()
                elif menu.info.is_pointing(pos):
                    display_instructions()
                    menu = Menu()
                elif menu.load.is_pointing(pos):
                    save = Button((255, 0, 100), 500, 645, 150, 50, 24, 'Zapisz')
                    load = Button((255, 0, 100), 325, 645, 150, 50, 24, 'Wczytaj')
                    check_b = Button((255, 0, 100), 150, 645, 150, 50, 24, 'Sprawdz')
                    main_singleplayer.play_game(save, load, check_b, 1)


if __name__ == "__main__":
    pygame.init()
    main()
