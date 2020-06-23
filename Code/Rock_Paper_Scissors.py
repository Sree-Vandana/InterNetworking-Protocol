"""
Game Class holds all rules of the game
"""
class Rock_Paper_Scissors:
    def __init__(self, id):
        self.id = id
        self.player_1_Went = False
        self.player_2_Went = False
        self.connected_to_game = False
        self.moves = [None, None]
        self.ng = 0

    # check if players are connected to game or not--> if not show waiting in onthe players screen
    def connected(self):
        return self.connected_to_game

    # update moves list with that players move
    def update_player_moves(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.player_1_Went = True
        else:
            self.player_2_Went = True

    def get_player_move(self, p):
        return self.moves[p]

    # tells if both players went or not
    def both_players_Went(self):
        return self.player_1_Went and self.player_2_Went

    # if both players made their moves; check thir moves against one another and see who won (Game Rules)
    def winner(self):

        # get the 1st charecter of the string R/P/S (of the move; from moves)
        player1_move = self.moves[0].upper()[0]
        player2_move = self.moves[1].upper()[0]
        Rock = "R"
        Paper = "P"
        Scissors = "S"
        New_Game = "N"
        winner = -1

        if player1_move == Rock and player2_move == Scissors:
            winner = 0
        elif player1_move == Scissors and player2_move == Rock:
            winner = 1
        elif player1_move == Paper and player2_move == Rock:
            winner = 0
        elif player1_move == Rock and player2_move == Paper:
            winner = 1
        elif player1_move == Scissors and player2_move == Paper:
            winner = 0
        elif player1_move == Paper and player2_move == Scissors:
            winner = 1
        elif player1_move == "N" and player2_move == "N":
            winner = 2
        elif player1_move == New_Game and player2_move in (Rock, Paper, Scissors):
            winner = 3
        elif player2_move == New_Game and player1_move in (Rock, Paper, Scissors):
            winner = 3

        return winner

    def reset_game(self):
        self.player_1_Went = False
        self.player_2_Went = False