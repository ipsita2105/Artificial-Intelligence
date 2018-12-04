#!/usr/bin/env python

import sys
import re
import numpy as np
import Queue

#Parity function

def get_sum(board,i, j):

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
            sum1 = sum1 + get_sum(board, i, j)
            
    parity = (dvalue + sum1)%2
    print 'parity= ',parity


def d(board):

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
    return d

class agent:
    def move(self,copy_board, d):       # Takes the move and returns new board configuration
        board = copy_board

        n = len(board[0])
        ii=0
        jj=0


        for i in range(0, n):
            for j in range(0, n):
                if board[i, j] == n*n:
                    ii = i
                    jj = j
                    break

        if d == 1:                      # Right
            if jj+1 < n:
                board[ii, jj] = board[ii, jj+1]
                board[ii, jj+1] = n*n 
            else:
                return board


        if d == 2:                      # Left
            if jj-1 >= 0:
                board[ii, jj] = board[ii, jj-1]
                board[ii, jj-1] = n*n
            else:
                return board


        if d == 3:                      # Up
            if ii-1 >= 0:
                board[ii, jj] = board[ii-1, jj]
                board[ii-1, jj] = n*n
            else:
                return board

        if d == 4:                      # Down
            if ii+1 < n:
                board[ii, jj] = board[ii+1, jj]
                board[ii+1, jj] = n*n
            else:
                return board


        return board

class env:
    class node:

        def __intit__(self):                    # Env Tree nodes have these attributes
            self.value = numpy.array([])
            self.parent = numpy.array([])
            self.move = 'null'                  # Move from parent to this value

        def print_node(self):
            print 'Value =',self.value,'\nParent =',self.parent

    def add_to_tree(self,tree, new_config, b, direction):

        for t in tree:
            if np.array_equal(t.value, new_config):
                return
        n = self.node()
        n.value = new_config
        n.parent = b
        
        if direction == 1:
            n.move = 'Right'
        elif direction == 2:
            n.move = 'Left'
        elif direction == 3:
            n.move = 'Up'
        elif direction == 4:
            n.move = 'Down'
        else:
            n.move = 'Start'

        tree.append(n)

    def get_parent(self,node, tree):

        for t in tree:
            if np.array_equal(t.value, node):
                return t.parent

    def get_move(self,node, tree):
        
        for t in tree:
            if np.array_equal(t.value, node):
                return t.move

    def print_steps(self,tree, goal_config):    # Trace back path to root and prints after putting nodes in Lifo

        q = Queue.LifoQueue()
        curr = goal_config
        q.put(curr)
        move_queue = Queue.LifoQueue()
        move_queue.put(self.get_move(curr, tree))

        while not np.array_equal(self.get_parent(curr, tree), np.array([])):
            curr = self.get_parent(curr, tree)
            move = self.get_move(curr, tree)
            q.put(curr)
            move_queue.put(move)

        while not q.empty():
            print q.get(),'    ',move_queue.get(),'\n'


    def bfs(self,board, goal_config, a):

        q = Queue.Queue()           # Fifo Queue
        q.put(board)

        tree = []                   # tree is made out of nodes
        self.add_to_tree(tree, board, np.array([]),0)
        

        while not q.empty():
            
            b = q.get()

            if np.array_equal(b, goal_config):      # This is the percept
                 print 'Steps are-'
                 self.print_steps(tree, goal_config)
                 return
            
            for d in range(1, 5):   # directions 1, 2, 3, 4

                    copy_board = np.copy(b)
                    new_config = a.move(copy_board, d)

                    if not np.array_equal(new_config, b):   # Add if move results in new configuration
                        q.put(new_config)            
                        # Add to tree 
                        self.add_to_tree(tree, new_config, b, d)

def main():

    # Generate random board
    print 'Enter matrix (space as n^2)'
    a = input()
    board = np.array(a)
    n = len(board[0])

    # generate the goal config
    num = 1
    goal_config = []

    a = agent()
    e = env()

    for t in range(0, n):       # generate the goal config
        row_list = []
        for r in range(0, n):
            row_list.append(num)
            num += 1
        goal_config.append(row_list) 

    gc = np.array(goal_config)
    e.bfs(board, gc, a)


if __name__ == '__main__':
  main()
