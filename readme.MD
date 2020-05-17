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


## Defining the Problem Space

The **set of valid states** is all the chess boards that have between 0 and N pieces.

Our **successor function** is adding one additional piece to the board compared to the previous board.

The **cost function** is the number of moves, which in this case, is irrelevant. Every move costs the same.

Our **goal state** is defined as an NxN board, which has N pieces on it, where no piece is in danger from another piece of being eaten.

The **Initial state** is an empty board that is N x N chessboard, where N is provided by the user at runtime.

## Breadth First Search vs. Depth First Search

Things started to get interesting at this point. I modified the code by changing line 49 by adding a zero to the pop() method:

for s in successors( fringe.pop(0))

This changed how the code goes through the fringe, by switching from DFS to BFS. pop() with no index, takes the last element first (Last In First Out – LIFO). By putting an index of 0, and calling pop(0), we are taking the first element. This converts us from a stack (DFS) to a queue (BFS) that is now First in First Out (FIFO).

## Using Collections or Lists - A Pythonic Choice

In reading the python documentation on [Data Structures](https://docs.python.org/2/tutorial/datastructures.html), I noticed something interesting about the .pop() method. The documentation states that using lists as queues is highly inefficient, since it causes every other has to be shifted over. It recommends using collections.deque and the .popleft() method to implement a queue. I added the following to my code at the beginning:

## Describe Successor Functions

## Blocking Pieces

To block a piece from being used, the user enters those on the command line, in terms of x,y coordinates.  Then, the program creates a blank board for just blocks.  The blocked squares are then added to this board.  Then, when a new piece is considered, this blocked board is consulated to determine if that square has been deemed off-limits.