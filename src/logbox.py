from typing import Tuple
import pygame.freetype
from src.game_classes import GFXEntity


class LogBox(GFXEntity):
    """ Klasa okna dialogowego z logami na temat stanu gry """

    text_rect_size = text_x, text_y = (20, 20)
    text_gap = 30

    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        color: Tuple[int, int, int],
        text_color: Tuple[int, int, int],
        window: pygame.Surface,
        n_texts=3,
    ):
        super().__init__(pos, color, window)
        self._text_color = text_color
        self._size = size
        self._n_texts = n_texts
        x, y = pos
        self._pos = [
            (x + self.text_x, y + self.text_y + j * self.text_gap)
            for j in range(self._n_texts)
        ]
        self._rects = [
            pygame.Rect(rect_pos, self.text_rect_size) for rect_pos in self._pos
        ]
        self._texts = ["" for _ in self._pos]
        self._rect = pygame.Rect(self._pos[0], size)

    def load_text(self, input_text: str):
        """ Wczytuje log z gry na koniec okna dialogowego """
        if input_text != self._texts[-1] and not(input_text == "Rozpoczales    nowa    gre" and
                                                 input_text in self._texts):
            for i, _ in enumerate(self._texts):
                if i < self._n_texts - 1:
                    self._texts[i] = self._texts[i + 1]
                else:
                    self._texts[i] = input_text

    def print_text(self, font: pygame.freetype.Font):
        """ Wyświetla  okno dialogowe """
        self.draw()
        for i, text in enumerate(self._texts):
            font.render_to(self._window, self._rects[i], text, self._text_color)

    @property
    def texts(self):
        return self._texts

    @texts.setter
    def texts(self, loaded_texts: list):
        """ Setter to ustawiania logów z zapisanej poprzednio gry """
        if len(loaded_texts) == self._n_texts:
            self._texts = loaded_texts
        else:
            raise AttributeError(f"Liczba wiadomości w logach jest nieodpowiednia! - powinno ich być {self._n_texts}")
