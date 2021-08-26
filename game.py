class Game:
    def __init__(self, id):
        self.Turn = [True, False]
        self.ready = False #both p's conn, ready to play
        self.inProgress = False
        self.pLock = [False, False]
        self.id = id
        self.moves = [None, None]
        self.selection = [None, None]

    def play(self, player, coordinate):
        # coordinate = coords (tuple)
        # coordinate is checked client side before send
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
    
    def connected(self):
        return self.ready