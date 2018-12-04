#!/usr/bin/env python

import numpy as np
import sys
import os
import re

class env:

    def __init__(self):
        self.grid = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                             [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                             [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                             [1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
                             [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                             [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                             [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
                             [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

        # assume origin at top left corner

        self.start = np.array([2, 0])
        self.goal  = np.array([6, 8])

    def percept(self, a):
        if a.curr[0] == self.goal[0] and a.curr[1] == self.goal[1]:
            print a.curr
            return 1
        else:
            print a.curr
            return 0

class agent:

    def __init__(self):

        self.curr = np.array([2, 0])    # Hardcoded 
        self.dir  = 0       

    def update_state(self):

        direction = np.array([0,0])

        if self.dir == 0:               # Right
            direction[0] = 0
            direction[1] = 1
        
        elif self.dir == 1:             # Left
            direction[0] = 0
            direction[1] = -1

        elif self.dir == 2:             # Down
            direction[0] = 1
            direction[1] = 0

        elif self.dir == 3:             # Up
            direction[0] = -1
            direction[1] = 0

        self.curr = self.curr + direction

    def check_move(self,e):
        
        x = int(self.curr[0])
        y = int(self.curr[1])

        # First check if inside grid
        if x >= 0 and x < 10 and y >= 0 and y < 10:
            if e.grid[x, y] == 1:
                return 1
        return 0
    
    def move(self,d,e):
        self.dir = d
        prev_state = self.curr
        self.update_state()
        check = self.check_move(e)
        if check == 0:
            self.curr = prev_state
            return 0
        return 1


def main():

    a = agent()
    e = env()

    while not e.percept(a):
        d = np.random.randint(4)
        move = a.move(d,e)


if __name__ == '__main__':
    main()
