"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    current_player = X
    X_cnt = sum(row.count(X) for row in board) 
    O_cnt = sum(row.count(O) for row in board)
    if X_cnt < O_cnt:
        current_player = X
    elif X_cnt > O_cnt:
        current_player = O
    
    return current_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j]==EMPTY):
                possible_actions.add((i,j))

    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    if i<0 or i>2 or j<0 or j>2:
        raise ValueError("out of bound")
    if board[i][j] != EMPTY:
        raise ValueError("is not EMPTY")
    
    new_board = copy.deepcopy(board)
    current_player = player(board)
    new_board[action[0]][action[1]] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # row horizontally
    for row in board:
        if row[0] != EMPTY and row[0]==row[1]==row[2]:
            return row[0]
    # vertically
    for col in range(3):
        if board[0][col] != EMPTY and board[0][col] == board[1][col] ==board[2][col]:
            return board[0][col]

    # diagonally
    if board[1][1]!=EMPTY and (board[0][0]==board[1][1]==board[2][2] or board[0][2]==board[1][1]==board[2][0]):
        return board[1][1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or sum(row.count(EMPTY) for row in board)==0:
        return True
    else:
        return False 

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X :
        utility_value = 1
    elif winner(board) == O:
        utility_value = -1
    else:
        utility_value = 0

    return utility_value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board)==True:
        return None
    if player(board) == X :
        optimal_value = -float('inf')
        optimal_action = None

        for action in actions(board):
            value = minimax_value(result(board,action))
            if value > optimal_value:
                optimal_value = value
                optimal_action = action
        return optimal_action
    
    elif player(board) == O :
        optimal_value = float('inf')
        optimal_action = None

        for action in actions(board):
            value = minimax_value(result(board,action))
            if value < optimal_value:
                optimal_value = value
                optimal_action = action
        return optimal_action

def minimax_value(board):
    if terminal(board):
        return utility(board)
    if player(board) ==X :
        value = -float('inf')
        for action in actions(board):
            value = max(value,minimax_value(result(board,action)))
        return value
    elif player(board) == 'O':
        value = float('inf')
        for action in actions(board):
            value = min(value,minimax_value(result(board,action)))
        return value
