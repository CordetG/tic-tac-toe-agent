# Cordet Gula
# CS 541 Fall 2022
# Artificial Intelligence
# Programming Assignment #3
# Tic-Tac-Toe
# agent.py

import numpy as np
import pickle
import random


# The purpose of this file is to develop a tic-tac-toe agent
# and a randomized baseline opponent to train from

class Player:
    MINT = 2  # Agent is 'O'
    opponent = 1  # Opponent is 'X'
    delta = 0.07  # Delta value for greedy action
    learn_rate = 0.2  # Learning rate
    discount = 0.9  # Discount value

    def __init__(self):
        self.state_field = []  # List of states
        self.q_dict = {}  # Q-Table Dictionary
        self.epsilon = 0.9  # Epsilon value for greedy action
        self.rand_prob = 0  # Choose random probability
        self.reward = 0  # Reward value

    # Encode board into "state" for q_table
    @staticmethod
    def record_state(state) -> str:
        return "".join(str(i) for i in state)

    # Generate 3^9 possible board states (only need to do this once)
    def generate_states(self, n_states) -> None:
        for s in range(n_states):
            state_list = []
            state = s
            for move in range(9):
                state_list.append(state % 3)
                state //= 3
            str_state = self.record_state(state_list)
            self.state_field.append(str_state)

    # This function Creates the initial Q-Table and saves to external file
    # This only runs once
    def init_q_table(self):
        n_states = (3 ** 9)  # 3^9 States
        q_list = np.zeros((n_states, 9), dtype=int)  # q-value list set to 0
        q_list = q_list.tolist()
        self.generate_states(n_states)

        # Map board states to actions into a dictionary
        self.q_dict = dict(map(lambda s, a: (s, a), self.state_field, q_list))
        # Set all unavailable moves to -1
        for key in self.q_dict:
            for status in range(9):
                if key[status] != '0':
                    self.q_dict[key][status] = -1

        self.save_train_data()

    # Save the q_table dictionary
    def save_train_data(self) -> None:
        pickle.dump(self.q_dict, open("q_table.p", "wb"))

    # Load the training data into q_table dictionary
    def load_train_data(self) -> None:
        self.q_dict = pickle.load(open("q_table.p", "rb"))

    # Select player positions
    def select_positions(self) -> int:
        self.MINT = random.randint(1, 2)
        self.opponent = 1 if self.MINT == 2 else 1
        return self.MINT, self.opponent

    # Switch the next turn
    def next_turn(self, player) -> int:
        return self.opponent if player == self.MINT else self.MINT

    # Human Opponent
    @staticmethod
    def human() -> int:
        move = 0
        while move < 1 or move > 9:
            move = input('Enter valid move [1-9]: ')
        return move

    # Random Baseline Opponent
    @staticmethod
    def random_agent(board) -> int:
        choices = []
        for pos in board:
            if pos == 0:
                choices.append(board.index(pos))
        move = random.choice(choices)
        return move

    # Mint decides actions using epsilon-greedy
    def mint_move(self, state, epochs) -> int:
        move = 0  # Agent Mint's Move
        r = random.uniform(0, 1)  # Random number between 0,1
        actions = self.q_dict[state]  # q-value list relative to actions
        valid_actions = []  # List of only valid actions

        # Decrease epsilon by delta every 7 epochs until 0
        if epochs % 7 == 0 and self.epsilon > self.delta:
            self.epsilon = (self.epsilon - self.delta)
        elif epochs % 7 == 0 and self.epsilon <= self.delta:
            self.epsilon = 0

        for a in actions:
            if a != -1:
                valid_actions.append(actions.index(a))

        if r > self.epsilon:
            move = actions.index(max(actions))
        elif r <= self.epsilon:
            move = random.choice(valid_actions)

        return move

    # Updates the Q-Table with new Q-value
    def update_q_value(self, curr_state, new_state, action) -> None:
        q_val = self.q_dict[curr_state][action]
        next_q_val = self.q_dict[new_state]
        q_val = q_val + self.learn_rate * (self.reward + self.discount * (max(next_q_val) - q_val))
        self.q_dict[curr_state][action] = q_val

    # Agent Mint receives a reward if game is terminated
    def receive_reward(self, agent_won, is_draw) -> None:
        if agent_won and not is_draw:
            self.reward = 1
        elif not agent_won and is_draw:
            self.reward = 0.5
        elif not agent_won and not is_draw:
            self.reward = 0
