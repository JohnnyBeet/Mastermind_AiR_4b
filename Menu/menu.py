#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from Menu.Buttons import Button


class Menu:

    """ Główne menu gry """
    def __init__(self):
        self._running = True
        self.display_surf = None
        self.size = self.width, self.height = 640, 400
        self.color = (255, 192, 203)
        self._running = True

        pygame.init()
        # narysuj tło
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display_surf.fill(self.color)

        # rysuje tytuł
        self.title = "MASTERMIND"
        font = pygame.font.SysFont('comicsans', 52)
        title = font.render(self.title, 1, (47,23,56))
        self.display_surf.blit(title, (self.width/2 - title.get_width()/2, self.height/5 - title.get_height()/5,))

        # rysuje przycisk "Nowa gra"
        self.new_g = Button((0, 100, 200), 280, 140, 100, 40, "New Game")
        self.new_g.draw(self.display_surf)

        # rysuje przycisk "Wczytaj"
        self.load = Button((0, 100, 200), 280, 190, 100, 40, "Load Game")
        self.load.draw(self.display_surf)

        # rysuje przycisk "Statystyki"
        self.stats = Button((0, 100, 200), 280, 240, 100, 40, "High Scores")
        self.stats.draw(self.display_surf)

        # rysuje przycisk "Manuel :P"
        self.info = Button((0, 100, 200), 280, 290, 100, 40, "Instructions")
        self.info.draw(self.display_surf)

        # rysuje przycisk "Wyjscie"
        self.esc = Button((0, 100, 200), 280, 340, 100, 40, "Exit")
        self.esc.draw(self.display_surf)

        pygame.display.update()

    def on_event(self, event):
        """ Metoda odpowiedzialna za obsługe przycisków"""
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.esc.is_pointing(pos):
                self._running = False

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
        self.on_cleanup()


if __name__ == "__main__":
    theMenu = Menu()
    theMenu.on_execute()
