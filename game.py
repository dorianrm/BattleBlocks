class Game:
    def __init__(self, id):
        self.ready = False #both p's conn, ready to play
        self.Turn = [True, False]
        self.inProgress = False
        self.pLock = [False, False]
        self.id = id
        self.moves = [None, None]
        self.shotStatus = [None, None] #Bool: True=Hit False=Miss
        self.coords = [None, None]

    def play(self, player, coordinate):
        # coordinate = coords (tuple)
        # coordinate is checked client side before send
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
    
    def connected(self):
        return self.ready