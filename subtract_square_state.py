from game_state import GameState
from subtract_square_move import SubtractSquareMove
from math import sqrt
from random import randint


class SubtractSquareState(GameState):
    ''' The state of a Subtract Square game

    current_total: int   --- total to be subtracted from
    '''

    def __init__(self, p, interactive=False, current_total=0):
        ''' (SubtractSquareState, int, str) -> NoneType

        Initialize SubtractSquareState self with current_total the number
        to decrease to 0.

        Assume:  0 <= current_total is an int
                        p in {'p1', 'p2'}
        '''
        if interactive:
            current_total = randint(1, int(input('Maximum starting value? ')))
        GameState.__init__(self, p)
        self.current_total = current_total
        self.over = (current_total < 1)
        self.instructions = ('On your turn, you may remove any number so long '
                             'as it is (a) a perfect square, and '
                             '(b) no more than the current number.')

    def __repr__(self):
        ''' (SubtractSquareState) -> str

        Return a string representation of SubtractSquareState self
        that evaluates to an equivalent SubtractSquareState

        >>> s = SubtractSquareState('p1', current_total = 17)
        >>> s
        SubtractSquareState('p1', False, 17)
        '''
        return 'SubtractSquareState({}, False, {})'.format(
            repr(self.next_player), repr(self.current_total))

    def __str__(self):
        ''' (SubtractSquareState) -> str

        Return a convenient string representation of SubtractSquareState (self).

        >>> s = SubtractSquareState('p1', current_total=17)
        >>> print(s)
        Current total: 17; next player: p1
        '''
        return ('Current total: {}; next player: {}'.format(
            str(self.current_total), str(self.next_player)))

    def __eq__(self, other):
        ''' (SubtractSquareState, object) -> bool

        Return True iff this SubtractSquareState is the equivalent to other.

        >>> s1 = SubtractSquareState('p1', current_total=17)
        >>> s2 = SubtractSquareState('p1', current_total=17)
        >>> s1 == s2
        True
        '''
        return (isinstance(other, SubtractSquareState) and
                self.current_total == other.current_total and
                self.next_player == other.next_player)

    def apply_move(self, move):
        ''' (SubtractSquareState, SubtractSquareMove) -> SubtractSquareState

        Return the new SubtractSquareState reached by applying move to self.

        >>> s1 = SubtractSquareState('p1', current_total=17)
        >>> s2 = s1.apply_move(SubtractSquareMove(9))
        >>> print(s2)
        Current total: 8; next player: p2
        '''
        if move in self.possible_next_moves():
            new_total = self.current_total - move.amount
            return SubtractSquareState(self.opponent(),
                                       current_total=new_total)
        else:
            return None

    def rough_outcome(self):
        '''(SubtractSquareState) -> float

        Return an estimate in interval [LOSE, WIN] of best outcome next_player
        can guarantee from state self.

        >>> SubtractSquareState('p1', current_total=0).rough_outcome()
        -1.0
        >>> SubtractSquareState('p1', current_total=1).rough_outcome()
        1.0
        >>> SubtractSquareState('p1', current_total=5).rough_outcome()
        -1.0
        >>> SubtractSquareState('p1', current_total=16).rough_outcome()
        1.0
        '''
        if is_pos_square(self.current_total):
            return SubtractSquareState.WIN
        elif all([is_pos_square(self.current_total - n**2)
                  for n in range(1, self.current_total + 1)
                  if n**2 < self.current_total]):
            return SubtractSquareState.LOSE
        else:
            return SubtractSquareState.DRAW

    def get_move(self):
        '''(SubtractSquareState) -> SubtractSquareMove

        Prompt user and return move.
        '''
        return SubtractSquareMove(int(input('Remove how much? ')))

    def winner(self, player):
        ''' (SubtractSquareState, str) -> bool

        Return True iff the game is over and player has won.

        >>> s1 = SubtractSquareState('p1', current_total=17)
        >>> s2 = s1.apply_move(SubtractSquareMove(16))  # p1's move
        >>> s3 = s2.apply_move(SubtractSquareMove(1))   # p2's move
        >>> s3.winner('p1')
        False

        Preconditions: player is either 'p1' or 'p2'
        '''
        # normal, not misere, subtract square game?
        # http://en.wikipedia.org/wiki/Subtract_a_square
        return self.current_total == 0 and self.opponent() == player

    def possible_next_moves(self):
        ''' (SubtractSquareState) -> list of SubtractSquareMove

        Return a (possibly empty) list of moves that are legal
        from the present state.

        >>> s1 = SubtractSquareState('p1', current_total=17)
        >>> L1 = s1.possible_next_moves()
        >>> L2 = [SubtractSquareMove(1), SubtractSquareMove(4), SubtractSquareMove(9), SubtractSquareMove(16)]
        >>> len(L1) == len(L2) and all([m in L2 for m in L1])
        True
        '''
        return [SubtractSquareMove(i**2)
                for i in range(self.current_total, 0, -1)
                if i*i <= self.current_total]


def is_pos_square(n):
    '''(int) -> bool

    Return whether n is a positive perfect square.

    >>> is_pos_square(5)
    False
    >>> is_pos_square(9)
    True
    '''
    from math import sqrt
    return round(sqrt(n))**2 == n and n > 0


if __name__ == '__main__':
    import doctest
    doctest.testmod()