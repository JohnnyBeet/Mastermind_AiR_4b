from src.game_classes import Button, GFXEntity
import pygame.freetype
import pygame.gfxdraw

# WORK IN PROGRESS
AVAILABLE_CODE_LENGHTS = [str(i) for i in range(3, 9)]
AVAILABLE_DIFFICULTY_LVLS = ["easy", "normal", "hard", "master"]


class TriangularButton(Button):
    " Przycisk używany do zmiany parametrów startowych gry "
    def __init__(self, pos: tuple, color: tuple, window: pygame.Surface, side, orientation):
        super().__init__(pos, color, window, (0, 0))
        self.side = side
        self.orientation = orientation  # left or right

    def draw(self):
        x = self._pos[0]
        y = self._pos[1]
        a = int(self.side / 2)
        y_offset = self.side
        x_offset = int(a * 1.73)
        if self.orientation == "right":
            self._rect = pygame.draw.polygon(self._window, self._color, [(x, y), (x, y + y_offset),
                                                                         (x + x_offset, y + a)])
        elif self.orientation == "left":
            self._rect = pygame.draw.polygon(self._window, self._color, [(x, y), (x, y + y_offset),
                                                                         (x - x_offset, y + a)])

    def change_value(self, i, i_range):
        """ Zmienia wartość zmiennej pod którą zostanie podpięty przycisk """
        if self.orientation == "left":
            if i - 1 in i_range:
                return i - 1
            else:
                return i
        elif self.orientation == "right":
            if i + 1 in i_range:
                return i + 1
            else:
                return i
        else:
            return i


class Display(GFXEntity):
    """ Klasa menu wyboru długości kodu oraz poziomu trudności """
    def __init__(self, pos, size, color, window, values, offset=0, font="gfx/ARCADECLASSIC.ttf", display_size=(60, 120),
                 font_size=30, font_color=(255, 255, 255)):
        super().__init__(pos, color, window, size)
        self.displayable_values = values
        self.displayed_value = values[0]
        self.value_index = 0
        self.values_range = [i for i, _ in enumerate(self.displayable_values)]
        self.font = pygame.freetype.Font(font, font_size)
        self.font_color = font_color
        self.offset = offset
        self.display_pos = pos[0] + offset, pos[1] + 15
        self.display_size = display_size
        self.display_rect = pygame.Rect(self.display_pos, self.display_size)
        self.left_button = TriangularButton((pos[0] - 100, pos[1]), (200, 0, 0), window, 50, "left")
        self.right_button = TriangularButton((pos[0] + 100, pos[1]), (200, 0, 0), window, 50, "right")

    def change_value(self, mouse_cords: list, clicked: list) -> list:
        """ Zmienia wartość wyświetlanej wartości zmiennej - trochę przekombinowane """
        if self.left_button._rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            self.value_index = self.left_button.change_value(self.value_index, self.values_range)
            self.displayed_value = self.displayable_values[self.value_index]
            if self.offset != 0:
                if self.displayed_value in ["easy", "hard"]:
                    self.offset = -30
                    self.display_pos = self._pos[0] + self.offset, self.display_pos[1]
                    self.display_rect = pygame.Rect(self.display_pos, self.display_size)
                elif self.displayed_value in ["normal", "master"]:
                    self.offset = -45
                    self.display_pos = self._pos[0] + self.offset, self.display_pos[1]
                    self.display_rect = pygame.Rect(self.display_pos, self.display_size)
            clicked = [False, True]

        if self.right_button._rect.collidepoint(mouse_cords[0], mouse_cords[1]) and clicked[0] and clicked[1]:
            self.value_index = self.right_button.change_value(self.value_index, self.values_range)
            self.displayed_value = self.displayable_values[self.value_index]
            if self.offset != 0:
                if self.displayed_value in ["easy", "hard"]:
                    self.offset = -30
                    self.display_pos = self._pos[0] + self.offset, self.display_pos[1]
                    self.display_rect = pygame.Rect(self.display_pos, self.display_size)
                elif self.displayed_value in ["normal", "master"]:
                    self.offset = -45
                    self.display_pos = self._pos[0] + self.offset, self.display_pos[1]
                    self.display_rect = pygame.Rect(self.display_pos, self.display_size)
            clicked = [False, True]

        return clicked

    def draw(self):
        super(Display, self).draw()
        self.left_button.draw()
        self.right_button.draw()
        self.font.render_to(self._window, self.display_rect, self.displayed_value, self.font_color)


class GameSettingMenu(GFXEntity):
    """ Klasa menu wyboru długości zgadywanego kodu oraz poziomu trudności gry """
    def __init__(self, pos, color, window, size):
        super().__init__(pos, color, window, size)
        self.code_lenght_display = Display((pos[0] + 200, pos[1] + 30), (200, 80),
                                           color, window, AVAILABLE_CODE_LENGHTS)
        self.difficulty_display = Display((pos[0] + 200, pos[1] + 130), (200, 80),
                                          color, window, AVAILABLE_DIFFICULTY_LVLS, -30)
        self.button = Button((175, 450), (0, 100, 0), self._window, (260, 80))

    def draw(self):
        super(GameSettingMenu, self).draw()
        self.code_lenght_display.draw()
        self.difficulty_display.draw()
        self.button.draw()

    def check(self, mouse_cords, clicked) -> list:
        clicked = self.code_lenght_display.change_value(mouse_cords, clicked)
        clicked = self.difficulty_display.change_value(mouse_cords, clicked)
        clicked = self.button.interact(mouse_cords, clicked)
        return clicked

    def return_game_settings(self) -> tuple:
        if self.button.clicked:
            code_lenght = int(self.code_lenght_display.displayed_value)
            available_diff_lvls = {"easy": 4 * code_lenght, "normal": 3 * code_lenght, "hard": 2 * code_lenght,
                                   "master": code_lenght}
            diff_lvl = available_diff_lvls[self.difficulty_display.displayed_value]
            return code_lenght, diff_lvl
        else:
            return None, None
