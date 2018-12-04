#!/usr/bin/env python

import numpy as np

overs = 50

V = np.zeros([overs*6 +1, 11])   # balls X wicket
R = np.zeros([overs*6 +1, 11])   # stores policy 


def pw(r, x):

    pwmin = {1:0.01, 2:0.02, 3:0.03, 4:0.1, 6:0.3}
    pwmax = {1:0.1, 2:0.2, 3:0.3, 4:0.5, 6:0.7}

    pw = pwmax[r] + (pwmin[r] - pwmax[r])*((x-1)/9.0)
    return pw

def pr(x):

    prmin = 0.5
    prmax = 0.8

    pr = prmin + (prmax -prmin)*((x-1)/9.0)
    return pr

def U(b, x):

    runs = [1, 2, 3, 4, 6]
    temp = {}

    for i in runs:
        vs = (1 -pw(i, x))*(pr(x)*i + V[b-1, x]) + pw(i, x)*(0 + V[b-1, x-1])
        temp[i] = vs

    max_i = 0
    max_value = 0

    for r in runs:
        if temp[r] > max_value:
            max_value = temp[r]
            max_i = r
    
    R[b, x] = max_i
    V[b, x] = max_value


def main():

    balls = overs*6         # total balls
    b = 1                   # balls left

    while b <= balls:

        for w in range(1, 11):  #update for each pair
            U(b, w)

        b += 1

    np.savetxt("value.txt", V, fmt="%i")
    np.savetxt("policy.txt",R,fmt="%i")


if __name__ == '__main__':
    main()