from strategy import Strategy


class StrategyMinimax(Strategy):
    '''Interface to suggest an optimal move for the computer which the computer
    assumes the player will also make the optimal move and moves accordingly'''
    def suggest_move(self, state):
        '''
        (StrategyMinimax, TippyState)-> TippyMove

        suggest an optimal move from the moves avaiable.This algorithm assumes
        the opponent also makes the optimal move.
        '''
        if len(state.possible_next_moves()) == 1:
            return state.possible_next_moves()[0]
        else:
            best_score, best_move = self.best_move(state)
            print('return the best move')
            return best_move

    def best_move(self, state):
        '''
        (StrategyMinimax, TippyState)-> int, TippyMove

        Initially check if the game can be won after selecting an
        available move. If not, assume the opponent makes an optimal move
        using Minimax strategy and check if the game can be won after
        the opponent moves. This process continues until the algorithm
        determines the player's eventual move will win the game,
        or the game cannot be won. If the game can be won,the algorithm will
        return the optimal moves to make in order to win the game. If the
        algorithm determines it is impossible for the player to win
        no matter how it moves, it then begins to check if the player
        can draw the game. It revisits the available moves again, and check
        if the game can be drawn after the next move. If not,
        assume the opponent makes an optimal move using Minimax strategy and
        check if the game can be drawn after the opponent moves. If
        the game can be drawn, the algorithm will return the optimal moves to
        draw the game. If the algorithm determines it is impossible for the
        player to win nor draw the game, it simply returns the next move
        from the available moves.
        '''
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
