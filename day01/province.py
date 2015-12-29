#!/usr/bin/env python
with open('china.txt','r') as f:
    for line in f.readlines():
        new_line = line.strip().split()
        print(new_line)
        input()
