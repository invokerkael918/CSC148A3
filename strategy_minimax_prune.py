from strategy import Strategy


class StrategyMinimaxPrune(Strategy):
    '''Interface to suggest an optimal move for the computer which the computer
    assumes the player will also make the optimal move and moves accordingly'''
    at_most = 1.0

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
            best_score, best_move = self.best_move(state)
            at_most = best_score
            print('return the best move')
            return best_move

    def best_move(self, state):
        '''
        (StrategyMinimax, SubtractSquareState or TippyState )->
        int, SubtractSquareMove or TippyMove

        This function optimizes the running time of minimax by keeping track
        of the score guaranteed to both players. For instance, if Minimax
        finds that the p1 can atleast achive a score of 0, this score is
        guaranteed to p1. This strategy abandons any further search whenever
        the score guaranteed to p2 is >= -1 times the score guaranteed to p1,
        because it would be meaningless to continue the search.

        >>>from subtract_square_state import SubtractSquareState
        >>>a=StrategyMinimaxPrune()
        >>>b=SubtractSquareState('p1',current_total=99)
        >>>a.suggest_move(b)
        return the best move
        SubtractSquareMove(4)

        >>>b=SubtractSquareState('p1',current_total=95)
        >>>a.suggest_move(b)
        return the best move
        SubtractSquareMove(81)

        '''
        if self.at_most == -1.0:
            return -1.0, state.possible_next_moves()[0]

        if self.at_most == 1.0:
            for next_move in state.possible_next_moves():
                next_state = state.apply_move(next_move)
                if next_state.over:
                    score = next_state.outcome()
                else:
                    score, move = self.best_move(next_state)
                if score == -1.0:
                    return 1.0, next_move

        for next_move in state.possible_next_moves():
            next_state = state.apply_move(next_move)
            if next_state.over:
                score = next_state.outcome()
            else:
                score, move = self.best_move(next_state)
            if score == 0.0:
                return 0.0, next_move

        return -1.0, state.possible_next_moves()[0]
