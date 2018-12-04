#!/usr/bin/env python
import numpy as np
import math
import sys

gamma = 0.99

#velocity range
v_min = - 0.07
v_max =   0.07

#position range
p_min = -0.6
p_max =  1.2

#number of bins in space
#same for both position and velocity
num_bins = 200

#initial condition
v_start  = 0.0
p_start  = -0.5

#left, stay, right
actions = [-1, 0, 1]

#value martix
value_matrix = np.zeros([num_bins, num_bins])
#policy matrix
policy_matrix = np.zeros([num_bins, num_bins])

#do endpoint = False
v_array = np.linspace(v_min, v_max, num = num_bins-1)
p_array = np.linspace(p_min, p_max, num = num_bins-1)


def get_v(p, v, a):
    
    v_temp = v + a*(0.001) + np.cos(3*p)*(-0.0025)

    if v_temp < v_min:
        return v_min
    
    if v_temp > v_max:
        return v_max

    else:
        return v_temp
        
def get_p(p, v):
    p_temp = p + v *(1)

    if p_temp < p_min:
        return p_min
    if p_temp > p_max:
        return p_max
    else:
        return p_temp

def reward(p):

    if p >= 0.6:
        return 1
    return -1

def U(V):

    for v in v_array:
        for p in p_array:

            v_index = np.digitize(v, v_array)
            p_index = np.digitize(p, p_array)

            temp = []
            for a in actions:

                v_next = get_v(p, v, a)
                p_next = get_p(p, v)

                v_bin = np.digitize(v_next, v_array)
                p_bin = np.digitize(p_next, p_array)

                v_temp = reward(p_next) + gamma*(value_matrix[v_bin, p_bin]) 
                temp.append(v_temp)

            max_value = temp[0]
            max_index = 0
 
            for k in range(0, len(temp)):
                if temp[k] >= max_value:
                    max_value = temp[k]
                    max_index = k

            value_matrix[v_index, p_index] = max_value
            policy_matrix[v_index, p_index] =  actions[max_index]
            

if __name__ == '__main__':

    i = 0
    while 1:
        print i
        old_value_matrix = np.copy(value_matrix)
        U(value_matrix)

        if np.array_equal(value_matrix, old_value_matrix):
           break

        i = i +1

    #.np.savetxt("value_matrix.txt", value_matrix)
    np.savetxt("policy_matrix.txt", policy_matrix, fmt="%i")
