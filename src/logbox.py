from src.game_classes import GFXEntity
import pygame.freetype
from typing import Tuple


class LogBox(GFXEntity):
    """ Klasa okna dialogowego z logami na temat stanu gry """
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], color: Tuple[int, int, int],
                 text_color: Tuple[int, int, int], window: pygame.Surface, n_texts=3):
        super().__init__(pos, color, window)
        self._text_color = text_color
        self._size = size
        self._n_texts = n_texts
        self._pos = [(pos[0] + 20, pos[1] + 20 + j * 30) for j in range(self._n_texts)]
        self._rects = [pygame.Rect(self._pos[i], (20, 20)) for i in range(self._n_texts)]
        self._texts = ["" for _ in range(self._n_texts)]
        self._rect = pygame.Rect(self._pos[0], size)

    def load_text(self, input_text: str):
        """ Wczytuje log z gry na koniec okna dialogowego """
        if input_text != self._texts[-1]:
            for i, _ in enumerate(self._texts):
                if i < self._n_texts - 1:
                    self._texts[i] = self._texts[i+1]
                else:
                    self._texts[i] = input_text

    def print_text(self, font: pygame.freetype.Font):
        """ Wyświetla  okno dialogowe """
        self.draw()
        for i, text in enumerate(self._texts):
            font.render_to(self._window, self._rects[i], text, self._text_color)
