#!/usr/bin/env python3

import sys

assembly = sys.argv[1]
N_size = int(sys.argv[2]) if len(sys.argv) > 2 else 500

num = assembly.split('.')[-4]

prefix = f"sc_{num}_"

size = {}
scaffold = []
index = {}

with open(assembly) as f:
    for line in f:
        line = line.strip()
        if line.startswith('>'):
            fields = line.split()
            fields[0] = fields[0][1:]
            e = fields[0].split(':')
            size.setdefault(e[0], []).append([int(fields[1]), int(fields[2])])
        else:
            scaffold.append(line)

for ctg, aa in size.items():
    pos = 1
    for i in range(len(aa)):
        end = pos + aa[i][1] - 1
        index[aa[i][0]] = [ctg, pos, end, aa[i][1]]
        pos = end + 1

for n in range(len(scaffold)):
    id = n + 1
    bb = scaffold[n].split()
    start = 1
    end = 0
    num = 0
    for i in range(len(bb)):
        if i > 0:
            end += N_size
            num += 1
            print(f"{prefix}{id}\t{start}\t{end}\t{num}\tN\t{N_size}\tscaffold\tyes\tpaired-ends")
            start = end + 1
        num += 1
        index_ = int(bb[i])
        strand = "+"
        if index_ < 0:
            strand = "-"
            index_ = abs(index_)
        cc = index[index_]
        end += cc[3]
        print(f"{prefix}{id}\t{start}\t{end}\t{num}\tW\t{cc[0]}\t{cc[1]}\t{cc[2]}\t{strand}")
        start = end + 1
