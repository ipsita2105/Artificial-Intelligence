#!/usr/bin/env python

import numpy
import pickle
import math


class vehicle:
   
    class path_info:                    # Class internal to vehicle
         def __init__(self):            # Contains info about each edge traversed
            self.start_node = 0
            self.end_node   = 0
            self.start_time = 1000000
            self.end_time   = 0.0
            self.speed      = 0.0


    def __init__(self):                 # Defines the vehicle
        self.path_list      = []
        self.curr_time      = 0.0
        self.path_index     = 0
        self.path           = []

class env:

    def __init__(self):                 # env has all info about each vehicle and the road matrix
        self.vehicle_list = []
        self.road_matrix  = []

    def all_done(self):                 # check if all vehicles have completed their path
        for v in self.vehicle_list:
            if v.path_index < 4:
                return 0
        return 1    

    def cal_speed(self,v,N):
        t = v.path_index
        speed = (math.exp((0.5)*int(N))/(1+math.exp((0.5)*int(N)))+15/(1+math.exp((0.5)*int(N))))/60.0
        (v.path_list[t]).speed = speed

    def cal_time(self,v,spt,ept):
        t = v.path_index
        d = self.road_matrix[spt,ept]
        s = (v.path_list[t]).speed

        time = d/s

        v.path_list[t].end_time = v.path_list[t].start_time + time
        v.curr_time = (v.path_list[t]).end_time

        if t < 3:
            (v.path_list[t+1]).start_time = (v.path_list[t]).end_time


    def go(self,i,spt,ept):
        v = self.vehicle_list[i]
        posn = 0
        time = float((self.vehicle_list[i]).curr_time)

        for x in range(0, len(self.vehicle_list)):
            if x != i :
                for p in (self.vehicle_list[x]).path_list:
                    if p.start_node == spt and p.end_node == ept:                       # vehicles on same path
                       if float(p.start_time) < time and float(p.end_time) > time:      # vehicles with less start time and more end time than current start time
                           posn += 1

        self.cal_speed(v,posn)
        self.cal_time(v,spt,ept)


def main():

    e  = env()
    e.road_matrix = pickle.load(open("road","r"))
    paths         = pickle.load(open("vehicle","r"))
    time          = pickle.load(open("time","r"))

    v_num = len(time)
    i = 0

    while i < v_num:                        # initializing structure for each vehicle
        v_temp           = vehicle()
        v_temp.curr_time = time[i]
        v_temp.path      = paths[i]
        (e.vehicle_list).append(v_temp)
        x = 0
        while x < 4:
            pinfo            = vehicle.path_info()
            pinfo.start_node = paths[i,x]
            pinfo.end_node   = paths[i,x+1]

            if x == 0:
                pinfo.start_time = time[i]
            ((e.vehicle_list[i]).path_list).append(pinfo)
            x = x + 1

        i = i + 1

    while not e.all_done():
     mintime = 100000
     minindex = 0

     for i in range(0,v_num):               # vehicle with least current time moves

        v = e.vehicle_list[i]
        if v.path_index < 4:
                if v.curr_time < mintime:
                    mintime  = v.curr_time
                    minindex = i

     spt = paths[minindex,(e.vehicle_list[minindex].path_index)]
     ept = paths[minindex,(e.vehicle_list[minindex].path_index + 1)]
     e.go(minindex, spt, ept)
     (e.vehicle_list[minindex]).path_index += 1
    

    for j in range(0,v_num):                # for printing
        x = 0
        v = e.vehicle_list[j]
        line = []
        while x < 4:
            l = v.path_list[x]
            #print 'from',l.start_node,'to',l.end_node,'start_time=',l.start_time/60.0,'end_time=',l.end_time/60.0,'speed=',l.speed
            line.append(float(l.start_time/60.0))
            if x == 3:
                line.append(float(l.end_time/60.0))
            x = x+ 1
        print line

if __name__ == '__main__':
    main()