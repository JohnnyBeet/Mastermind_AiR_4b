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


def display_instructions():
    pygame.init()
    is_done = False
    screen = TutorialScreen('Instructions/graphics/plansza1.jpg')
    screen_number = 1

    """ Poniższe dwa przyciski służą jako wybierajka w tutorialu"""
    classic = Button((242, 209, 107), 116, 228, 280, 120, 34, "Tryb Klasyczny")
    classic.draw(screen.screen)
    word = Button((242, 209, 107), 628, 228, 280, 120, 34, "Tryb Słowny")
    word.draw(screen.screen)
    pygame.display.update()

    word_flag = 0  # flaga, która zapobiega wciśnięciu przycisku classic, niewidocznego, ale znajdującego się na planszy z wersją słowną

    """ Main loop tutoriala """
    while not is_done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                """ Poniższy kod to jakaś smutna porażka, aż wstyd przyznawać się do takiego raka """
                if screen_number == 1:
                    pos = pygame.mouse.get_pos()
                    """ Wybierajka dla tutoriala"""
                    if classic.is_pointing(pos) and word_flag == 0:
                        screen_number += 1
                        screen = TutorialScreen('Instructions/graphics/plansza' + str(screen_number) + '.jpg')
                        screen.add_next_button((426, 460))
                        screen.add_previous_button((54, 460))
                    if word.is_pointing(pos):
                        screen = TutorialScreen('Instructions/graphics/word1.jpg')
                        word_flag = 1
                        """ Warunek powrotu do menu """
                if screen.ret_menu.is_pointing(pos):
                    is_done = True
                    word_flag = 0
                elif screen.next is not None:  # warunek, który pozwala na pozostanie na ekranie wersji słownej, aż do kliknięcia menu
                    if screen.next.is_pointing(pos):
                        """ obsługa kolejnych ekranów"""
                        screen_number += 1
                        screen = TutorialScreen('Instructions/graphics/plansza' + str(screen_number) + '.jpg')
                        """ dla ekranów od 1 do 5 rysuję przyciski w pewnych miejscach,
                            dla ekranów od 5 do 10 rysuje w innym miejscu """
                        if 0 < screen_number < 5:
                            screen.add_next_button((426, 460))
                            screen.add_previous_button((54, 460))
                        elif 5 <= screen_number < 10:
                            screen.add_next_button((680, 460))
                            screen.add_previous_button((530, 460))
                    elif screen_number > 1:
                        """ obsługa poprzednich ekranów (ale kolejnych do narysowania, chodzi o to że się cofamy) """
                        if screen.previous.is_pointing(pos):
                            screen_number -= 1
                            screen = TutorialScreen('Instructions/graphics/plansza' + str(screen_number) + '.jpg')
                            """ dla ekranów od 1 do 5 rysuję przyciski w pewnych miejscach,
                                dla ekranów od 5 do 10 rysuje w innym miejscu """
                            if 1 < screen_number < 5:
                                screen.add_next_button((426, 460))
                                screen.add_previous_button((54, 460))
                            elif 5 <= screen_number < 10:
                                screen.add_next_button((680, 460))
                                screen.add_previous_button((530, 460))
                            else:
                                """ Tutaj wracamy do 1 ekranu, czyli do wybierajki """
                                classic = Button((242, 209, 107), 116, 228, 280, 120, 34, "Tryb Klasyczny")
                                classic.draw(screen.screen)
                                word = Button((242, 209, 107), 628, 228, 280, 120, 34, "Tryb Słowny")
                                word.draw(screen.screen)
                                pygame.display.update()
