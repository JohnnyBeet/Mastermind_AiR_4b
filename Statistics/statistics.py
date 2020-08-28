#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import pygame
from Menu.Buttons import Button


class Stats:
    """ Klasa do przechowywania statystyk (zamysł jest taki: wczytaj z jsona staty,
    wrzuć do instancji klasy, edytuj pola w trakcie rozgrywki, zapisz po skończeniu) """
    def __init__(self):
        self.played_matches = 0
        self.won_matches = 0
        self.win_percentage = 0
        self.normal_mastermind = 0
        self.word_version = 0

    def save_stats(self):
        with open('Statistics/stats.txt', 'w') as outfile:
            json.dump(self.__dict__, outfile)

    def load_stats(self):
        with open('Statistics/stats.txt', 'r') as json_file:
            self.__dict__ = json.load(json_file)


class DisplayData:
    def __init__(self):
        self.size = self.width, self.height = 1024, 576
        self.color = (128, 205, 50)
        pygame.init()
        self.board = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.board.fill(self.color)

        # rysuje tytuł
        self.title = "Statystyki"
        font = pygame.font.SysFont('gfx/ARCADECLASSIC.TFF', 52)
        title = font.render(self.title, 1, (47, 23, 56))
        self.board.blit(title,
                         (self.width / 2 - title.get_width() / 2, self.height / 12 - title.get_height() / 12,))

        # rysuje przycisk "powrot"
        self.go_back = Button((0, 100, 200), 442, 420, 140, 60, "Powrót")
        self.go_back.draw(self.board)

        # pętla wypisująca zawartość stats.txt na ekran
        spacer = 120
        font = pygame.font.SysFont('gfx/ARCADECLASSIC.TFF', 34)
        data = Stats()
        data.load_stats()
        for name, number in data.__dict__.items():
            if name == "played_matches":
                text = font.render("Rozegrane gry  =  " + str(number), 1, (10, 10, 10))
                self.board.blit(text, (self.width / 5 - title.get_width() / 5, spacer))
                spacer += 60
                pygame.display.update()
            elif name == "won_matches":
                text = font.render("Wygrane gry  =  " + str(number), 1, (10, 10, 10))
                self.board.blit(text, (self.width / 5 - title.get_width() / 5, spacer))
                spacer += 60
                pygame.display.update()
            elif name == "win_percentage":
                text = font.render("Procent zwycięstw  =  " + str(number) + "%", 1, (10, 10, 10))
                self.board.blit(text, (self.width / 5 - title.get_width() / 5, spacer))
                spacer += 60
                pygame.display.update()
            elif name == "normal_mastermind":
                text = font.render('''Gry rozegrane w trybie "Mastermind"  =  ''' + str(number), 1, (10, 10, 10))
                self.board.blit(text, (self.width / 5 - title.get_width() / 5, spacer))
                spacer += 60
                pygame.display.update()
            elif name == "word_version":
                text = font.render('''Gry rozegrane w trybie słownym  =  ''' + str(number), 1, (10, 10, 10))
                self.board.blit(text, (self.width / 5 - title.get_width() / 5, spacer))
                spacer += 60
                pygame.display.update()
        pygame.display.update()


def display_stats():
    pygame.init()
    is_done = False
    display_data = DisplayData()
    while not is_done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if display_data.go_back.is_pointing(pos):
                    is_done = True
