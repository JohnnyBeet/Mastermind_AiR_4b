#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from Menu.Buttons import Button


class TutorialScreen:
    """ Klasa odpowiedzialna za każdy z ekranów tutoriala"""
    def __init__(self, file_location: str):
        self.size = 1024, 576
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((255, 255, 255))
        self.background = pygame.image.load(file_location)
        self.screen.blit(self.background, (0, 0))
        self.next = None
        self.previous = None

        # dodaje przycisk powrotu do menu
        self.ret_menu = Button((242, 209, 107), 830, 460, 140, 60, 24, "Menu")
        self.ret_menu.draw(self.screen)
        pygame.display.update()

    def add_next_button(self, pos: tuple):
        self.next = Button((242, 209, 107), pos[0], pos[1], 140, 60, 24, "Dalej")
        self.next.draw(self.screen)
        pygame.display.update()

    def add_previous_button(self, pos: tuple):
        self.previous = Button((242, 209, 107), pos[0], pos[1], 140, 60, 24, "Wstecz")
        self.previous.draw(self.screen)
        pygame.display.update()

# TODO: dodaj wybór pomiędzy zwykłym mastermindem a trybem słownym


def display_instructions():
    pygame.init()
    is_done = False
    screen = TutorialScreen('Instructions/graphics/plansza1.jpg')
    screen.add_next_button((426, 460))
    screen_number = 1
    """ Main loop tutoriala """
    while not is_done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if screen.ret_menu.is_pointing(pos):
                    is_done = True
                elif screen.next.is_pointing(pos):
                    screen_number += 1
                    screen = TutorialScreen('Instructions/graphics/plansza' + str(screen_number) + '.jpg')
                    if 0 < screen_number < 5:
                        screen.add_next_button((426, 460))
                        screen.add_previous_button((54, 460))
                    elif 5 <= screen_number < 10:
                        screen.add_next_button((680, 460))
                        screen.add_previous_button((530, 460))
                elif screen_number > 1:
                    if screen.previous.is_pointing(pos):
                        screen_number -= 1
                        screen = TutorialScreen('Instructions/graphics/plansza' + str(screen_number) + '.jpg')
                        if 1 < screen_number < 5:
                            screen.add_next_button((426, 460))
                            screen.add_previous_button((54, 460))
                        elif 5 <= screen_number < 10:
                            screen.add_next_button((680, 460))
                            screen.add_previous_button((530, 460))
                        else:
                            screen.add_next_button((426, 460))
