import pygame
import random
import Statistics.statistics as stat
from abc import ABC
from src.settings_loading import colors

""" data jest tymczasowym obiektem, który zbiera info z danej rozgrywki """
data = stat.Stats()
data.load_stats()  # wczytuje poprzednie statystyki, zeby ich nie utracic


class GFXEntity(ABC):
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

    _state = 0

    """ Klasa kołka/kamyczka (w zależności od interpretacji wizualnej) """
    def __init__(self, pos: tuple, color: tuple, radius: int, window: pygame.Surface):
        super().__init__(pos, color, window)
        self._radius = radius
        self._rect = pygame.draw.circle(self._window, self._color, self._pos, self._radius)

    def draw(self):
        """ Rysuje kołek w wskazanym oknie """
        pygame.draw.circle(self._window, self._color, self._pos, self._radius)

    def change(self, mouse_cords: list, clicked: list) -> list:
        """ Metoda służy do zmieniania koloru kołka.
            Zwraca listę z wartościami boolowskimi, które są używane
            w niezawodnym systemie wprowadzania informacji z myszki
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

    active_row = 0

    def __init__(self, pos: tuple, size: tuple, color: tuple, window: pygame.Surface, n_pegs: int, rows: int):
        super().__init__(pos, color, window, size)
        self._n_pegs = n_pegs
        self.n_rows = rows

        """ Skalowanie rozmiaru kołków na planszy w zależności od ich ilości """
        self.scaling_coeff = 5 - rows/n_pegs
        self.peg_offset_x = 50 + (3-n_pegs) * 20
        self.peg_offset_y = round(-45 + 30 * self.scaling_coeff)
        if n_pegs >= 5 or n_pegs == 4 and rows < 12:
            self.peg_offset_y -= 50
        self.change_x = 600/n_pegs
        self.change_y = 550/rows
        self.peg_size = self.scaling_coeff * self.change_x/14
        self.peg_size = round(self.peg_size)
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
                    self.rows_of_pegs[i].append(Peg((150 + self.peg_offset_x + round(self.change_x*j),
                                                     100 + self.peg_offset_y + round(self.change_y*i)),
                                                    (255, 255, 255), self.peg_size, self._window))
        """ Definicja przycisku na planszy """
        self.button = CheckButton((300, 645), (255, 0, 100), self._window, (200, 50))
        self._message = "Rozpoczales    nowa    gre"

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

    def get_rects(self):
        rects = [self.button.get_rect()]
        for row in self.rows_of_pegs:
            for peg in row:
                rects.append(peg._rect.copy())
        return rects


class Button(GFXEntity):
    """ Klasa przycisku """

    clicked = False

    def __init__(self, pos: tuple, color: tuple, window: pygame.Surface, size):
        super().__init__(pos, color, window, size)

    def interact(self, mouse_cords, clicked):
        if self._rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            self.clicked = True
            return [False, True]
        else:
            self.clicked = False
            return clicked


class CheckButton(Button):
    """ Przycisk używany na planszy do sprawdzenia stanu gry """
    def __init__(self, pos: tuple, color: tuple, window: pygame.Surface, size):
        super().__init__(pos, color, window, size)

    def click_button(self, board: Board, mouse_cords: tuple, clicked: tuple) -> list:
        """ Sprawdza czy przycisk został wciśnięty oraz czy gracz nie zgadł kodu. """
        active_row = board.active_row
        winning_pegs = board.winning_pegs
        rows_of_pegs = board.rows_of_pegs
        board_state = []
        n_pegs = board._n_pegs
        for peg in rows_of_pegs[active_row]:
            board_state.append(peg._color)

        if self._rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            if board_state != [(255, 255, 255) for _ in range(n_pegs)] != winning_pegs:
                if board_state == winning_pegs:
                    board.change_message("win")
                    data.won_matches += 1  # jesli wygralismy, trzeba to odnotowac
                    data.win_percentage = (data.won_matches/data.played_matches) * 100
                    data.save_stats()
                    return [False, False]
                else:
                    # zlicza ile kolorów zostało trafionych przez gracza
                    bulls, cows = 0, 0
                    already_used_user = [False for _ in range(n_pegs)]
                    already_used_secret = [False for _ in range(n_pegs)]
                    for i, value in enumerate(board_state):
                        if value == winning_pegs[i]:
                            bulls += 1
                            already_used_secret[i] = True
                            already_used_user[i] = True
                    for i in range(n_pegs):
                        for j in range(n_pegs):
                            if already_used_user[j] or already_used_secret[i]:
                                continue
                            if winning_pegs[i] == board_state[j]:
                                cows += 1
                                already_used_secret[i] = True
                                already_used_user[j] = True

                    board.change_message(f'{board.active_row+1}{" "*8}Row{" "*8}{bulls}{" "*8}bulls{" "*8}{cows}{" "*8}'
                                         f'cows')
                    active_row += 1
                    if active_row >= board.n_rows:
                        board.change_message("lose")
                        return [False, False]
                clicked = [False, True]
            else:
                board.change_message("Wszystkie    pola    nie    moga    byc    puste!")
        board.active_row = active_row
        return clicked

    def get_rect(self):
        return self._rect.copy()
