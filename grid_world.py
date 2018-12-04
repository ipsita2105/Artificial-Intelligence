#!/usr/bin/env python

import numpy as np
import sys
import os
import re
import Queue
import math

class env:

    def __init__(self):
        self.grid = np.array([[1,1,1,1], [1,0,0,1] , [1,1,0,0], [1,1,1,0]]) # Environment grid
        # assume origin at top left corner

        self.start = np.array([3, 0])
        self.goal  = np.array([0, 3])

    def percept(self, a):
        if a.curr[0] == self.goal[0] and a.curr[1] == self.goal[1]:
            print a.curr
            return 1
        else:
            print a.curr
            return 0

class agent:

    def move(self, curr, e, d):

        direction = np.array([0,0])     # Possible movements

        if d == 0:               # Right
            direction[0] = 0
            direction[1] = 1
        
        elif d == 1:             # Left
            direction[0] = 0
            direction[1] = -1

        elif d == 2:             # Down
            direction[0] = 1
            direction[1] = 0

        elif d == 3:             # Up
            direction[0] = -1
            direction[1] = 0

        new_dir =  curr + direction
        flag = self.check_move(e, new_dir)  # Check if new point inside grid
        if flag:
            return new_dir
        else:
            return curr         # if not return current

    def check_move(self, e, curr): 
        x = curr[0]
        y = curr[1]

        # First check if inside grid
        # Dimension to be given

        s = (e.grid).shape
        dim = s[0]

        if x >= 0 and x < dim and y >= 0 and y < dim:
            if e.grid[x, y] == 1:
                return 1
        return 0


    def get_dist(self, mode, c1, c2):
            #Returns Manhattan distance
            if mode == 1:
             return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

            # Returns Euclidian distance
            return math.sqrt( ((c1[0] - c2[0])*(c1[0] - c2[0])) + ((c1[1] - c2[1])*(c1[1] - c2[1])) )

    class node(object):         # object of tree

        def __init__(self, value, parent, move, priority):
            self.value = value
            self.parent = parent
            self.move = move            # move from parent to value
            self.priority = priority

        def __cmp__(self, other):
            return cmp(self.priority, other.priority)

        def print_node(self):
            print 'Value=',self.value,'Parent=',self.parent,'Move=',self.move,'Priority=',self.priority

    def bfs(self, e, mode):

        pq = Queue.PriorityQueue()
        n_start = self.node(e.start, np.array([]), 'Start', self.get_dist(mode, e.start, e.goal))
        pq.put(n_start)
        tree = []   # Program tree
        tree.append(n_start)

        while not pq.empty():

            q = pq.get()

            if np.array_equal(q.value, e.goal):     #Percept
                self.print_path(tree, e)
                return

            for d in range(0, 4):

                cp_posn = np.copy(q.value)
                new_config = self.move(cp_posn, e, d)

                if not np.array_equal(new_config, q.value):
                 n = self.node(new_config, q.value, self.get_direction(d), self.get_dist(mode, new_config, e.goal ))
                 pq.put(n)
                 tree.append(n)

    def get_parent(self, tree, curr):

        for t in tree:
            if np.array_equal(t.value, curr):
                return t.parent

    def print_path(self, tree, e):
        
        q = Queue.LifoQueue()
        curr = e.goal

        q.put(curr)
        path_len = 0

        while not np.array_equal(curr, np.array([])):
            curr = self.get_parent(tree, curr)
            q.put(curr)

        while not q.empty():
            path_len += 1
            print q.get()

        print 'Path length =',path_len -2



    def get_direction(self, d):

        if d == 0:
            return 'Right'
        elif d == 1:
            return 'Left'
        elif d == 2:
            return 'Down'
        elif d == 3:
            return 'Up'

        return 'Invalid Direction'


def main():

    a = agent()
    e = env()
    
    print 'Enter 1 for Manhattan and 2 for Euclidian'
    m = int(input())
    a.bfs(e, m)

if __name__ == '__main__':
    main()
