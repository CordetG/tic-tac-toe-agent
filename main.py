# Cordet Gula
# CS 541 Fall 2022
# Artificial Intelligence
# Programming Assignment #3
# Tic-Tac-Toe
# main.py

from create_board import Game
from agent import Player
import matplotlib.pyplot as plt


def play():
    ai = Player()  # Player object
    rumble = Game()  # Game object [Let's get ready to 'rumble']
    epochs = 30  # Number of Epochs
    n_games = 10  # Number of games
    epoch_list = [0, 1, 2]  # List of epochs
    score_list = [5, 10, 15]  # List of agent scores
    opp_score_list = [1, 5, 7]  # List of opponent scores
    human = ""  # Ask if opponent is human
    is_human = False  # Check if opponent is human

    """
    ### This creates the initial Q-table, saves to external file [only runs once] ###
    run_once = Player()
    Player.init_q_table(run_once)
    """
    while human != 'y' and human != 'n':
        human = input('Is the opponent human [y or n]? ')
        if human.lower() == 'y':
            is_human = True
        elif human.lower() == 'n':
            is_human = False

    # At start of the program load Q-table
    Player.load_train_data(ai)

    plot(epoch_list, score_list, opp_score_list, is_human)


def plot(epochs, scores, opp_scores, is_human):
    opponent = 'Human' if is_human else 'Random Agent'
    plt.plot(epochs, scores, '-.', color='magenta', label='MINT [Agent]')
    plt.plot(epochs, opp_scores, '--', color='black', label='Opponent')
    plt.xlabel('Epochs')
    plt.ylabel('Score [Out of 10]')
    plt.title('Total Scores \n Delta = 0.07 Alpha = 0.2 Discount = 0.9'
              '\n Opponent: %s' % opponent)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    play()
