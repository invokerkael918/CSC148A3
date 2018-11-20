class GameState:
    '''
    Snapshot of information between moves for a two-player, sequential move,
    zero-sum, perfect-information game, including the next player to move.
    In the special case that the game is over, the next player is recorded,
    but may not make a legal move.

    next_player: str    -- player about to move, unless game is over
                           in which case it is the opponent of the player
                           who just moved
    over: bool          -- flag indicating whether game is over
    instructions: str   -- description of what actions to take at each turn
    WIN: float          -- class constant indicating next player has won
    LOSE: float         -- class constant indicating next player has lost
    DRAW: float         -- class constant indicating next player tied
    '''
    # assign class constants
    WIN, LOSE, DRAW = 1.0, -1.0, 0.0

    def __init__(self, p, interactive=False):
        '''(GameState, str, bool) -> NoneType

        Construct the starting state for an occurrence of the game with
        next player p.  If interactive, prompt for input.

        prerequisite - p is in {'p1', 'p2'}
        '''
        self.next_player, self.over = p, False
        self.instructions = 'Generic instructions --- fill in with subclass'

    def opponent(self):
        '''(GameState) -> str

        Return the opponent of the next player, either 'p1' or 'p2'.

        >>> gs = GameState('p1')
        >>> gs.opponent()
        p2
        '''
        if self.next_player == 'p1':
            return 'p2'
        else:
            return 'p1'

    def get_move(self):
        '''(GameState) -> Move

        Prompt user and return a move.
        '''
        raise NotImplementedError('Implemented in a subclass')

    def apply_move(self, move):
        '''(GameState, Move) -> GameState

        Return the new game state reached by applying move to
        state self, or None if the move is illegal.
        '''
        raise NotImplementedError('Method must be implemented in a subclass')

    def winner(self, player):
        ''' (GameState, str) -> bool

        Return whether player has won the game.

        Assume: player is either 'p1' or 'p2'
                and there are no more legal moves; the game is over
        '''
        raise NotImplementedError('Method must be implemented in a subclass')

    def possible_next_moves(self):
        ''' (GameState) -> list of Move

        Return a (possibly empty) list of moves that are legal
        from the present state.
        '''
        raise NotImplementedError('Method must be implemented in a subclass')

    def outcome(self):
        ''' (GameState) -> float

        Return the outcome of this GameState for self.next_player, at the end
        of the game. The outcome is in {WIN, LOSE, DRAW}.

        self.over must be True.
        '''
        if self.winner(self.next_player):
            return GameState.WIN
        elif self.winner(self.opponent()):
            return GameState.LOSE
        else:
            return GameState.DRAW

    def rough_outcome(self):
        '''(GameState) -> float

        Return estimate of outcome based only on current state. Value
        is in interval [LOSE, WIN]
        '''
        raise NotImplementedError('Method must be implemented in a subclass')