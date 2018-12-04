#!/usr/bin/env python3

import numpy as np
import math

#For probability matrix
#########################################################
L1 = np.zeros((20, 20))
def poisson(Lambda, n):
    return ((Lambda**n)*math.exp(-Lambda))/math.factorial(n)

#calulate the req X return matrix 
for req in range(0, 20):
    for ret in range(0, 20):
        L1[req, ret] = poisson(3, req)*poisson(3, ret)

L2 = np.zeros((10, 10))
#calculate the req X return matrix
for req in range(0, 10):
    for ret in range(0, 10):
        L2[req, ret] = poisson(2, req)*poisson(1, ret)

P1 = np.zeros((20, 20))
R1 = np.zeros((20, 20))

for start in range(0, 20):
    for end in range(0, 20):

        p = 0
        r = 0
        diff = end - start
        for req in range(0, 20):
            for ret in range(0, 20):

                if (ret - req) == diff:
                    p = p + (L1[req, ret])
                    r = r + 10*(L1[req, ret])*req

        R1[start, end] = r
        P1[start, end] = p

P2 = np.zeros((10, 10))
R2 = np.zeros((10, 10))

for start in range(0, 10):
    for end in range(0, 10):

        p = 0
        r = 0
        diff = end - start
        for req in range(0, 10):
            for ret in range(0, 10):

                if (ret - req) == diff:
                    p = p + (L2[req, ret])
                    r = r + 10*(L2[req, ret])*req

        R2[start, end] = r
        P2[start, end] = p

######################################################################

#action space
#total actions = 3*(len(a1)) + 1 = 91

a1 = [[-1, 1, 0], [-1, 0, 1], 
      [-2, 2, 0], [-2, 0, 2], [-2, 1, 1],
      [-3, 2, 1], [-3, 1, 2], [-3, 3, 0], [-3, 0, 3],
      [-4, 4, 0], [-4, 0, 4], [-4, 3, 1], [-4, 1, 3], [-4, 2, 2],
      [-5, 5, 0], [-5, 0, 5], [-5, 4, 1], [-5, 1, 4], [-5, 2, 3], [-5, 3, 2],
      [2, -1, -1],
      [3, -2, -1], [3, -1, -2],
      [4, -2, -2], [4, -3, -1], [4, -1, -3],
      [5, -4, -1], [5, -1, -4], [5, -2, -3], [5, -3, -2]]
############################################################################

discount = 0.9

policy = {}

def isValid(ctemp):

    if ctemp[0] >= 0 and ctemp[0] < 20:
        if ctemp[1] >= 0 and ctemp[1] < 10:
            if ctemp[2] >= 0 and ctemp[2] < 10:
                return 1
    return 0

def U(vm):

    vnew = np.copy(vm)

    for l1 in range(0, 20):
        for l2 in range(0, 10):
            for l3 in range(0, 10):

                V = []
                cars = [l1,l2,l3]
                #print('l1=',l1,'l2=',l2,'l3=',l3)
                #locations 0, 1, 2
                for i in range(0, 3):

                    #just do all actions
                    #check if resulting states valid

                    for a in a1:
                        v_temp = 0
                        cost   = 0
                        action = ""
                        ctemp = []

                        if i == 0:
                            ctemp  = [cars[0]+a[0], cars[1]+a[1], cars[2]+a[2]]
                            action = str(a[0]) + str(a[1]) + str(a[2])
                            cost   = -2*abs(a[0])

                        if i == 1:
                            ctemp = [cars[0]+a[1], cars[1]+a[0], cars[2]+a[2]]
                            action = str(a[1]) + str(a[0]) +str(a[2])
                            cost  = -2*abs(a[1]) 

                        if i == 2:
                            ctemp  = [cars[0]+a[1], cars[1]+a[2], cars[2]+a[0]]
                            action = str(a[1]) + str(a[2]) + str(a[0])
                            cost   = -2*abs(a[1])

                        #morning
                        if isValid(ctemp):

                            #we have reached a valid intermediate state
                            #v_temp = for all [p(c_temp, a, s')*()
                            
                            v_temp = 0
                            for x1 in range(0, 20):
                                for x2 in range(0, 10):
                                    for x3 in range(0, 10):
                                        reward = cost + R1[ctemp[0], x1] + R2[ctemp[1], x2] + R2[ctemp[2], x3]
                                        v_temp = v_temp + (P1[ctemp[0], x1]*P2[ctemp[1], x2]*P2[ctemp[2], x3])*(reward + discount*vm[x1, x2, x3])
                        
                            V.append([v_temp, action])

                #for action [0,0,0]
                v_temp = 0
                for x1 in range(0, 20):
                    for x2 in range(0, 10):
                        for x3 in range(0, 10):
                            reward = R1[l1, x1] + R2[l2, x2] + R2[l3, x3]
                            v_temp = v_temp + (P1[l1, x1]*P2[l2, x2]*P2[l3, x3])*(reward + discount*vm[x1, x2, x3])

                V.append([v_temp, '000'])

                #print('V=\n',V)
                if len(V) > 0:
                    max_value = V[0][0]
                    max_index = 0

                    for j in range(0, len(V)):
                        if V[j][0] > max_value:
                            max_value = V[j][0]
                            max_index = j
                    
                    vnew[l1, l2, l3] = max_value
                    policy[l1, l2, l3] = V[max_index][1]
    return vnew

if __name__ == "__main__":
    
    value_matrix = np.zeros([20, 10, 10])

    i = 0
    #while 1:
    for k in range(0, 5):
        print('i=',i)
        i = i + 1
        old_vm = np.copy(value_matrix)
        value_matrix = U(value_matrix)

        if np.array_equal(old_vm, value_matrix):
            break                            
    '''
    #print value matrix
    for i in range(0, 20):
        print('i=', i)
        for j in range(0, 10):
            for k in range(0, 10):
                print(round(value_matrix[i][j][k], 3), end=" ")
        print('\n')
    '''
    #print policy matrix
    for i in range(0, 20):
        print('i=',i)
        for j in range(0, 10):
            for k in range(0, 10):
                if (i, j, k) in policy.keys():
                    print(policy[i, j,  k], end=" ")
                else:
                    print('000', end=" ")
        print('\n')