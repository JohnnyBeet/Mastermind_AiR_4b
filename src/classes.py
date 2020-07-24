import pygame
import random

"""Słownik nazwa koloru -> wartość RGB koloru. Można przenieść to później do jakiegoś pliku CONFIG.txt"""
colors = {"white": (255, 255, 255), "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
          "purple": (255, 0, 255), "aqua": (0, 255, 255), "black": (0, 0, 0)}


class Peg:
    def __init__(self, pos: tuple, color: tuple, radius: int, window: pygame.Surface):
        self._pos = pos  # (x, y)
        self._color = color  # (R, G, B)
        self._radius = radius
        self.window = window
        self.rect = pygame.draw.circle(self.window, self._color, self._pos, self._radius)
        self.state = 0

    def draw(self):
        """Rysuje kołek na ekranie"""
        pygame.draw.circle(self.window, self._color, self._pos, self._radius)

    def change(self, mouse_cords: list, clicked: list) -> list:
        """

            Metoda służy do zmieniania koloru kołka.
            Zwraca listę z wartościami boolowskimi,
            które są używane w niezawodnym systemie wprowadzania informacji z myszki (TRADEMARK)

        """

        for i, key in enumerate(colors):
            if i == self.state:
                self._color = colors[key]
                if i == len(colors) - 1:
                    self.state = 0
                break

        if self.rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            self.state += 1
            clicked = [False, True]

        return clicked


class Board:
    def __init__(self, pos: tuple, size: tuple, window: pygame.Surface, n_pegs: int, rows: int):
        self._pos = pos  # (x, y)
        self._size = size  # (width, height)
        self.button_rect = pygame.Rect((150, 500), (200, 50))
        self.rect = pygame.Rect(pos, size)
        self.window = window
        self._n_pegs = n_pegs
        self.active_row = 0
        self.winning_pegs = []
        for i in range(n_pegs):
            k = random.randint(0, len(colors) - 2)
            for j, key in enumerate(colors):
                if j == k:
                    self.winning_pegs.append(colors[key])
                    break
        self.rows_of_pegs = [[] for _ in range(rows)]

    def fill_rows(self):
        """
            Wypełnia pola w planszy białymi kołkami.
            Możliwe że można to przenieść  do __init__.
        """
        for i, row in enumerate(self.rows_of_pegs):
            if not row:
                for j in range(self._n_pegs):
                    self.rows_of_pegs[i].append(Peg((100 + j*50, 100 + i*50), (255, 255, 255), 20, self.window))

    def draw(self):
        """Rysuje planszę wraz z kołkami"""
        pygame.draw.rect(self.window, (100, 200, 100), self.rect)
        pygame.draw.rect(self.window, (255, 0, 100), self.button_rect)
        for row in self.rows_of_pegs:
            if row:
                for peg in row:
                    peg.draw()

    def interact(self, mouse_cords, clicked) -> list:
        """
            Metoda sprawdza po kolei kołki
            TODO: zoptymalizować
        """
        for peg in self.rows_of_pegs[self.active_row]:
            dummy = peg.change(mouse_cords, clicked)
            if not dummy == clicked:
                return dummy
        return clicked

    def click_button(self, mouse_cords, clicked) -> list:
        board_state = []
        for peg in self.rows_of_pegs[self.active_row]:
            board_state.append(peg._color)
        if self.button_rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            if board_state == self.winning_pegs:
                print("You won!")  # just for testing purposes
                return [False, False]
            else:
                self.active_row += 1
                if self.active_row >= 8:
                    self.active_row = 0
            clicked = [False, True]
        return clicked

