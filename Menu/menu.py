#!/usr/bin/python
# -*- coding: utf-8 -*-

# from Menu.Buttons import Button
from Statistics.statistics import *
import os
from Instructions.instructions import *

# zmiana katalogu roboczego na "Mastermind_AiR_4b"
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
print(os.getcwd())
import main_singleplayer  # zaimportowałem dopiero tutaj, żeby PATH się zgadzał


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
        self.new_g = Button((0, 100, 200), 442, 160, 140, 60, "New Game")
        self.new_g.draw(self.display_surf)

        # rysuje przycisk "Wczytaj"
        self.load = Button((0, 100, 200), 442, 230, 140, 60, "Load Game")
        self.load.draw(self.display_surf)

        # rysuje przycisk "Statystyki"
        self.stats = Button((0, 100, 200), 442, 300, 140, 60, "High Scores")
        self.stats.draw(self.display_surf)

        # rysuje przycisk "Manuel :P"
        self.info = Button((0, 100, 200), 442, 370, 140, 60, "Instructions")
        self.info.draw(self.display_surf)

        # rysuje przycisk "Wyjscie"
        self.esc = Button((0, 100, 200), 442, 440, 140, 60, "Exit")
        self.esc.draw(self.display_surf)

        pygame.display.update()


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
                    settings = display_stats()
                    menu = Menu()
                elif menu.new_g.is_pointing(pos):
                    main_singleplayer.play_game()
                elif menu.info.is_pointing(pos):
                    info = display_instructions()
                    menu = Menu()


if __name__ == "__main__":
    pygame.init()
    main()
