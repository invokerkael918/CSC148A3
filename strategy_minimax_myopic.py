from strategy import *


class StrategyMinimaxMyopic(Strategy):
    def suggest_move(self, state):
        '''
        (StrategyMinimax, SubtractSquareState or TippyState)->
        SubtractSquareMove or TippyMove

        suggest an optimal move from the moves avaiable.This algorithm assumes
        the opponent also makes the optimal move.
        '''
        if len(state.possible_next_moves()) == 1:
            return state.possible_next_moves()[0]
        else:
            best_score, best_move = self.best_move(state, n=3)
            print('return the best move')
            return best_move

    def best_move(self, state, n=3):
        '''
        (StrategyMinimax, SubtractSquareState or TippyState )->
        int, SubtractSquareMove or TippyMove

        This function optimizes the running time of minimax by using the
        rough_outcome function to estimate the appropriate steps to take if the
        game is not over within the next ten steps.The result produced with
        this strategy may not be as accurate as Minimax itself.

        >>>from subtract_square_state import SubtractSquareState
        >>>a=StrategyMinimaxMyopic()
        >>>b=SubtractSquareState('p1',current_total=99)
        >>>a.suggest_move(b)
        return the best move
        SubtractSquareMove(4)

        >>>b=SubtractSquareState('p1',current_total=95)
        >>>a.suggest_move(b)
        return the best move
        SubtractSquareMove(81)

        '''

        n_init = n

        for next_move in state.possible_next_moves():
            next_state = state.apply_move(next_move)
            if next_state.over:
                score = next_state.outcome()
            elif n >= 0:
                n -= 1
                score, move = self.best_move(next_state, n)
            else:
                score = next_state.rough_outcome()
            n = n_init
            if score == -1.0:
                return 1.0, next_move

        n_init = n

        for next_move in state.possible_next_moves():
            next_state = state.apply_move(next_move)
            if next_state.over:
                score = next_state.outcome()
            elif n >= 0:
                n -= 1
                score, move = self.best_move(next_state, n)
            else:
                score = next_state.rough_outcome()
            n = n_init
            if score == 0.0:
                return 0.0, next_move

        return -1.0, state.possible_next_moves()[0]
