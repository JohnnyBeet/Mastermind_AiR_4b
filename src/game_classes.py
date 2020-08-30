import pygame
import pygame.freetype
import random
import Statistics.statistics as stat
from abc import ABC
from src.settings_loading import colors, checkbutton_configs, game_configs
from string import ascii_lowercase as allowed_characters
from state_of_the_game.peg_mode import PegGame

load_game = PegGame()

""" data jest tymczasowym obiektem, który zbiera info z danej rozgrywki """
data = stat.Stats()
data.load_stats()  # wczytuje poprzednie statystyki, zeby ich nie utracic


class GFXEntity(ABC):
    """ Klasa macierzysta zawierająca podstawowe parametry obiektu graficznego w pygame """

    def __init__(
        self, pos: tuple, color: tuple, window: pygame.Surface, size: tuple = (0, 0)
    ):
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
        self._rect = pygame.draw.circle(
            self._window, self._color, self._pos, self._radius
        )

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
        x, y = mouse_cords
        lmb, rmb = clicked  # sprawdza czy lewy i prawy przycisk myszy został wciśniety w odpowiedniej kolejności
        if self._rect.collidepoint(x, y) and lmb and rmb:
            self._state += 1
            clicked = [False, True]

        return clicked

    @property
    def color(self):
        return self._color

    @property
    def rect(self):
        return self._rect


class Letter(GFXEntity):

    _state = 0

    def __init__(
        self,
        pos: tuple,
        color: tuple,
        window: pygame.Surface,
        size: tuple,
        value,
        font_color: tuple,
        font_size=24,
        font_path="gfx/ARCADECLASSIC.TTF",
    ):
        super().__init__(pos, color, window, size)
        self._value = value  # obecnie wyświetlana literka
        self._font_color = font_color
        self._font_size = font_size
        self._font_path = font_path

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, change: str):
        """ Zmienia wartość literki - z np. 'a' na 'b'  na żądanie """
        if len(change) == 1 and change.lower() in allowed_characters:
            self._value = change.lower()
        else:
            raise TypeError("Oczekiwaliśmy pojedyńczej literki!")

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, new_size: int):
        """ Myślę że może się przydać przy jakimś skalowaniu planszy - ewentulnie się to usunie """
        if isinstance(new_size, int) and 4 <= new_size <= 40:
            self._font_size = new_size
        else:
            raise TypeError("Rozmiar czcionki wydaje się być nieprawidłowy!")

    @property
    def font_path(self) -> str:
        return self._font_path

    @property
    def font_color(self) -> tuple:
        return self._font_color

    @property
    def font(self) -> pygame.freetype.Font:
        return pygame.freetype.Font(self._font_path, self._font_size)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self._pos, self._size).copy()

    def draw(self):
        """ Rysuje literkę """
        GFXEntity.draw(self)
        self.font.render_to(self._window, self._rect, self._value, self._font_color)

    def change(self, mouse_cords: list, clicked: list) -> list:
        """ Metoda służy do zmieniania wartości literki.
            Zwraca listę z wartościami boolowskimi, które są używane
            w niezawodnym systemie wprowadzania informacji z myszki
        """

        # TODO: zmienić na input z klawiatury
        for i, value in enumerate(allowed_characters):
            if i == self._state:
                self._value = value
                if i == len(allowed_characters) - 1:
                    self._state = 0
                break

        x, y = mouse_cords
        lmb, rmb = clicked  # sprawdza czy lewy i prawy przycisk myszy został wciśniety w odpowiedniej kolejności
        if self._rect.collidepoint(x, y) and lmb and rmb:
            self._state += 1  # TODO: zamiast zmieniać stan literki to będzie tutaj wprowadzana nowa wartość
            clicked = [False, True]

        return clicked


