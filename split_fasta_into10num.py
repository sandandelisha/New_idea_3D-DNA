#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys

size_file = sys.argv[1]


size = []
with open(size_file) as f:
    for line in f:
        line = line.strip().split()
        size.append([line[0], int(line[1])])


part = {}
length = {i: 1 for i in range(1, 11)}


for i in range(len(size)):
    
    len_ = [[j, length[j]] for j in range(1, 11)]
    len_.sort(key=lambda x: x[1])   
    part[len_[0][0]] = part.get(len_[0][0], []) + [size[i]]
    length[len_[0][0]] += size[i][1]


for j in range(1, 11):
    with open(size_file + '.' + str(j), 'w') as f:
        for ctg in part.get(j, []):
           f.write('{}\t{}\n'.format(ctg[0], ctg[1]))


