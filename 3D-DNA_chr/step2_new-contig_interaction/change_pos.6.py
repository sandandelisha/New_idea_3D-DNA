import sys
import random

agp = sys.argv[1] # "/public/home/wangwen_lab/zonghang/project/Pp/05.3ddna/01.fish_ctg/FINAL_cut.agp"
merged_nodups = sys.argv[2]
p = int(sys.argv[3]) if len(sys.argv) >= 4 else int(random.random() * 1000)


index = {}
pos = {}
new_sca = {}
strand = {}

with open(agp) as f:
    for line in f:
        fields = line.strip().split('\t')
        if len(fields) < 9:
            continue
        st = (int(fields[6]) // 1000) + 1
        en = (int(fields[7]) // 1000) - 1
        for i in range(st, en+1):
            if fields[5] not in new_sca:
                new_sca[fields[5]] = {}
            new_sca[fields[5]][i] = fields[0]
            if fields[5] not in strand:
                strand[fields[5]] = {}
            strand[fields[5]][i] = fields[8]
            if fields[8] == '+':
                if fields[5] not in pos:
                    pos[fields[5]] = {}
                pos[fields[5]][i] = int(fields[1]) - int(fields[6]) + 1
            else:
                if fields[5] not in pos:
                    pos[fields[5]] = {}
                pos[fields[5]][i] = int(fields[2]) + int(fields[6]) - 1

with open(merged_nodups) as f:
    for line in f:
        fields = line.strip().split(' ')
        if not fields[1] in pos or not fields[5] in pos:
            continue
        p1 = int(int(fields[2]) / 1000)
        p2 = int(int(fields[6]) / 1000)
        if not pos[fields[1]].get(p1) or not pos[fields[5]].get(p2):
            continue
        st1 = pos[fields[1]][p1]
        st2 = pos[fields[5]][p2]
        strand1 = strand.get(fields[1]).get(p1)
        if strand1 == '+':
            fields[2] = str(int(fields[2]) + pos[fields[1]][p1])
            fields[1] = new_sca.get(fields[1]).get(p1)
        else:
            fields[2] = pos[fields[1]][p1] - int(fields[2])
            fields[1] = new_sca.get(fields[1]).get(p1)
        strand2 = strand.get(fields[5]).get(p2)
        if strand2 == '+':
            fields[6] = str(int(fields[6]) + pos[fields[5]][p2])

            fields[5] = new_sca.get(fields[5]).get(p2)
        else:
            fields[6] = pos[fields[5]][p2] - int(fields[6])
            fields[5] = new_sca.get(fields[5]).get(p2)
        print(' '.join(map(str, fields)))

