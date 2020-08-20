#!/usr/bin/python
# -*- coding: utf-8 -*-
import json


# nalezy utworzyc slownik my_dict, w ktorym beda znajdowaly sie informacje o kolorach kazdego z przyciskow na planszy
class SaveData:
    def __init__(self,):
        # w self.colors chce przechowywac tabele, o stanie planszy gry
        self.colors = []
        self.level = None
        self.active_row = 0
        self.n_pegs = 0

    def save_game(self,state_tab,a_row,lev,n_pegs_):
        self.active_row = a_row
        self.n_pegs = n_pegs_
        self.level = lev
        self.colors = state_tab
        with open('Save&LoadGame/save.txt', 'w') as outfile:
            json.dump(self.__dict__, outfile)
          
    def load_game(self):
        with open('Save&LoadGame/save.txt', 'r') as file:
            self.__dict__ = json.load(file)
        # tutaj nalezy wywolac plansze z odpowiednimi danymi przechowywanymi w tej klasie
