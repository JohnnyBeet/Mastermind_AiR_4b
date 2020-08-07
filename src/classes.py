import pygame
import random

""" Słownik nazwa koloru -> wartość RGB koloru. Można przenieść to później do jakiegoś pliku CONFIG.txt """
colors = {"white": (255, 255, 255), "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
          "purple": (200, 0, 255), "aqua": (0, 255, 255), "black": (0, 0, 0)}


class GFXEntity:
    """ Klasa macierzysta zawierająca podstawowe parametry obiektu graficznego w pygame """
    def __init__(self, pos: tuple, color: tuple, window: pygame.Surface, size: tuple = (0, 0)):
        self._pos = pos  # (x, y)
        self._color = color  # (R, G, B)
        self._size = size  # (długość, wysokość)
        self._window = window  # okno w którym będzie wyświetlany obiekt
        self._rect = pygame.Rect(pos, size)  # obiekt pygame.Rect używany do kolizji

    def draw(self):
        """ Rysuje obiekt w wskazanym oknie """
        pygame.draw.rect(self._window, self._color, self._rect)


class Peg(GFXEntity):
    """ Klasa kołka/kamyczka (w zależności od interpretacji wizualnej) """
    def __init__(self, pos: tuple, color: tuple, radius: int, window: pygame.Surface):
        super().__init__(pos, color, window)
        self._radius = radius
        self._rect = pygame.draw.circle(self._window, self._color, self._pos, self._radius)
        self._state = 0

    def draw(self):
        """ Rysuje kołek w wskazanym oknie """
        pygame.draw.circle(self._window, self._color, self._pos, self._radius)

    def change(self, mouse_cords: list, clicked: list) -> list:
        """ Metoda służy do zmieniania koloru kołka.
            Zwraca listę z wartościami boolowskimi, które są używane
            w niezawodnym systemie wprowadzania informacji z myszki (TRADEMARK)
        """
        for i, key in enumerate(colors):
            if i == self._state:
                self._color = colors[key]
                if i == len(colors) - 1:
                    self._state = 0
                break

        if self._rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            self._state += 1
            clicked = [False, True]

        return clicked


class Board(GFXEntity):
    """ Klasa planszy """
    def __init__(self, pos: tuple, size: tuple, color: tuple, window: pygame.Surface, n_pegs: int, rows: int):
        super().__init__(pos, color, window, size)
        self._n_pegs = n_pegs
        self.active_row = 0

        """ Generuje ukryty kod do zgadnięcia """
        self.winning_pegs = []
        for i in range(n_pegs):
            k = random.randint(0, len(colors) - 2)
            for j, key in enumerate(colors):
                if j == k:
                    self.winning_pegs.append(colors[key])
                    break

        """ Wypełnia pola w planszy białymi kołkami. """
        self.rows_of_pegs = [[] for _ in range(rows)]
        for i, row in enumerate(self.rows_of_pegs):
            if not row:
                for j in range(self._n_pegs):
                    self.rows_of_pegs[i].append(Peg((100 + j*50, 100 + i*50), (255, 255, 255), 20, self._window))
        """ Definicja przycisku na planszy """
        self.button = Button((150, 500), (255, 0, 100), self._window, (200, 50))
        self._message = "Jeszcze nic istotnego sie nie wydarzylo"

    def draw(self):
        """ Rysuje planszę wraz z kołkami w wskazanym oknie """
        pygame.draw.rect(self._window, (100, 200, 100), self._rect)
        self.button.draw()
        for row in self.rows_of_pegs:
            if row:
                for peg in row:
                    peg.draw()

    def interact(self, mouse_cords, clicked) -> list:
        """ Metoda sprawdza po kolei kołki na planszy, czy zostały kliknięte """
        for peg in self.rows_of_pegs[self.active_row]:
            clicked = peg.change(mouse_cords, clicked)
        return clicked

    def get_message(self):
        return self._message

    def change_message(self, condition: str):
        if condition == "win":
            self._message = "WYGRALES  !"
        elif condition == "lose":
            self._message = "PRZEGRALES  !"
        else:
            self._message = condition


class Button(GFXEntity):
    """ Klasa przycisku """
    def __init__(self, pos: tuple, color: tuple, window: pygame.Surface, size):
        super().__init__(pos, color, window, size)

    def click_button(self, board: Board, mouse_cords: tuple, clicked: tuple) -> list:
        """ Sprawdza czy przycisk został wciśnięty oraz czy gracz nie zgadł kodu.
            Nie jestem pewny, czy konieczne jest podawanie obiektu Planszy board.
            TODO: Rework aby to bez podawania board działało(jeżeli to możliwe)
        """
        active_row = board.active_row
        winning_pegs = board.winning_pegs
        rows_of_pegs = board.rows_of_pegs
        board_state = []
        for peg in rows_of_pegs[active_row]:
            board_state.append(peg._color)
        if self._rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            if board_state == winning_pegs:
                board.change_message("win")
                return [False, False]
            else:
                bulls, cows = 0, 0
                already_counted = []
                for i, value in enumerate(board_state):
                    if value == winning_pegs[i]:
                        bulls += 1
                    elif value in winning_pegs and value not in already_counted:
                        already_counted.append(value)
                        cows += 1
                board.change_message(f'{bulls} bulls    {cows}    cows')
                active_row += 1
                if active_row >= 8:
                    board.change_message("lose")
                    return [False, False]
            clicked = [False, True]
        board.active_row = active_row
        return clicked

