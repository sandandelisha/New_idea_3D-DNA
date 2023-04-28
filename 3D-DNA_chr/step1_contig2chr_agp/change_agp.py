#!/usr/bin/env python3

import sys


n = 0
with open(sys.argv[1], 'r') as agp, open(sys.argv[2], 'w') as output, open(sys.argv[3], 'w') as error:
    for line in agp:

        if line.strip() == "":
            continue

          
   
        fields = line.strip().split('\t')
        if fields[4] == 'W':
            ctg_id = 'new_ctg.{}.{}'.format(fields[0].replace('Scaffold_', ''), n)
            start = 1
            end = int(fields[7]) - int(fields[6]) + 1
            new_line = '{}\t{}\t{}\t{}\tW\t{}\t{}\t{}\t{}\n'.format(ctg_id, start, end, 1, fields[5], fields[6], fields[7], fields[8])
            output.write(new_line)
            error.write('new.contig.{}.{}\t{}\n'.format(fields[0].replace('Scaffold_', ''), n, line.strip()) + '')

            n += 1
