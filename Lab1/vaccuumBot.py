#!/usr/bin/env python

import sys

class env:

	def __init__(self):
	   self.true_dirt_x = 2         # true position of dirt
	   self.true_dirt_y = 1
	   self.start_bot_x = 0         # true initial position of bot
	   self.start_bot_y = 0	   


	def get_percept(self,bo):
            bx     = bo.curr_x
            by     = bo.curr_y
            bx_int = bo.curr_x - self.start_bot_x
            by_int = bo.curr_y - self.start_bot_y

            if self.true_dirt_x == bx and self.true_dirt_y == by:
                print 'cuurent location= (',bx,',',by,') bunny state= (',bx_int,',',by_int,') Percept = True True location= (',self.start_bot_x,',',self.start_bot_y,')'
                sys.exit()

            else:
                print 'cuurent location= (',bx,',',by,') bunny state= (',bx_int,',',by_int,') Percept = False True location= (',self.start_bot_x,',',self.start_bot_y,')'


class bunny:
	
	def __init__(self):
	    self.step   = 0     # offset from initial position   
	    self.curr_x = 0     # This is the true position
	    self.curr_y = 0

	def update_state(self,env_obj,i,j):


	    self.curr_x = int(env_obj.start_bot_x) + int(i)
	    self.curr_y = int(env_obj.start_bot_y) + int(j)


def main():

	b = bunny()
	e = env()

	while 1:
	     b.step = b.step + 1
             off = b.step

             for i in range(-off,off):          # bot moves in squares of different offsets from initial position
                 for j in range(-off, off):
                     b.update_state(e,i,j)
                     e.get_percept(b)

	     	     	    
if __name__ == '__main__':
   main() 
