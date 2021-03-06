"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # --- GOOD ----
    # if game.is_loser(player):
    #     return float("-inf")

    # if game.is_winner(player):
    #     return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # return float(my_moves - opp_moves)
    # --- GOOD ----


    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    pos = game.get_player_location(player)

    # Make sure pos tuple doesnt contain 0's or boards height or width - that means its on the permimeter
    # BAD
    if pos[0] == 0 or pos[0] == game.width-1 or pos[1] == 0 or pos[1] == game.width-1:
        # print('PAN ', my_moves - opp_moves)
        return float(my_moves - opp_moves)
    else:
        # print('PETER ', my_moves)
        return my_moves
    
    

    # implement corner heuristic!
    # rewarding opponent on corner!
    # if player == game._inactive_player
        # - .score called on min - reward corner

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # raise NotImplementedError

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    pos = game.get_player_location(player)


    if pos == (0, 0) or pos == (0, 6) or pos == (6, 6) or pos == (6, 0):
        if player == game._active_player:
            return -10
        elif player == game._inactive_player:
            return float(my_moves)
    else:
        return float((my_moves - opp_moves) ** 2)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # raise NotImplementedError

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=20.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        # best_move = (-1, -1)

        # center of board
        # if game.move_count == 0:
        #     return(int(game.height/2), int(game.width/2))

        legal_moves = game.get_legal_moves()

        # If no legal moves left
        if not len(legal_moves):
            return (-1, -1)

        # center of board
        if game.move_count == 0:
            return(int(game.height/2), int(game.width/2))

        # center of board - when i am player 2
        if game.move_count == 1 and (int(game.height/2), int(game.width/2)) in legal_moves:
            return(int(game.height/2), int(game.width/2))
        
        # Set best move to return at minimum some move
        best_move = legal_moves[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        # best_move = (-1,-1)
        # legal_moves = game.get_legal_moves()

        legal_moves = game.get_legal_moves()

        if not len(legal_moves):
            return (-1, -1)
    
        best_move = legal_moves[0]

        for m in legal_moves:
            v = self.min_value(game.forecast_move(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
        return best_move

    def terminal_test(self, gameState, depth):
        """ Return True if the game is over for the active player
        and False otherwise.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not bool(gameState.get_legal_moves()) or depth <= 0

    # If out of moves on a MIN level - Opponenet is out of moves and loses
    def min_value(self, gameState, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # If terminates on min_value it's _inactive_player / player 2's turn
        if self.terminal_test(gameState, depth):
            return self.score(gameState, gameState._inactive_player)
            # return 1

        v = float("inf")
        min_legal_moves=gameState.get_legal_moves()
        for m in min_legal_moves:
            v = min(v, self.max_value(gameState.forecast_move(m), depth - 1))
        return v

    # If out of moves on a MAX level - Computer is out of moves and loses
    def max_value(self, gameState, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # If terminates on max_value it's _active_player / player 1's turn
        if self.terminal_test(gameState, depth):
            return self.score(gameState, gameState._active_player)

        v = float("-inf")
        max_legal_moves = gameState.get_legal_moves()
        for m in max_legal_moves:
            v = max(v, self.min_value(gameState.forecast_move(m), depth - 1))
        return v


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        legal_moves = game.get_legal_moves()

        # If not legal moves left
        if not len(legal_moves):
            return (-1, -1)

        # center of board
        if game.move_count == 0:
            return(int(game.height/2), int(game.width/2))

        # center of board - when i am player 2
        if game.move_count == 1 and (int(game.height/2), int(game.width/2)) in legal_moves:
            return(int(game.height/2), int(game.width/2))
        
        # Set best move to return at minimum some move
        best_move = legal_moves[0]

        depth = 1

        try:
            # The try/except block will automatically catch the exception raised when the timer is about to expire.

            while True:
                move = self.alphabeta(game, depth)
                # print('depth --- ', depth)
                best_move = move
                depth += 1

            # return self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        best_score = float("-inf")
        # best_move = (-1,-1)

        legal_moves = game.get_legal_moves()

        if not len(legal_moves):
            return (-1, -1)
    
        best_move = legal_moves[0]

        my_dict = {}
        ww = game.width - 1
        hh = game.height - 1

        for m in legal_moves:
            
            v = self.min_value(game.forecast_move(m), depth - 1, alpha, beta)
            
            if v > best_score:
                best_score = v
                best_move = m
            alpha = max(alpha, best_score)
            # beta = min(beta, best_score)

        return best_move


    def terminal_test(self, gameState, depth):
        """ Return True if the game is over for the active player
        and False otherwise.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not bool(gameState.get_legal_moves()) or depth <= 0


    # If out of moves on a MAX level - Computer is out of moves and loses
    def max_value(self, gameState, depth, alpha, beta):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # If terminates on max_value it's _active_player / player 1's turn
        if self.terminal_test(gameState, depth):
            return self.score(gameState, self)

        v = float("-inf")
        max_legal_moves = gameState.get_legal_moves()
        for m in max_legal_moves:
            
            v = max(v, self.min_value(gameState.forecast_move(m), depth - 1, alpha, beta))

            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v


    # If out of moves on a MIN level - Opponenet is out of moves and loses
    def min_value(self, gameState, depth, alpha, beta):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # If terminates on min_value it's _inactive_player / player 2's turn
        if self.terminal_test(gameState, depth):
            return self.score(gameState, self)
            # return 1

        v = float("inf")
        min_legal_moves=gameState.get_legal_moves()
        for m in min_legal_moves:
            
            v = min(v, self.max_value(gameState.forecast_move(m), depth - 1, alpha, beta))

            if v <= alpha:
                return v
            beta = min(beta, v)

        return v


# def board_to_matrix(board):
#     r = np.zeros((board.height, board.width))
#     p1_loc = board._board_state[-1]
#     p2_loc = board._board_state[-2]

#     for i in range(board.height):
#         for j in range(board.width):
#             idx = i + j * board.height
#             if board._board_state[idx]:
#                 if idx == p1_loc:
#                     r[i,j] = 1
#                 elif idx == p2_loc:
#                     r[i,j] = 2
#                 else:
#                     r[i,j] = -1
#     return r



# ALL MY TEST CODE
# from isolation import Board
# from sample_players import RandomPlayer
# from sample_players import GreedyPlayer
# import numpy as np
# print('--- STARTING ---')

# player1 = AlphaBetaPlayer()
# player2 = GreedyPlayer()

# player1 = RandomPlayer()
# player2 = AlphaBetaPlayer()

# game = Board(player1, player2)




# m = (0, 3)

# game_matrix = board_to_matrix(game)
# game_matrix[m[0]][m[1]] = 22
# print(game_matrix)

# print('-----')

# rotate_90 = np.array(list(zip(*game_matrix[::-1])))
# rotate_180 = np.array(list(zip(*rotate_90[::-1])))
# rotate_270 = np.array(list(zip(*rotate_180[::-1])))

# print(rotate_90)

# itemindex = np.where(rotate_90==22)
# print((itemindex[0][0], itemindex[1][0]))

# print('-----')
# print(rotate_180)
# itemindex2 = np.where(rotate_180==22)
# print((itemindex2[0][0], itemindex2[1][0]))

# print('-----')
# print(rotate_270)
# itemindex3 = np.where(rotate_270==22)
# print((itemindex3[0][0], itemindex3[1][0]))




# winner, history, outcome = game.play()

# print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
# print(game.to_string())
# print("Move history:\n{!s}".format(history))
















# print(game.get_legal_moves())

# good_move = ab.get_move(game, lambda : 10.0)

# print(good_move)

# game.apply_move(good_move)

# good_move2 = mp.get_move(game, lambda : 10.0)

# print(good_move2)

# print(game.get_legal_moves())

# game.apply_move((2, 3))
# game.apply_move((2, 1))

# cc = custom_score(game, player1)

# print(cc)








# more_moves = mp.get_move(game, lambda : 10.0)

# print(more_moves)

# game.apply_move(good_move)

# ll = mp.get_move(game, lambda : 10.0)

# print(ll)








# mp.get_move(game, lambda : 10.0)



# mp.score(game, player1)

# game.apply_move((2, 3))
# game.apply_move((2, 4))

# mp.score(game, player1)









# import time
# now = time.time()
# future = now + 3

# def tim():
#     while True:
#         if now > future:
#             break