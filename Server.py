"""
Server hosts the game at IP address: 192.168.0.27 and Port Number: 9999
"""
import socket
import _thread
import pickle
from Rock_Paper_Scissors import Rock_Paper_Scissors

# Server Details
server = "192.168.0.27"
port = 9999

# Setting up the Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()
print("Server Started.\nWaiting for a connection...")

class Server:

    def __init__(self):
        # current players count connected to server
        self.player_count = 0
        # dictionary game stores game object as value accessed with key = game_id (0,1,2,..)
        self.games_dict = {}

    # client thread that sends and receives messages.
    def player_thread(self,connection, player_num, gameId):   # player = 0 or 1
        # update player_count and games_dict when players leave

        # send the player number to client
        connection.send(str.encode(str(player_num)))
        """
            From client to server
            get --> client requests for game and server sends it (respective game object)
            reset --> reset from client ;
            move --> R; P; S
        """
        while True:
            try:
                data = connection.recv(4096).decode()
                # every time loop runs; check if the gameId is valid or not (break condi 1)
                if gameId in self.games_dict:
                    current_game = self.games_dict[gameId]

                    if not data: #(break condi 2)
                        break
                    else:
                        if data == "reset":
                            current_game.reset_game()
                        elif data != "get":
                            current_game.update_player_moves(player_num, data)

                        connection.sendall(pickle.dumps(current_game))
                # if no game then break the infinite loop
                else:
                    break
            except:
                break

        print("Lost connection ")
        # if player leaves delete the game
        try:
            Id = self.games_dict[gameId]
            del self.games_dict[gameId]
            print("Closing Game", gameId, "with game_object: ", Id)
        except:
            pass
        self.player_count -= 1
        connection.close()

    def main(self):
        # Run server all the time
        while True:
            # server accepts the players request
            connection, player_ip_address = s.accept()
            print("Connected to:",connection)

            # add players to player_count and creates a new games with unique gameId (if their is no exsisting player already)
            # for every 2 people connected to game increment gameid by1 (00,11,22,..)
            player_num = 0
            self.player_count += 1
            gameId = (self.player_count - 1) // 2

            # for the 1st palyer (player 0) ctreate new game
            if self.player_count % 2 == 1:
                self.games_dict[gameId] = Rock_Paper_Scissors(gameId)
                print("For Player 0\nCreating a new game...")

            # add second player(player 1) adds to the existing game id
            else:
                player_num = 1
                self.games_dict[gameId].connected_to_game = True

            # start the thread for each client providing the gamming interface
            _thread.start_new_thread(self.player_thread, (connection, player_num, gameId))

Server = Server()
Server.main()
