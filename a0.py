#!/usr/bin/env python
# a0.py : Solve the N-Rooks, N-Queens, N-Knights problem!
# Started by D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated again for homework by Derrick Eckardt in 2018.
# Refactored in 2020.

import sys
from operator import add
import cProfile
import time

# Count # of pieces in given row
def count_on_row(board, row):
    # return sum( board[row] ) 
    return board[row].count(1) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count # of pieces in the diagonals from a particular spot on the board
def count_on_diagonals(board,row,col):
    diags = 0
    for colpos in range(col-1,-1,-1):
        rowpos = row+colpos-col
        if rowpos >= 0 and board[rowpos][colpos]==1:
            return 1 # diags += board[rowpos][colpos] 
        rowpos = row-colpos+col
        if rowpos <= N-1 and board[rowpos][colpos]==1:
            return 1 #diags += board[rowpos][colpos]
    return 0

# Count number of piece in L-shapes that could attack another knight
def count_on_els(board,row,col):
    els = 0
    # Opportunity to streamline code in future below
    rowpos = [row-2,row-1,row+1,row+2]
    colpos = [col-1,col-2,col-2,col-1]
    # els = sum([board[rowpos[x]][colpos[x]] for x in [0,1,2,3] if rowpos[x] >=0 and rowpos[x] <= N-1 and colpos[x] >=0 and colpos[x] <= N-1])
    for x in [0,1,2,3]:
        if rowpos[x] >=0 and rowpos[x] <= N-1 and colpos[x] >=0 and colpos[x] <= N-1 and board[rowpos[x]][colpos[x]] == 1:
            # els += board[rowpos[x]][colpos[x]]
            return 1
    return 0 # els

# Count total # of pieces on board
def count_pieces(board):
    return [ row.count(1) for row in board ].count(1)

# Return a string with the board rendered in a human-friendly format
def printable_board(board, ntype):
    piece_used = "R" if ntype == "nrook" else "Q" if ntype == "nqueen" else "K" if ntype == "nknight" else "?"
    return "\n".join([ " ".join([ piece_used if col==1 else "X" if col==2 else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Blocks the placement on the board at a given position, and returns a new board (doesn't change original)
def block_spot(board, row, col):
    return board[0:row] + [board[row][0:col] + [2,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board, total_pieces, ntype):
    if total_pieces < N and ntype == "nrook":
        return [add_piece(board, r, total_pieces) for r in range(0, N) if board[r][total_pieces] != 1 and count_on_row(board,r)==0 and blocked_board[r][total_pieces] != 2]
    elif total_pieces < N and ntype == "nqueen":
        return [add_piece(board, r, total_pieces) for r in range(0, N) if board[r][total_pieces] != 1 and count_on_row(board,r)==0 and count_on_diagonals(board,r,total_pieces)==0 and blocked_board[r][total_pieces] != 2]
    elif total_pieces < N and ntype == "nknight":
        return [add_piece(board, r, total_pieces) for r in range(0, N) if board[r][total_pieces] != 1 and count_on_els(board,r,total_pieces) == 0 and blocked_board[r][total_pieces] != 2]
    else:
        return[]

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Find solution board
def solve_board(initial_board, ntype):
    fringe = [(initial_board,count_pieces(initial_board))]
    # print(fringe)
    while len(fringe) > 0:
        next_board,pieces = fringe.pop()
        all_successors = successors(next_board,pieces, ntype)
        for s in all_successors:
            if pieces+1 == N:
                if is_goal(s):
                    return(s)
            fringe.append((s,pieces+1))
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

# For testing - cProfile.run("solution = solve_board(initial_board, ntype)")
solution = solve_board(initial_board, ntype)
printable_solution = list( map(add, solution[r], blocked_board[r]) for r in range(0,N) ) 
print (printable_board(printable_solution, ntype) if solution else "Sorry, no solution found. :(")