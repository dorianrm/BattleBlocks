class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.p1Turn = False
        self.p2Turn = False
        self.ready = False #both p's conn, ready to play
        self.pLock = [False, False]
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0] #p1,p2

    def get_player_moves(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        # move = coords (tuple)
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
    
    def connected(self):
        return self.ready
    
    def bothWent(self):
        return self.p1Went and self.p2Went
    
    def winner(self):
        p1 = self.moves[0].upper()[0] #First letter of move
        p2 = self.moves[1].upper()[0]

        winner = -1 #tie

        if p1 == "R" and p2 == "P":
            winner = 1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False