class Board(GFXEntity):
    """ Klasa planszy """

    active_row = 0
    x, y = game_configs["screen_size"]
    change_x_base, change_y_base = (
        x - 200,
        y - 350,
    )  # gra w małych rozdzielczościach nie jest wskazana
    base_peg_x, base_peg_y = 150, 100

    def __init__(
        self,
        pos: tuple,
        size: tuple,
        color: tuple,
        window: pygame.Surface,
        n_pegs: int,
        rows: int,
        _type: str,
    ):
        super().__init__(pos, color, window, size)
        self._n_pegs = n_pegs
        load_game.n_pegs = n_pegs
        self.n_rows = rows
        self._type = _type

        """ Skalowanie rozmiaru kołków na planszy w zależności od ich ilości """
        self.scaling_coeff = 5 - rows / n_pegs
        self.peg_offset_x = 50 + (3 - n_pegs) * 20
        self.peg_offset_y = round(-45 + 30 * self.scaling_coeff)
        if n_pegs >= 5 or n_pegs == 4 and rows < 12:
            self.peg_offset_y -= 50
        self.change_x = self.change_x_base / n_pegs
        self.change_y = self.change_y_base / rows
        self.peg_size = self.scaling_coeff * self.change_x / 14
        self.peg_size = round(self.peg_size)

        if self._type == "Peg":
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
                        self.rows_of_pegs[i].append(
                            Peg(
                                (
                                    self.base_peg_x
                                    + self.peg_offset_x
                                    + round(self.change_x * j),
                                    self.base_peg_y
                                    + self.peg_offset_y
                                    + round(self.change_y * i),
                                ),
                                colors["white"],
                                self.peg_size,
                                self._window,
                            )
                        )
        elif self._type == "Letter":
            """ Generuje ukryty kod do zgadnięcia """

            n_pegs_to_str = {3: "three", 4: "four", 5: "five", 6: "six"}

            def random_line(afile):
                lines = open(afile).read().splitlines()
                myline = random.choice(lines)
                return myline

            file = f"WordVersion/{n_pegs_to_str[self._n_pegs]}_letter_words.txt"
            word = random_line(file)
            self.winning_pegs = [letter for letter in word]
            print(self.winning_pegs)

            """ Wypełnia pola w planszy pustymi polami. """
            self.rows_of_pegs = [[] for _ in range(rows)]
            for i, row in enumerate(self.rows_of_pegs):
                if not row:
                    for j in range(self._n_pegs):
                        self.rows_of_pegs[i].append(
                            Letter(
                                (
                                    self.base_peg_x
                                    + self.peg_offset_x
                                    + round(self.change_x * j),
                                    self.base_peg_y
                                    + self.peg_offset_y
                                    + round(self.change_y * i),
                                ),
                                colors["white"],
                                self._window,
                                (self.peg_size, self.peg_size),
                                "_",
                                colors["red"],
                            )
                        )

        """ Definicja przycisku na planszy """
        self.button = CheckButton(
            checkbutton_configs["pos"],
            checkbutton_configs["color"],
            self._window,
            checkbutton_configs["size"],
        )

        self._message = "Rozpoczales    nowa    gre"

    @property
    def type(self):
        return self._type

    def draw(self):
        """ Rysuje planszę wraz z kołkami w wskazanym oknie """
        pygame.draw.rect(self._window, self._color, self._rect)
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

    @property
    def message(self):
        return self._message

    def change_message(self, condition: str):
        if condition == "win":
            self._message = "WYGRALES  !"
        elif condition == "lose":
            self._message = "PRZEGRALES  !"
        else:
            self._message = condition

    def get_rects(self):
        """ Zwraca obiekty typu rect potrzebne to sprawdzania kolizji z myszką """
        rects = [self.button.get_rect()]
        for row in self.rows_of_pegs:
            for peg in row:
                rects.append(peg.rect.copy())
        return rects

    @property
    def n_pegs(self):
        return self._n_pegs


class Button(GFXEntity):
    """ Klasa przycisku """

    clicked = False

    def __init__(self, pos: tuple, color: tuple, window: pygame.Surface, size):
        super().__init__(pos, color, window, size)

    def interact(self, mouse_cords, clicked):
        x, y = mouse_cords
        lmb, rmb = clicked  # sprawdza czy lewy i prawy przycisk myszy został wciśniety w odpowiedniej kolejności
        if self._rect.collidepoint(x, y) and lmb and rmb:
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
        pegs_or_letters = Board.type
        active_row = board.active_row
        load_game.active_row = board.active_row
        winning_pegs = board.winning_pegs
        rows_of_pegs = board.rows_of_pegs
        n_pegs = board.n_pegs
        board_state = [
            item.color if pegs_or_letters == "Peg" else item.value for item in rows_of_pegs[active_row]
        ]

        load_game.colors.append(board_state)

        x, y = mouse_cords
        lmb, rmb = clicked  # sprawdza czy lewy i prawy przycisk myszy został wciśniety w odpowiedniej kolejności
        if self._rect.collidepoint(x, y) and lmb and rmb:
            if board_state != [colors["white"] for _ in range(n_pegs)] != winning_pegs:
                if board_state == winning_pegs:
                    board.change_message("win")
                    data.won_matches += 1  # jesli wygralismy, trzeba to odnotowac
                    data.win_percentage = round(
                        (data.won_matches / data.played_matches) * 100
                    )
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

                    board.change_message(
                        f'{board.active_row+1}{" "*8}Row{" "*8}{bulls}{" "*8}bulls{" "*8}{cows}{" "*8}'
                        f"cows"
                    )
                    active_row += 1
                    if active_row >= board.n_rows:
                        board.change_message("lose")
                        return [False, False]
                clicked = [False, True]
            else:
                board.change_message(
                    "Wszystkie    pola    nie    moga    byc    puste!"
                )
        board.active_row = active_row
        return clicked

    def get_rect(self):
        """ Zwraca obiekt typu rect potrzebny to sprawdzania kolizji z myszką """
        return self._rect.copy()
