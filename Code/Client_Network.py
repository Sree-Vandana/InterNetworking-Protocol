import socket
import pickle

# connect to this server to start the game
class Game_Network:

    def __init__(self):
        self.server = "192.168.0.27"
        self.port = 9999
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.server, self.port))
            # get the player no. from the server
            self.player_num = self.client.recv(2048).decode()
        except:
            print("Error in ther Server side\nClosing the Game..")

    # send to server
    def send(self, data):
        #send string data to the server
        self.client.send(str.encode(data))
        #receive object data from serever
        return pickle.loads(self.client.recv(2048*4))

    def get_player_num(self):
        return self.player_num