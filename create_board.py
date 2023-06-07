# Cordet Gula
# CS 541 Fall 2022
# Artificial Intelligence
# Programming Assignment #3
# Tic-Tac-Toe
# create_board.py

import numpy as np


# The purpose of this file is to build a board class for tic-tac-toe

# This class create the board
class Game:

    def __init__(self):
        self.board = []  # Initialize board for game-play

    # Create blank encoded board
    def blank_board(self) -> object:
        self.board = [0 for _ in range(9)]
        return self.board

    # Create 3x3 matrix board
    def decode_board(self) -> list:
        return [self.board[i:i + 3] for i in range(0, len(self.board), 3)]

    # Update the board based on new turn
    def update_board(self, spot, player) -> object:
        self.board[spot] = player
        return self.board

    # Check if the game has ended
    def is_end(self) -> bool:
        eval_board = self.decode_board()  # Create 3x3 board to evaluate
        col_board = np.transpose(eval_board)  # Check columns by transpose
        fval = eval_board[0][0]
        bval = eval_board[0][2]
        fcount, bcount = 0, 0  # Forward and Backward diagonal count

        for i in range(len(eval_board)):
            check_row = len(set(eval_board[i]))
            check_col = len(set(col_board[i]))
            if check_row == 1 and eval_board[i][0] != 0:
                return True
            elif check_col == 1 and col_board[i][0] != 0:
                return True
            else:
                if fval == eval_board[i][i] and fval != 0:
                    fcount += 1
                    fval = eval_board[i][i]
                if bval == eval_board[i][2 - i] and bval != 0:
                    bcount += 1
                    bval = eval_board[i][2-i]
                if fcount == 3 or bcount == 3:
                    return True

        return True if self.is_draw() else False

    # Check if agent [MINT] wins
    def is_winner(self, ai) -> bool:
        eval_board = self.decode_board()  # Create 3x3 board to evaluate
        col_board = np.transpose(eval_board)  # Check columns by transpose
        fcount, bcount = 0, 0  # Forward and Backward diagonal count

        for i in range(len(eval_board)):
            check_row = len(set(eval_board[i]))
            check_col = len(set(col_board[i]))
            if check_row == 1 and eval_board[i][0] == ai:
                return True
            elif check_col == 1 and col_board[i][0] == ai:
                return True
            else:
                if eval_board[i][i] == ai:
                    fcount += 1
                if eval_board[i][2 - i] == ai:
                    bcount += 1
                if fcount == 3 or bcount == 3:
                    return True
        return False

    # Check if the board is full
    def is_draw(self) -> bool:
        return True if 0 not in self.board else False

    # Display board
    def display_board(self) -> None:
        show_board = self.decode_board()
        for row in show_board:
            for mark in row:
                if mark == 0:
                    print('-', end=" ")
                else:
                    print('X', end=" ") if mark == 1 else print('O', end=" ")
            print()
