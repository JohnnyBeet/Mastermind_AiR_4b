#!/usr/bin/python
# -*- coding: utf-8 -*- 
import json
from src.game_classes import *


# nalezy utworzyc slownik my_dict, w ktorym beda znajdowaly sie informacje o kolorach kazdego z przyciskow na planszy
class SaveData:
    def __init__(self):
        # w self.colors chce przechowywac tabele, o stanie planszy gry
        self.colors = []
        self.active_row = 0
        self.n_pegs = 0
        self.rows = 0
        self.rows_of_pegs = None
        self.winning_code = []

    def save_game(self, state_tab, a_row, n_pegs_, rows):
        for z in state_tab:
            self.colors.append(z)
        for x in range(a_row, rows + 1):
            for o in range(n_pegs_):
                self.colors.append(colors['white'])
        self.active_row = a_row
        self.n_pegs = n_pegs_
        self.rows = rows
        # self.rows_of_pegs = [[] for _ in range(self.rows)]
        # for i, row in enumerate(self.rows_of_pegs):
        #     if not row:
        #         for j in range(self.n_pegs):
        #             self.rows_of_pegs[i].append(
        #                 Peg(
        #                     (
        #                         self.base_peg_x
        #                         + self.peg_offset_x
        #                         + round(self.change_x * j),
        #                         self.base_peg_y
        #                         + self.peg_offset_y
        #                         + round(self.change_y * i),
        #                     ),
        #                     self.colors[j + i * self.n_pegs],
        #                     self.peg_size,
        #                     self._window,
        #                 )
        #             )

        with open('SaveAndLoadGame/save.txt', 'w') as outfile:
            json.dump(self.__dict__, outfile)
       
    def delete_savedgame(self):
        with open('SaveAndLoadGame/save.txt', 'r') as file:
            b = json.load(file)
        del b
          
    def load_game(self, saved_p):
        with open('SaveAndLoadGame/save.txt', 'r') as file:
            self.__dict__ = json.load(file)
            """ Rysuje planszę wraz z kołkami w wskazanym oknie """


