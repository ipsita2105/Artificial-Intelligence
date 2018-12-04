#!/usr/bin/env python

import sys

class env:

	def __init__(self):
	   self.true_land  = 9      # true position of shore
	   self.true_bunny = 12	    # true initial position of bunny


	def get_percept(self, bunny_obj):

	   if int(self.true_land) == int(int(self.true_bunny)+ int(bunny_obj.curr)):
		print 'Current location=', int(int(self.true_bunny)+ int(bunny_obj.curr)),'Bunny state =',bunny_obj.curr,'Percept = True Action=',bunny_obj.direction,'True location =',int(self.true_bunny)
		sys.exit()
		return 1	

	   else:
		print 'Current location=', int(int(self.true_bunny)+ int(bunny_obj.curr)),'Bunny state =',bunny_obj.curr,'Percept = False Action=',bunny_obj.direction,'True location =',int(self.true_bunny)
		return 0

class bunny:
	
	def __init__(self):
	    self.step      = 0   # offset from 0 
	    self.direction = 1   # left or right
	    self.curr      = 0   # internal state of bunny

	def update_state(self,env_obj):

	    self.curr = (self.step)*(self.direction) 


def main():

	b = bunny()
	e = env()

	while 1:
	     b.step = b.step + 1

	     b.direction = 1        # go offset times right
	     b.update_state(e)
	     e.get_percept(b) 
	     	    
	     b.direction = -1       # go offset times left
	     b.update_state(e)
	     e.get_percept(b) 

	     	     	    
if __name__ == '__main__':
   main() 













	     
