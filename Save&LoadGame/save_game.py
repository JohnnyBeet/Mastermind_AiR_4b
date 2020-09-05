#!/usr/bin/python
# -*- coding: utf-8 -*- 
import json
import src.game_classes.py

# nalezy utworzyc slownik my_dict, w ktorym beda znajdowaly sie informacje o kolorach kazdego z przyciskow na planszy
class SaveData:
    def __init__(self):
        # w self.colors chce przechowywac tabele, o stanie planszy gry
        self.colors = []
        self.active_row = 0
        self.n_pegs = 0

    def save_game(self,state_tab,a_row,,n_pegs_):
        self.active_row = a_row
        self.n_pegs = n_pegs_
        self.colors = state_tab
        with open('Save&LoadGame/save.txt', 'w') as outfile:
            json.dump(self.__dict__, outfile)
       
    def delete_savedgame(self)
         with open('Save&LoadGame/save.txt', 'r') as file:
            b= json.load(file)
          del b  
          
    def load_game(self):
        with open('Save&LoadGame/save.txt', 'r') as file:
            self.__dict__ = json.load(file)
            """ Rysuje planszę wraz z kołkami w wskazanym oknie """
        Board.draw()
        """Zmieniam kolory kołków"""
        for row in self.active_row:
            if row:
                for peg in self.n_pegs:
                    peg.color()=self.colors[row][peg]
        
