#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from tkinter import Tk, Label, messagebox, IntVar, Button
"""
    Jeu 2048 en mode texte version 0.0.5
    version POO
    interface graphique
    Todo: ajouter meilleur score
"""


def random_tile_value():
    """
        choisie nouvelle tuile dans la grille avec une probabilité:
        2: 9/10 et 4: 1/10
    """
    return random.choice([2] * 9 + [4])  # probabilité => 2: 9/10 ; 4:1/10


def tile_color(value):
    colors = {0:     '#848484',
              2:     '#FFFFFF',
              4:     '#FFFF6B',
              8:     '#FF7F00',
              16:    '#D6710C',
              32:    '#B9260A',
              64:    '#ED0000',
              128:   '#FFD700',
              256:   '#FFD700',
              512:   '#FFD700',
              1024:  '#FFD700',
              2048:  '#FFD700',
              4096:  '#FFD700',
              8192:  '#FFD700',
              16384: '#FFD700',
              32786: '#FFD700'}
    return colors[value]


class Grid(object):
    """ Objet représentant le jeu 2048 """
    def __init__(self):
        self.window = self.window_init()
        self.game_init()
        self.window.mainloop()

    def window_init(self):
        root = Tk()
        root.iconbitmap('favicon.ico')
        root.title('')
        root.bind_all('<Key-Down>', self.move_down)
        root.bind_all('<Key-Left>', self.move_left)
        root.bind_all('<Key-Right>', self.move_right)
        root.bind_all('<Key-Up>', self.move_up)
        return root

    def game_init(self):
        self.game_board = [[0] * 4 for _ in range(4)]
        self.init_game_board()
        self.label_grid = self.init_label_grid()
        self.update_label_grid()
        self.score = self.init_label_score()
        Button(self.window, text="Recommencer", command=self.game_init, height=3)\
            .grid(row=4, column=3, rowspan=2)

    def init_game_board(self):
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        i = random.choice(range(4))
        j = random.choice(range(4))
        while self.game_board[i][j] != 0:
            i = random.choice(range(4))
            j = random.choice(range(4))
        self.game_board[i][j] = random_tile_value()

    def init_label_grid(self):
        grid = [[(Label(self.window,
                        font=("Helvetica", 16, "bold"),
                        borderwidth=4,
                        width=3,
                        justify='center'))for _ in range(4)] for _ in range(4)]
        return grid

    def update_label_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.game_board[i][j]
                grid = self.label_grid[i][j]
                if value != 0:
                    grid.config(text=value, background=tile_color(value))
                else:
                    grid.config(text='', background=tile_color(value))
                grid.grid(row=i, column=j, padx=5, pady=5, ipadx=30, ipady=30)

    def init_label_score(self):
        score = IntVar()
        score.set(0)
        Label(self.window, font=("Helvetica", 16, "bold"),
              text='score', justify='center').grid(row=4, column=0)
        score_label = Label(self.window,
                            font=("Helvetica", 16, "bold"),
                            textvariable=score,
                            justify='center')
        score_label.grid(row=5, column=0)
        return score

    def merge(self, row):
        store = []
        result = []
        for elt in row:  # on vire les zéros
            if elt != 0:
                store.append(elt)
        store.extend([0] * (len(row) - len(store)))
        # print("sans les zéros", store)
        i = 0
        while i < len(store) - 1:
            if store[i] == store[i + 1]:
                result.append(store[i] + store[i + 1])
                score = self.score.get()
                self.score.set(score + store[i] + store[i + 1])
                i += 2
            else:
                result.append(store[i])
                i += 1
        result.append(store[-1])  # ajout du dernier élément
        result.extend([0] * (len(row) - len(result)))
        # print("fusion des doublons", result)
        return result

    def move(self):
        if self.is_game_over():
            if self.is_win():
                replay = messagebox.askyesno("Bravo", "Vous avez gagné !")
            else:
                replay = messagebox.askyesno("Echec", "Vous avez perdu !")
            if replay:
                self.game_init()
        else:
            for i in range(len(self.game_board)):
                self.game_board[i] = self.merge(self.game_board[i])
            if not self.is_full():
                self.add_new_tile()

    def move_up(self, event):
        self.transpose()
        self.move()
        self.transpose()
        self.update_label_grid()

    def move_left(self, event):
        self.move()
        self.update_label_grid()

    def move_right(self, event):
        self.mirror()
        self.move()
        self.mirror()
        self.update_label_grid()

    def move_down(self, event):
        self.anti_transpose()
        self.move()
        self.anti_transpose()
        self.update_label_grid()

    def transposed(self):
        return [list(i) for i in zip(*self.game_board)]

    def transpose(self):
        self.game_board = self.transposed()

    def mirror(self):
        store = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                store[i][j] = self.game_board[i][3 - j]
        self.game_board = store

    def anti_transpose(self):
        store = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                store[i][j] = self.game_board[3 - j][3 - i]
        self.game_board = store

    def is_full(self):
        for row in self.game_board:
            if 0 in row:
                return False
        return True

    def is_movable(self):
        for row in self.game_board:
            for i in range(3):
                if row[i] == row[i + 1]:
                    return True
        trans = self.transposed()
        for row in trans:
            for i in range(3):
                if row[i] == row[i + 1]:
                    return True
        return False

    def is_game_over(self):
        return self.is_full() and not self.is_movable()

    def is_win(self):
        return max(max(self.game_board)) >= 2048


def test():
    pass


if __name__ == '__main__':
    Grid()
