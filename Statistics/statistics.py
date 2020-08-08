#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

class Stats:
    """ Klasa do przechowywania statystyk (zamysł jest taki: wczytaj z jsona staty,
    wrzuć do instancji klasy, edytuj pola w trakcie rozgrywki, zapisz po skończeniu) """
    def __init__(self):
        self.played_matches = 0
        self.won_matches = 0
        self.win_percentage = 0
        self.fav_gametype = {"Normal Mastermind": 0 , "Bulls & Cows": 0 }

    def save_stats(self):
        with open('Statistics/stats.txt', 'w') as outfile:
            json.dump(self.__dict__, outfile)


    def load_stats(self):
        with open('Statistics/stats.txt', 'r') as json_file:
            self.__dict__ = json.load(json_file)

#  TODO: zrób infterfejs graficzny dla statystyk