# N-Queens

Solves the classical [Eight Queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle), and has been modified to allow for *n* number of queens, and will also solve for *n* number of rooks, and *n* number of knights.

The user also has the option to select squares on the board that are blocked, i.e. a piece may not be able to be placed there.

## To Run Program

To run:

    ./a0.py piece board_size blocked_squares x1 y1 ... xn yn
    
where:
- *piece* is either "nrook", "nqueen", or "nknight".
- *board_size* is how many pieces are placed on the board
- *blocked_squares* is the number of blocked_squares
- *x1* and *y1* are option arguments, are the x,y coordinates of first blocked square, which continues all the way until xn,yn coordinates of the final blocked square.