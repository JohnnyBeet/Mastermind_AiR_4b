#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

class PegGame:

    def __init__(self):
        self.colors = []
        self.n_pegs = 0
        self.active_row = 0

    def save_game(self):
        with open('state_of_the_game/save.txt','w') as outfile:
            json.dump(self.__dict__, outfile)

    def load_game(self):
        if self.n_pegs == 0:
            pass    # nie ma zapisanej gry
        else:
            with open('state_of_the_game/save.txt') as j_file:
                self.__dict__ = json.load(j_file)