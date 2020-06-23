# InterNetworking-Protocols

## Networked Games
A  Multiplayer Game is chosen (in this case <i>Rock-Paper-Scissors</i>).</br>
A network protocol is proposed that could support the game on-line, and the protocol is implemented in a Python (<i>using PyCharm</i>)</br>
The Server and client have following [Specifications](https://github.com/Sree-Vandana/InterNetworking-Protocols/blob/master/Game%20Specifications.pdf)
</br>
## Communication between Server and Clients

![Server-Client-Communications](https://github.com/Sree-Vandana/InterNetworking-Protocols/blob/master/Game%20Pics/Server-Client%20Communications.png)

* <p>The server is up and running and keeps listening to the clients.</br></p>
* <p>Client 1 connects to the server</br></p>
* <p>The server accepts the connection and sends the player number as a reply to the connected client.</br></p>
* <p>This client 1 waits for other player to connect to the server and start playing the game.</br></p>
    (this waiting is timed, meaning after a certain time period, say 1 minute the client will be asked if he wants to continue the wait or want to quit the game. And based on the choice he made; appropriate action is taken)</br></p>
* <p>If within the time period, another player connects to the server and starts playing, server pairs these two clients and creates a unique gaming Id for both the players and sends a game object to both the clients.</br></p>
* <p>When the game starts, the players make the moves, and send that to the server, the server updates this information in the current game (information stores with respect to current game object, this is indicated using blue dot in the above diagram).</br></p>
* <p>The players can access some part of game rules(indicated with blue dot above) and validate which of the two players won, and update the same in the score board of game window.</br></p>
* <p>The above operations continue. But when a player wishes to leave, he can leave at any time.</br></p>
* <p>Out of the two players, the player who wishes to leave, the game will be closed as well as the TCP connection.</br></p>
* <p>However, the other player if willing to continue playing, can still remain connected to the server, and start searching for another player or can leave as well.</br></p>
