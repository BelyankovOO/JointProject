import pygame
from datetime import datetime
import os
import json
import system
FILE_NAME = "./leaderboard/highscore.json"


class Leaderboard(object):
    def __init__(self, file_name=FILE_NAME):
        self.font = pygame.font.SysFont("Century Gothic", 15)
        self.file_name = file_name
        if not os.path.isfile(self.file_name):
            self.on_empty_file()
        with open(file_name) as f:
            self.scores = json.load(f)

    def on_empty_file(self):
        tmp = {'Alex': (222, '22.04.1997'), 'Oleg': (111, '09.04.1998')}
        with open(self.file_name, "w") as f:
            f.write(json.dumps(tmp))

    def save_score(self, name, score):
        self.scores[name] = (score, str(datetime.date(datetime.now())))
        with open(self.file_name, 'r+') as f:
            f.write(json.dumps(self.scores))

    def add_leader_table(self, table):
        self.scores_list = self.scores.items()
        self.scores_list = sorted(self.scores_list, key=lambda x: x[1][0], reverse=False)
        self.scores_list = list(self.scores_list)[:system.LEADERBOARD_MAX_ROW]
        table.default_cell_padding = 5
        table.add_row(['№', 'Name', 'Best Time', 'Date'])
        for i, score in enumerate(self.scores_list, 1):
            row = (i, score[0], score[1][0], score[1][1])
            print(row)
            table.add_row(row)
