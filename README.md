This is a basic chess AI using a Min-Max tree with A-B pruning. The search depth is 3 and usually completes in less than 5 seconds. The evaluation function used is the sum of the value of each remaining piece plus the distance it has moved forward multiplied by 0.25. The value is then compared to that of the opposing player. It can befound in the eval method of the ChessGame class.

The following rules have been implemented:
  - Piece movement
  - Piece taking
  - Promotion
  - Check
  - Castling
  - Checkmate

Because putting oneself in check is permitted as a
valid move in this case, stalemate conditions were 
not implemented.

The game can be played with either 1 player against
AI, or with 2 players. Moves are represented in 
algebraic notation, with each move being a pair of 
the square to move from and to. For example, to move 
the piece at A2 to A3, one would type A2 A3 or a2 a3.
If 1 player is selected, the player can choose to type 
"retire" as their move and let the AI take over for 
them (experimental). 

The board is stored as an 8x8 2D array, and each piece
is an object. A better way of storing the board and
generating moves would likely improve the efficiency
and allow a greater search depth to be reached.

-----------------------------------------------------
To run the program:

    python3 chess.py
