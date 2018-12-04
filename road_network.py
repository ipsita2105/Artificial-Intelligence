#!/usr/bin/env python

import numpy as np
import sys
import os
import re
import Queue
import math

class env:

    def __init__(self):
        self.road_network   = [{1:1, 4:2.5},                # Road Map adjacency list
                               {0:1, 5:6},
                               {3:10, 5:4},
                               {2:10, 8:2},
                               {0:2.5, 10:2.5},
                               {1:6, 2:4, 6:6, 11:10},
                               {5:6, 7:7},
                               {6:6, 8:4},
                               {3:2, 7:4, 9:11, 12:12},
                               {8:11, 13:1},
                               {4:2.5, 11:6, 14:3, 15:2.5},
                               {10:6, 5:10, 12:15, 16:20},
                               {8:12, 11:15, 13:2.5, 16:5},
                               {9:1, 12:2.5},
                               {10:3, 15:3},
                               {10:2.5, 14:3, 16:10},
                               {11:20, 12:5, 15:10}]
                                      
        self.start      = 0     # start node
        self.goal       = 13    # goal node

    def percept(self, p):
        if p == self.goal:
          return 1
        return 0


class agent:

    def __init__(self):
        self.heuristic = np.array([6.32, 5.38, 4.47, 2.24, 6.08, 5.10, 3.16, 2.24, 1.41, 6, 3, 1, 0, 1, 6.08, 3.16, 1.41])    # h(n)
        self.cong = 100     # congestion

    class qe(object):
        def __init__(self, parent, nid, time, mode, budget):    # each node in queue
            self.nid = nid
            self.time = time
            self.mode = mode
            self.budget = budget
            self.parent = parent


        def __cmp__(self, other):                               # cmp function for priority
            return cmp(self.time, other.time)

        def print_qe(self):
            print 'Id=',self.nid,'mode=',self.mode

        def __eq__(self, other):                                # overriding equivalence function for this class    
            if   self.nid == other.nid and self.time == other.time and  self.mode == other.mode and self.budget == other.budget:
                return 1
            return 0
        
        def __ne__(self, other):                                # overriding non equal function
            if   self.nid == other.nid and self.time == other.time and  self.mode == other.mode and self.budget == other.budget:
                return 0
            return 1
        


    def a_star(self, e, budget, cost):

        pq = Queue.PriorityQueue()

        q1 = self.qe(-1, e.start, 0, 'none', budget)
        pq.put(q1)

        parent = {}           # keeps most efficient parent 

        visited = []          # keep track of visited nodes
        visited.append(0)
        for i in range(1, 17):
            visited.append(0)

        busSpeed = 0            # define busSpeed according to congestion
        if self.cong == 0:
            busSpeed = 50.00
        elif self.cong == 50:
            busSpeed = 37.50
        else:
            busSpeed = 10.00

        cycleSpeed = 25.00      # Fixed cycle speed

        while not pq.empty():
            node = pq.get()
            #print 'DEQUEUED: Id=',node.nid,'time=',node.time,'budget=',node.budget

            if e.percept(node.nid) == 1:        # check if goal reached
                #print parent
                self.printpath(node, parent)
                return

           
            visited[node.nid] = 1           # mark as visited
            #for adjacent nodes
            for k in (e.road_network[node.nid]).keys():
                    if not visited[k]:
                        if  e.road_network[node.nid][k] > 3:            # try bus if road > 3
                            # Add for bus
                            busTime = e.road_network[node.nid][k]/busSpeed
                            busCost = (busTime)*cost
                            left = node.budget - busCost

                            if left > 0:                                # can take bus if budget left
                                qadj = self.qe(node.nid, k, node.time + busTime, 'Bus',left)
                                pq.put(qadj)
                                parent[qadj] = node
                                #print 'ENQUEUED: Id=',qadj.nid,'time=',qadj.time,'budget=',qadj.budget,'mode=',qadj.mode
            
                        # for cycle
                        qadj = self.qe(node.nid, k, node.time + (e.road_network[node.nid][k]/cycleSpeed), 'Cycle',node.budget)
                        pq.put(qadj)
                        #print 'ENQUEUED: Id=',qadj.nid,'time=',qadj.time,'budget=',qadj.budget,'mode=',qadj.mode
                        parent[qadj] = node

    def printpath(self, curr, parent):

        s = "Node "+str(curr.nid)+" Budget= "+str(curr.budget)+" Time= "+str(curr.time)+"Mode= "+str(curr.mode)
        stack = Queue.LifoQueue()
        stack.put(s)

        while curr in parent.keys():
            curr = parent[curr]
            s = "Node "+str(curr.nid)+" Budget= "+str(curr.budget)+" Time= "+str(curr.time)+" Mode= "+str(curr.mode)
            stack.put(s)

        while not stack.empty():
            print stack.get()


    def get_dist(self, c1, c2):
            # Returns Euclidian distance
            return math.sqrt( ((c1[0] - c2[0])*(c1[0] - c2[0])) + ((c1[1] - c2[1])*(c1[1] - c2[1])) )


def main():

    print 'Enter % congestion on road (100 or 50 or 0)'
    c = int(input())

    print 'Enter total budget'
    budget = int(input())

    print 'Enter bus cost (per hour)'
    cost = int(input())

    e = env()
    a = agent()
    a.cong = c
    a.a_star(e, budget, cost)

if __name__ == '__main__':
    main()