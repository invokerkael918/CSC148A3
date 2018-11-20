from strategy import *


class StrategyMinimaxMemoize(Strategy):
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
            best_score, best_move = self.best_move(state, {})
            print('return the best move')
            return best_move

    def best_move(self, state, dict_state_score):
        '''
        (StrategyMinimax, SubtractSquareState or TippyState )-> int,
        SubtractSquareMove or TippyMove

        This function optimizes the running time of minimax by memorizing the
        game states and its corresponding score that minimax have previous
        visited in a dictionary. once the same state is reached, the program
        instantly returns its corresponding score from the disctionary. This
        drastically saves the amount of steps minimax takes to reach its
        objective.

        >>>from subtract_square_state import SubtractSquareState
        >>>a=StrategyMinimaxMemoize()
        >>>b=SubtractSquareState('p1',current_total=99)
        >>>a.suggest_move(b)
        return the best move
        SubtractSquareMove(4)

        >>>b=SubtractSquareState('p1',current_total=95)
        >>>a.suggest_move(b)
        return the best move
        SubtractSquareMove(81)

        '''
        for next_move in state.possible_next_moves():
            next_state = state.apply_move(next_move)

            if str(next_state) in dict_state_score.keys():
                score = dict_state_score[str(next_state)]
            elif next_state.over:
                score = next_state.outcome()
            else:
                score, move = self.best_move(next_state, dict_state_score)
            dict_state_score[str(next_state)] = score
            if score == -1.0:
                dict_state_score[str(state)] = 1.0
                return 1.0, next_move

        for next_move in state.possible_next_moves():
            next_state = state.apply_move(next_move)

            if str(next_state) in dict_state_score.keys():
                score = dict_state_score[str(next_state)]
            elif next_state.over:
                score = next_state.outcome()
            else:
                score, move = self.best_move(next_state, dict_state_score)
            dict_state_score[str(next_state)] = score
            if score == 0.0:
                dict_state_score[str(state)] = 0.0
                return 0.0, next_move

        dict_state_score[str(state)] = -1.0
        return -1.0, state.possible_next_moves()[0]
