from move import Move


class SubtractSquareMove(Move):
    ''' A move in the game of Subtract Square.

    amount: int -- amount to subtract from current value.
    '''

    def __init__(self, amount):
        ''' (SubtractSquareMove, int) -> NoneType

        Initialize a new SubtractSquareMove for removing amount from value.

        Assume: amount is a positive integer square.
        '''
        self.amount = amount

    def __repr__(self):
        ''' (SubtractSquareMove) -> str

        Return a string representation of this SubtractSquareMove.
        >>> m1 = SubtractSquareMove(4)
        >>> m1
        SubtractSquareMove(4)
        '''
        return 'SubtractSquareMove({})'.format(str(self.amount))

    def __str__(self):
        ''' (SubtractSquareMove) -> str

        Return a string representation of this SubtractSquareMove
        that is suitable for users to read.

        >>> m1 = SubtractSquareMove(4)
        >>> print(m1)
        Remove 4
        '''

        return 'Remove {}'.format(str(self.amount))

    def __eq__(self, other):
        ''' (SubtractSquareMove, SubtractSquareMove) -> bool

        Return True iff this SubtractSquareMove is the same as other.

        >>> m1 = SubtractSquareMove(4)
        >>> m2 = SubtractSquareMove(3)
        >>> print(m1 == m2)
        False
        '''
        return (isinstance(other, SubtractSquareMove) and 
                self.amount == other.amount)


if __name__ == '__main__':
    import doctest
    doctest.testmod()