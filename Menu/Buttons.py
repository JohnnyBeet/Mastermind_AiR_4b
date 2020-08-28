#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class Button:
    """ ta klasa określa tylko przyciski prostokątne """
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x    # koordynaty lewego, górnego rogu prostokąta
        self.y = y
        self.width = width    # wymiary
        self.height = height
        self.text = text    # tekst do wyświetlenia na przycisku

    def draw(self, window, outline = None):
        """ rysuje przycisk (z obramówką lub bez) """
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text:
            font = pygame.font.SysFont('comicsans', 24)
            text = font.render(self.text, 1, (0, 0, 0))    # zwraca tekst jako "Surface"
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                               self.y + (self.height/2 - text.get_height()/2)))    # ustawia tekst w środku przycisku

    def is_pointing(self, pos):
        """ sprawdza, czy kursor myszki najechał na przycisk """
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
