#!/usr/bin/env python

import sys

def main():

    f = sys.stdin
    c = f.read(1)
    word = 1
    
    # read any space in begining
    if c == " ":
        while c == " ":
            c = f.read(1)

    while c != "":

        if c == " ":
            while c == " ":     # skip multiple spaces between words
                c = f.read(1)
            word = word + 1

        elif c == '\n':
            while c == '\n':    # skip multiple new lines
                c = f.read(1)
            word = word + 1

        c = f.read(1)    
   
    print 'words =',word-1 # -1 for last new line read

if __name__ == '__main__':
    main()

