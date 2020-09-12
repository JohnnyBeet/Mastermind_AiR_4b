#!/usr/bin/python
# -*- coding: utf-8 -*- 
import json
import pygame
screen = pygame.display.set_mode((400, 400))


#nalezy utworzyc slownik my_dict, w ktorym beda znajdowaly sie informacje o kolorach kazdego z przyciskow na planszy
class SaveData:
    def __init__(self):
        self.active_row = 0
        self.n_pegs = 0
        self.rows = 0
        self.game_type = None
        # self.rows_of_pegs = None
        self.winning_code = []
        self.texts = []

    def save_game(self, a_row, n_pegs_, rows, game_type, _rows_of_pegs, _winning_code):
        json_data = []
        if game_type == 'Peg':
            for i, row in enumerate(_rows_of_pegs):
                for peg in row:
                    json_data.append(peg.to_json())
            with open('SaveAndLoadGame/json_data.txt', 'w+') as f:
                json.dump(json_data, f)
        elif game_type == 'Letter':
            for i, row in enumerate(_rows_of_pegs):
                for letter in row:
                    json_data.append(letter.to_json())
            with open('SaveAndLoadGame/json_data.txt', 'w+') as f:
                json.dump(json_data, f)
        self.active_row = a_row
        self.n_pegs = n_pegs_
        self.rows = rows
        self.game_type = game_type
        # self.rows_of_pegs = _rows_of_pegs
        self.winning_code = _winning_code
        with open('SaveAndLoadGame/save.txt', 'w') as outfile:
            json.dump(self.__dict__, outfile)


    def load_game(self):
        with open('SaveAndLoadGame/save.txt', 'r') as file:
            self.__dict__ = json.load(file)
            
        with open('SaveAndLoadGame/logbox_texts.txt', 'r') as texts_file:
            self.texts = json.load(texts_file)

        with open('SaveAndLoadGame/json_data', 'r') as n:
            json_data = json.load(n)

        if self.game_type == 'Peg':
            saved_pegs = []
            for i, row in enumerate(self.rows_of_pegs):
                check = 0
                for peg in row:
                    saved_pegs.append(peg.from_json(json_data[check + i * self.n_pegs], screen))
                    check += 1
            for i in range(self.rows):
                for j in range(self.n_pegs):
                    self.rows_of_pegs = saved_pegs[i + j * self.rows]
        elif self.game_type == 'Letter':
            saved_letters = []
            for i, row in enumerate(self.rows_of_pegs):
                check = 0
                for letter in row:
                    saved_letters.append(letter.from_json(json_data[check + i * self.n_pegs], screen))
                    check += 1
            for i in range(self.rows):
                for j in range(self.n_pegs):
                    self.rows_of_pegs = saved_letters[i + j * self.rows]
                    
    def save_logbox(self, texts: list):
        with open('SaveAndLoadGame/logbox_texts.txt', 'w') as saved_text_file:
            json.dump(texts, saved_text_file) 
