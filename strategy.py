class Strategy:
    '''Interface to suggest moves for a GameState.

    Must be subclassed to a concrete strategy.  Our intention is
    to provide a uniform interface for functions that suggest moves.
    '''

    def __init__(self, interactive=False):
        '''(Strategy, bool) -> NoneType

        Create new Strategy (self), prompt user if interactive.
        '''

    def suggest_move(self, state):
        '''(Strategy, GameState) -> Move

        Suggest a next move for state.
        '''
        raise NotImplementedError('Must be implemented in subclass')