from game_state import GameState
from tippy_move import TippyMove
from math import sqrt
from random import randint


class TippyState(GameState):
    '''
        A new game designed by inheriting the main class GameState. 
        
        grid_num:int -- The size of the grid which game Tippy will be played on.
        -grid: dict -- The dictionary which contains coordinates as the key
        and the coupons on the coordinates as value.
        
    '''
    def __init__(self, p, interactive=False, grid_num = None, _grid = None):
        
        '''
        (TippyState, str)-> NoneType
        Initialize the class TippyState with grid_num as the size of the grid
        to be played on to form a Tippy. 
        '''
        if interactive:
            start_grid_num = input('Maximum grid number which is equal or greater than 3? ')
            while not start_grid_num.isnumeric():
                start_grid_num = input('Maximum grid number which is equal or greater than 3? ')          
            grid_num = randint(3, int(start_grid_num))
            
        GameState.__init__(self, p)
        self.grid_num = grid_num
        self.instructions = ('On your turn, you may place at any position '
                             'so long as the row number and column number '
                             'not greater than the grid number.')
        self._grid = {}
        if _grid == None:
            for i in range(grid_num + 1):       
                for j in range(grid_num + 1):
                    if j == 0 :
                        self._grid[(i, j)] = i
                    elif i == 0:
                        self._grid[(i, j)] = j
                    else:
                        self._grid[(i, j)] = ' '
        else:
            self._grid = _grid

        self.over = not self.possible_next_moves()    
    
    def __repr__(self):
        ''' (TippyState) -> str

        Return a formal  representation of TippyState self.

        >>> s = TippyState('p1', grid_num=3)
        >>> s
        0   1   2   3   

        1               
        
        2               
        
        3               
        
        next player: 'p1'
        '''
        
        res = ''
        for i in range(self.grid_num + 1):
            for j in range(self.grid_num + 1):
                res += str(self._grid[(i, j)]) + '   '
            res = res + '\n' + '\n'
        return res  + 'next player: {}'.format(str(self.next_player))
        

    def __str__(self):
        ''' (TippyState) -> str

        Return a convenient and user friendly string representation of 
        TippyState self.

        >>> s = TippyState('p1', grid_num=3)
        >>> print(s)
        0   1   2   3   

        1               
        
        2               
        
        3               
        
        next player: 'p1'
        '''
        
        res = ''
        for i in range(self.grid_num + 1):
            for j in range(self.grid_num + 1):
                res += str(self._grid[(i, j)]) + '   '
            res = res + '\n' + '\n'
        return '\n' + res  + 'next player: {}'.format(str(self.next_player))
        
        
        

    def __eq__(self, other):
        ''' (TippyState, TippyState) -> bool

        Return True iff this TippyState is the equivalent to other.

        >>> s1 = TippyState('p1', grid_num=17)
        >>> s2 = TippyState('p1', grid_num=17)
        >>> s1 == s2
        True
        '''
        return (isinstance(other, TippyState) and
                self.grid_num == other.grid_num and
                self.next_player == other.next_player)

    def apply_move(self, move):
        ''' (TippyState, TippyMove) -> TippyState
        
        Return the new TippyState reached by applying move to self.

        >>> s1 = TippyState('p1', grid_num=3)
        >>> s2 = s1.apply_move(TippyMove((1, 1)))
        >>> print(s2)
        0   1   2   3   

        1   X            
        
        2               
        
        3               
        
        next player: 'p2'
        '''
        if move in self.possible_next_moves():
            next_state_grid = self._grid.copy()
            if self.next_player == 'p1':
                next_state_grid[move.position] = 'X'
            else:
                next_state_grid[move.position] = 'O'
            next_state = TippyState(self.opponent(), grid_num = self.grid_num, _grid = next_state_grid)

            return next_state
        else:
            return None
            
    def rough_outcome(self):
        '''(TippyState) -> float

        Return an estimate in interval [LOSE, WIN] of best outcome next_player
        can guarantee from state self.

        >>> s1 = TippyState('p1', grid_num=3)
        >>> s2 = s1.apply_move(TippyMove((2, 2)))
        >>> s3 = s2.apply_move(TippyMove((1, 2)))
        >>> s4 = s3.apply_move(TippyMove((2, 3)))
        >>> s5 = s4.apply_move(TippyMove((1, 3)))
        >>> s6 = s5.apply_move(TippyMove((3, 2)))
        >>> s6.rough_outcome()
        1.0
        >>> s1 = TippyState('p1', grid_num=3)
        >>> s2 = s1.apply_move(TippyMove((2, 2)))
        >>> s2.rough_outcome()
        0.0
        
        '''        
        Lx = self.currentXO('p1')
        Lo = self.currentXO('p2')

        for X in self.next_possible_value():
            Lx.append(X)
            Lo.append(X)
            if self.winner_check(Lx):
                return TippyState.WIN
            elif self.winner_check(Lo):
                return TippyState.LOSE
            Lx.remove(X)
            Lo.remove(X)
        else:
            return TippyState.DRAW
            

            
            
    def get_move(self):
        '''(TippyState) -> TippyMove

        Prompt user to make a move. Then return the as a tuple of coordinates.
        >>> s1 = TippyState('p1', grid_num=3)
        >>> s1.get_move()
        choose to place at row: 4
        choose to place at column: 3
        TippyMove((4, 3))
        '''
        i = int(input('choose to place at row: '))
        j = int(input('choose to place at column: '))
        
        return TippyMove((i, j))
    
    # helper function
    def winner_check(self, L):
        '''(TippyState, list)-> Bool
        
        A helper function to check if a Tippy is formed 
        
        >>> s1 = TippyState('p1', grid_num=3) 
        >>> s2 = s1.apply_move(TippyMove((1, 2)))
        >>> s3 = s2.apply_move(TippyMove((1, 1)))
        >>> s4 = s3.apply_move(TippyMove((2, 1)))
        >>> s5 = s4.apply_move(TippyMove((1, 3)))
        >>> s5.winner_check([1,2,3,4])
        False
        >>> s6 = s5.apply_move(TippyMove((2, 2)))
        >>> s6.winner_check([1,2,3,4,5])
        True 
        '''
        Lz = []
        for ele in L:
            if (ele + self.grid_num) in L and (ele%self.grid_num != 0 and ele%self.grid_num != 1):
                Lz.append([ele, (ele+self.grid_num)])
        for ele in Lz:
            if (((ele[0] - 1) in L) and ((ele[1] + 1) in L)) or (((ele[0] + 1) in L) and ((ele[1] - 1) in L)):
                return True
        Ls = []
        for ele in L:
                if ((ele + 1) in L) and (ele%self.grid_num != 0):
                    Ls.append([ele, (ele+1)])
        for ele in Ls:
            if (((ele[0] - self.grid_num) in L) and ((ele[1] + self.grid_num) in L)) or (((ele[0] + self.grid_num) in L) and ((ele[1] - self.grid_num) in L)):
                return True
        else:
            return False
    # helper function
    def currentXO(self,player):
        '''
        (TippyState, str) -> List of int
        Create a numerical representations of the coordinates on the grid.Then 
        store the numerical representationsin a dictionary as value, and the 
        coordinates as keys. 
        The moves each players make are stored in the dictionary with the 
        coordinates as the key and their respective numerical representation as
        value for further work to be done. 
        >>> s1 = TippyState('p1', grid_num=3)
        >>> s2 = s1.apply_move(TippyMove((2, 2)))
        >>> s3 = s2.apply_move(TippyMove((1, 3)))
        >>> s4 = s3.apply_move(TippyMove((2, 1)))
        >>> s5 = s4.apply_move(TippyMove((1, 2)))
        >>> s6 = s5.apply_move(TippyMove((3, 2)))
        >>> s7 = s6.apply_move(TippyMove((1, 1)))
        >>> s8 = s7.apply_move(TippyMove((3, 3)))
        >>> s8.currentXO('p1')
        [8, 4, 9, 5]
        >>> s2.currentXO('p1')
        [5]
        >>> s6.currentXO('p2')
        [2, 3]
        '''
        
        self.new_dic = {}
        a = 1
        for i in range(1, self.grid_num + 1):       
            for j in range(1,self.grid_num + 1):
                self.new_dic[(i, j)] = a + j - 1
            a = a + self.grid_num        
              
        Lp1 = []
        Lp2 = []
        if player == 'p1':
            for pointX in self._grid.items() :
                if pointX[1] == 'X':
                    Lp1.append(self.new_dic[pointX[0]])        
            return Lp1        
        if player == 'p2':
            for pointX in self._grid.items() :
                if pointX[1] == 'O':
                    Lp2.append(self.new_dic[pointX[0]])
            return Lp2       
    def winner(self,player):
        '''(TippyState, str)-> Bool
        
        Check if the player that made the last move has formed a Tippy to 
        win the game
        
        >>> s1 = TippyState('p1', grid_num=3)
        >>> s2 = s1.apply_move(TippyMove((2, 2)))
        >>> s3 = s2.apply_move(TippyMove((1, 3)))
        >>> s4 = s3.apply_move(TippyMove((2, 1)))
        >>> s5 = s4.apply_move(TippyMove((1, 2)))
        >>> s6 = s5.apply_move(TippyMove((3, 2)))
        >>> s7 = s6.apply_move(TippyMove((1, 1)))
        >>> s8 = s7.apply_move(TippyMove((3, 3)))
        >>> s8.winner('p1')
        True
        >>> s8.winner('p2')
        False
        '''

        if self.winner_check(self.currentXO(player)) and self.opponent() == player:
            return True            
        else:
            return False        
            

    def possible_next_moves(self):
        ''' (TippyState) -> list of TippyMove
       
        Return a (possibly empty) list of moves that are legal
        from the present state.

        >>> s1 = TippyState('p1', grid_num = 3)
        >>> L1 = s1.possible_next_moves()
        >>> L2 = [TippyMove((1, 1)), TippyMove((1, 2)), TippyMove((1, 3)), TippyMove((2, 1)),
        TippyMove((2, 2)), TippyMove((2, 3)), TippyMove((3, 1)), TippyMove((3, 2)), TippyMove((3, 3))]
        >>> len(L1) == len(L2) and all([m in L2 for m in L1])
        True
        '''
        if self.winner('p1') or self.winner('p2'):
            return []
        else:
            return [TippyMove((i, j))
                    for (i, j) in self._grid
                    if self._grid[(i, j)] == ' ']
        
    
    # helper function    
    def next_possible_value(self):
        '''(TippyState) -> List of int
        return the numerical representation of the available moves of the 
        current state
        >>> s1 = TippyState('p1', grid_num=3)
        >>> s1.next_possible_value()
        [2, 8, 9, 7, 1, 4, 3, 6, 5]
        >>> s2 = s1.apply_move(TippyMove((2, 2)))
        >>> s3 = s2.apply_move(TippyMove((1, 3)))
        >>> s4 = s3.apply_move(TippyMove((2, 1)))
        >>> s5 = s4.apply_move(TippyMove((1, 2)))
        >>> s6 = s5.apply_move(TippyMove((3, 2)))
        >>> s7 = s6.apply_move(TippyMove((1, 1)))
        >>> s8 = s7.apply_move(TippyMove((3, 3)))
        >>> s8.next_possible_value()
        [6, 7]
        '''
        
        L = []
        for point in self._grid.items():
            if point[1] == ' ':
                L.append(self.new_dic[point[0]])
        return L
        
    