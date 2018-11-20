import random

from strategy import Strategy


class StrategyRandom(Strategy):
    ''' Interface to suggest random moves.
    '''

    def suggest_move(self, state):
        '''(StrategyRandom, GameState) -> Move

        Return a random move from those available for state.

        Overrides Strategy.suggest_move
        '''
        return random.choice(state.possible_next_moves())