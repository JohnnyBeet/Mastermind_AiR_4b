#!/usr/bin/python
# -*- coding: utf-8 -*-
import json


# nalezy utworzyc slownik my_dict, w ktorym beda znajdowaly sie informacje o kolorach kazdego z przyciskow na planszy
class SaveData:
    def __init__(self,):
        # w self.colors chce przechowywac slownik, w ktorym beda informacje o kolorach kazdego przycisku
        self.colors = {}
        self.level = None
        self.active_row = 0
        self.n_pegs = 0

    def save_game(self,my_dict,a_row,lev,n_pegs_):
        with open('save.json', 'w') as outfile:
            json.dump(my_dict, outfile)
            self.colors = my_dict
            outfile.close()
        self.active_row = a_row
        self.n_pegs = n_pegs_
        self.level = lev

    def load_game(self):
        with open('save.json','r') as file:
            self.colors = json.load(file)
            file.close()
        # tutaj nalezy wywolac plansze z odpowiednimi danymi przechowywanymi w tej klasie
