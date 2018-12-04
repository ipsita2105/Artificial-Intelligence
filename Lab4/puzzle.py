#!/usr/bin/env python

import sys
import re
import numpy as np

class agent:
    def move(self,copy_board, d):   # Moves and return new configuration
        board = copy_board

        n = len(board[0])
        ii=0
        jj=0


        for i in range(0, n):       # Finding position of empty tile
            for j in range(0, n):
                if board[i, j] == n*n:
                    ii = i
                    jj = j
                    break

        if d == 1:                  # Right
            if jj+1 < n:
                board[ii, jj] = board[ii, jj+1]
                board[ii, jj+1] = n*n 
            else:
                return board


        if d == 2:                  # Left
            if jj-1 >= 0:
                board[ii, jj] = board[ii, jj-1]
                board[ii, jj-1] = n*n
            else:
                return board


        if d == 3:                  # Up
            if ii-1 >= 0:
                board[ii, jj] = board[ii-1, jj]
                board[ii-1, jj] = n*n
            else:
                return board

        if d == 4:                  # Down
            if ii+1 < n:
                board[ii, jj] = board[ii+1, jj]
                board[ii+1, jj] = n*n
            else:
                return board

        return board


def get_sum(board,i, j):        # Calculates the summation for given position in given board config

    summ = 0
    n = len(board[0])
    for r in range(i, n):
        for c in range(0, n):
            if r == i:
                if c > j: 
                  p_big = board[r, c]
                  if board[r, c] < board[i, j]:
                      summ += 1
                      #print 'p_big =',r,', ',c
            elif r > i: 
               p_big = board[r, c]
               if board[r, c] < board[i, j]:
                   summ += 1
                   #print 'p_big =',r,', ',c

    #print 'summ =',summ
    return summ

def get_parity(board):

    dvalue = d(board)
    sum1 = 0
    n = len(board[0])

    for i in range(0, n):
        for j in range(0, n):
            sum1 = sum1 + get_sum(board, i, j)  # Calculate sum for all positions
            
    parity = (dvalue + sum1)%2
    print 'Parity= ',parity


def d(board):                       # returns value of d for board

    n = len(board[0])
    # bottom right = n-1, n-1
    ii = 0
    jj = 0

    for i in range(0, n):
        for j in range(0, n):
            if board[i,j] == n*n:
                ii = i
                jj = j

    d = ((n-1) -ii) + ((n-1) -jj)            
    #print 'd = ',d
    return d

def main():

    print 'Enter matrix (space as n^2)'
    a = input()
    board = np.array(a)
    n = len(board[0])

    get_parity(board)

if __name__ == '__main__':
  main()
