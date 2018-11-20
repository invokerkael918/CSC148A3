from move import Move


class TippyMove(Move):
    ''' A move in the game of Subtract Square.

    amount: int -- amount to subtract from current value.
    '''

    def __init__(self, position):
        ''' (TippyMove, tuple) -> NoneType

        Initialize a new TippyMove for ......

        Assume: position is a tuple.
        '''
        self.position = position

    def __repr__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove.
        >>> m1 = TippyMove((1, 1))
        >>> m1
        TippyMove((1, 1))
        '''
        return 'TippyMove({})'.format(str(self.position))

    def __str__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove
        that is suitable for users to read.

        >>> m1 = TippyMove((1, 1))
        >>> print(m1)
        Place at (1, 1)
        '''

        return 'Place at {}'.format(self.position)

    def __eq__(self, other):
        ''' (TippyMove, TippyMove) -> bool

        Return True iff this TippyMove is the same as other.

        >>> m1 = TippyMove((1, 1))
        >>> m2 = TippyMove((3, 1))
        >>> print(m1 == m2)
        False
        '''
        return (isinstance(other, TippyMove) and
                self.position == other.position)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
