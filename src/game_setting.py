from src.game_classes import Button, GFXEntity
import pygame.freetype
import pygame.gfxdraw
from src.settings_loading import game_configs, menu_button_configs, colors

AVAILABLE_CODE_LENGHTS = [str(i) for i in range(3, 7)]
AVAILABLE_DIFFICULTY_LVLS = ["easy", "normal", "hard", "master"]


class TriangularButton(Button):
    """ Przycisk używany do zmiany parametrów startowych gry """

    def __init__(
        self, pos: tuple, color: tuple, window: pygame.Surface, side, orientation, id_range
    ):
        super().__init__(pos, color, window, (0, 0))
        self.side = side
        self.orientation = orientation  # left or right
        self._value_id = 0
        self.id_range = id_range

    @property
    def value_id(self):
        return self._value_id

    @value_id.setter
    def value_id(self, new_id):
        if new_id in self.id_range:
            self._value_id = new_id

    def change(self):
        """ Zmienia wartość zmiennej pod którą zostanie podpięty przycisk """
        if self.orientation == "left":
            if self._value_id - 1 in self.id_range:
                self._value_id -= 1

        elif self.orientation == "right":
            if self._value_id + 1 in self.id_range:
                self._value_id += 1

    def draw(self):
        x, y = self._pos
        a = int(self.side / 2)
        y_offset = self.side
        x_offset = int(a * 1.73)
        if self.orientation == "right":
            self._rect = pygame.draw.polygon(
                self._window,
                self._color,
                [(x, y), (x, y + y_offset), (x + x_offset, y + a)],
            )
        elif self.orientation == "left":
            self._rect = pygame.draw.polygon(
                self._window,
                self._color,
                [(x, y), (x, y + y_offset), (x - x_offset, y + a)],
            )

    def get_rect(self):
        return self._rect.copy()


class Display(GFXEntity):
    """ Klasa menu wyboru długości kodu oraz poziomu trudności """

    default_offset = 0
    value_index = 0
    button_color = (200, 0, 0)
    button_side = 50
    button_gap = 100

    def __init__(
        self,
        pos,
        size,
        color,
        window,
        values,
        font=game_configs["font_path"],  # ścieżka dostępu do pliku używanej czcionki
        display_size=(60, 120),
        font_size=30,
        font_color=colors["white"],
    ):
        super().__init__(pos, color, window, size)
        self.displayable_values = values
        self._displayed_value = values[0]
        self.values_range = [i for i, _ in enumerate(self.displayable_values)]
        self.font = pygame.freetype.Font(font, font_size)
        self.font_color = font_color
        self.display_size = display_size
        x, y = pos
        self.left_button = TriangularButton(
            (x - self.button_gap, y),
            self.button_color,
            window,
            self.button_side,
            "left",
            self.values_range
        )
        self.right_button = TriangularButton(
            (x + self.button_gap, y),
            self.button_color,
            window,
            self.button_side,
            "right",
            self.values_range
        )

    @property
    def offset(self):
        if self._displayed_value in ["easy", "hard"]:
            self.default_offset = -30
        elif self._displayed_value in ["normal", "master"]:
            self.default_offset = -45
        return self.default_offset

    @property
    def display_pos(self):
        x, y = self._pos
        return x + self.offset, y + 15

    @property
    def display_rect(self):
        return pygame.Rect(self.display_pos, self.display_size)

    @property
    def displayed_value(self):
        """ Zmienia wartość wyświetlanej wartości zmiennej """
        previous_value = self._displayed_value
        id_l, id_r = self.left_button.value_id, self.right_button.value_id

        if id_l != id_r:
            if self.displayable_values[id_l] == previous_value:
                self._displayed_value = self.displayable_values[id_r]
                self.left_button.value_id = id_r
            elif self.displayable_values[id_r] == previous_value:
                self._displayed_value = self.displayable_values[id_l]
                self.right_button.value_id = id_l

        return self._displayed_value

    def draw(self):
        super(Display, self).draw()
        self.left_button.draw()
        self.right_button.draw()
        self.font.render_to(
            self._window, self.display_rect, self.displayed_value, self.font_color
        )


class GameSettingMenu(GFXEntity):
    """ Klasa menu wyboru długości zgadywanego kodu oraz poziomu trudności gry """

    display_size = 200, 80  # rozmiar pojedyńczego interfejsu
    x_offset = 290  # bazowy odstęp od lewej krawędzi menu
    y_offset = 120  # bazowy odstęp od górnej krawędzi menu
    another_display_offset = 160  # odstęp osi y pomiędzy interfejsami ustawień gry

    def __init__(self, pos, color, window, size):
        super().__init__(pos, color, window, size)
        x, y = pos
        self.code_lenght_display = Display(
            (x + self.x_offset, y + self.y_offset),
            self.display_size,
            color,
            window,
            AVAILABLE_CODE_LENGHTS,
        )
        self.difficulty_display = Display(
            (x + self.x_offset, y + self.y_offset + self.another_display_offset),
            self.display_size,
            color,
            window,
            AVAILABLE_DIFFICULTY_LVLS,
        )
        self.button = Button(
            menu_button_configs["pos"],
            menu_button_configs["color"],
            self._window,
            menu_button_configs["size"],
        )

    def draw(self):
        """ Rusyje menu wraz z interfejsem ustawień gry """
        super(GameSettingMenu, self).draw()
        self.code_lenght_display.draw()
        self.difficulty_display.draw()
        self.button.draw()

    def return_game_settings(self) -> tuple:
        if self.button.clicked:
            code_lenght = int(self.code_lenght_display.displayed_value)
            available_diff_lvls = {
                "easy": 4 * code_lenght,
                "normal": 3 * code_lenght,
                "hard": 2 * code_lenght,
                "master": code_lenght,
            }
            diff_lvl = available_diff_lvls[self.difficulty_display.displayed_value]
            return code_lenght, diff_lvl
        else:
            return None, None

    @property
    def rects(self):
        """ Zwraca obiekty typu rect potrzebne to sprawdzania kolizji z myszką """
        rects = [
            self.button._rect.copy(),
            self.difficulty_display.left_button.get_rect().copy(),
            self.difficulty_display.right_button.get_rect(),
            self.code_lenght_display.left_button.get_rect(),
            self.code_lenght_display.right_button.get_rect(),
        ]
        return rects

    @property
    def elements(self):
        """ Zwraca obiekty należące do menu """
        elems = [
            self.button,
            self.difficulty_display.left_button,
            self.difficulty_display.right_button,
            self.code_lenght_display.left_button,
            self.code_lenght_display.right_button,
        ]
        return elems
