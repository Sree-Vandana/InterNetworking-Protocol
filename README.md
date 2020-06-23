# InterNetworking-Protocols

A Multiplayer Game is chosen (in this case Rock-Paper-Scissors).
A [network protocol](https://github.com/Sree-Vandana/InterNetworking-Protocols/blob/master/Network-Protocol.md) is proposed that could support the game on-line, and the protocol is implemented in a Python (using PyCharm)
The Server and client have following [Specifications](https://github.com/Sree-Vandana/InterNetworking-Protocols/blob/master/Game%20Specifications.pdf)
</br>
The Game Interface is as follows
</br>
![game-interface](https://github.com/Sree-Vandana/InterNetworking-Protocols/blob/master/Game%20Pics/player_0%20and%20player_1.png)
</br>
* <p>The two player who are paired can start playing game and the score board will be updated accordingly. And at any point of time any of the player can leave the game, at that time the other playing pair will be informed and redirected to the menu screen, and can start connecting to other player and continue playing.</p>
<img src= "https://github.com/Sree-Vandana/InterNetworking-Protocols/blob/master/Game%20Pics/other-player-left.png" width="500" height="500" />

* <p>The protocol is designed to handle server and Client crashes. During the Server crash, the players will be disconnected and redirected to menu screen where they will be informed about the trouble  at server side and will be asked if they wish to stay connected and try again later or Quit the game, and based on the option selected by the palyer appropriate action will be performed.</p>
<img src= "https://github.com/Sree-Vandana/InterNetworking-Protocols/blob/master/Game%20Pics/Server-crash.png" width="500" height="500" />

