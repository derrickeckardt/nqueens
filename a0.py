#!/usr/bin/env python
# a0.py : Solve the N-Rooks, N-Queens, N-Knights problem!
# Started by D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated again for homework by Derrick Eckardt in 2018.

import sys
from operator import add
import cProfile

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 
    
# Count # of pieces in the diagonals from a particular spot on the board
def count_on_diagonals(board,row,col):
    diags = 0
    # Opportunity to streamline code in future below
    for colpos in range(col-1,-1,-1):
        for rowpos in range(row+colpos-col,row+colpos-col-1,-1):
            if rowpos >= 0 and board[rowpos][colpos]==1:
                diags += board[rowpos][colpos] 
        for rowpos in range(row-colpos+col,row-colpos+col+1):
            if rowpos <= N-1 and board[rowpos][colpos]==1:
                diags += board[rowpos][colpos]
    return diags

# Count number of piece in L-shapes that could attack another knight
def count_on_els(board,row,col):
    els = 0
    # Opportunity to streamline code in future below
    rowpos = [row-2,row-1,row+1,row+2]
    colpos = [col-1,col-2,col-2,col-1]
    els = sum([board[rowpos[x]][colpos[x]] for x in range(0,4) if rowpos[x] >=0 and rowpos[x] <= N-1 and colpos[x] >=0 and colpos[x] <= N-1])
    return els

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_rooks_board(board):
    return "\n".join([ " ".join([ "R" if col==1 else "X" if col==2 else "_" for col in row ]) for row in board])

def printable_queens_board(board):
    return "\n".join([ " ".join([ "Q" if col==1 else "X" if col==2 else "_" for col in row ]) for row in board])

def printable_knights_board(board):
    return "\n".join([ " ".join([ "K" if col==1 else "X" if col==2 else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Blocks the placement on the board at a given position, and returns a new board (doesn't change original)
def block_spot(board, row, col):
    return board[0:row] + [board[row][0:col] + [2,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
# NRooks Successor
def successors4(board):
    total_pieces = count_pieces(board)
    if total_pieces < N:
        return [add_piece(board, r, total_pieces) for r in range(0, N) if board[r][total_pieces] != 1 and count_on_row(board,r)==0 and blocked_board[r][total_pieces] != 2]
    else:
        return[]
# NQueens Successor
def successors5(board):
    total_pieces = count_pieces(board)
    if total_pieces < N:
        return [add_piece(board, r, total_pieces) for r in range(0, N) if board[r][total_pieces] != 1 and count_on_row(board,r)==0 and count_on_diagonals(board,r,total_pieces)==0 and blocked_board[r][total_pieces] != 2]
    else:
        return[]

# NKnights Successor
def successors6(board):
    total_pieces = count_pieces(board)
    if total_pieces < N:
        return [add_piece(board, r, total_pieces) for r in range(0, N) if board[r][total_pieces] != 1 and count_on_els(board,r,total_pieces) == 0 and blocked_board[r][total_pieces] != 2]
    else:
        return[]

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve_rooks(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors4( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# Solve n-queens!
def solve_queens(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors5( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# Solve n-knights!
def solve_knights(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors6( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# This will tell us whether to run nrook or nqueen or nknight.   It is passed through command line arguments
ntype = str(sys.argv[1]) 

# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[2])

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.  A 2 will indicate a blocked piece
initial_board = [[0]*N]*N

# Initialize a mirror blocked board.  This way it doesn't mess with counting functions used elsewhere.
blocked_board = [[0]*N]*N

# This will find the slots that cannot be utilized, and place a 2 in them.
total_blocked = int(sys.argv[3])
if total_blocked > 0:
    for blocked in range(4,4+2*total_blocked,2):
        blockedrow = int(sys.argv[blocked]) - 1
        blockedcol = int(sys.argv[blocked+1]) -1
        blocked_board = block_spot(blocked_board,blockedrow,blockedcol)

if ntype == "nrook":
    solution = solve_rooks(initial_board)
    # zip solution and blocked board into one for display
    printable_solution = list( map(add, solution[r], blocked_board[r]) for r in range(0,N) ) 
    # Note: I learned how to add elements together from
    # https://stackoverflow.com/questions/18713321/element-wise-addition-of-2-lists/18713494
    # then I built on it since I needed to do list of list of addition
    print (printable_rooks_board(printable_solution) if solution else "Sorry, no solution found. :(")
    
elif ntype == "nqueen":
    cProfile.run("solution = solve_queens(initial_board)")
    printable_solution = list( map(add, solution[r], blocked_board[r]) for r in range(0,N) ) 
    print (printable_queens_board(printable_solution) if solution else "Sorry, no solution found. :(")
    
elif ntype == "nknight":
    solution = solve_knights(initial_board)
    printable_solution = list( map(add, solution[r], blocked_board[r]) for r in range(0,N) ) 
    print (printable_knights_board(printable_solution) if solution else "Sorry, no solution found. :(")