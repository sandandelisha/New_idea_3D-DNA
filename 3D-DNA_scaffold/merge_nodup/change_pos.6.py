#!/usr/bin/env python3
import sys

agp_path = sys.argv[1]
merged_nodups_path = sys.argv[2]

# 解析AGP文件，获取染色体的位置、方向等信息
new_sca = {}
strand = {}
pos = {}
with open(agp_path) as agp_file:
    for line in agp_file:
        fields = line.strip().split()
        if len(fields) < 9:
            continue
        seq_id = fields[5]
        if len(fields) < 9 or not fields[6].isdigit() or not fields[7].isdigit():
            continue
        try:
            seq_id = fields[5]
            start_idx = int(fields[6]) // 1000 + 1
            end_idx = int(fields[7]) // 1000 - 1
        except ValueError:
            continue

        
        for idx in range(start_idx, end_idx + 1):
            new_sca.setdefault(seq_id, {})[idx] = fields[0]
            strand.setdefault(seq_id, {})[idx] = fields[8]
            if fields[8] == '+':
                pos.setdefault(seq_id, {})[idx] = int(fields[1]) - int(fields[6]) + 1
            else:
                pos.setdefault(seq_id, {})[idx] = int(fields[2]) + int(fields[6]) - 1

# 处理基因组比对结果
with open(merged_nodups_path) as merged_nodups_file:
    for line in merged_nodups_file:
        fields = line.strip().split()
        if fields[1] not in pos or fields[5] not in pos:
            continue
        p1 = int(fields[2]) // 1000
        p2 = int(fields[6]) // 1000
        if p1 not in pos[fields[1]] or p2 not in pos[fields[5]]:
            continue
        st1 = pos[fields[1]][p1]
        st2 = pos[fields[5]][p2]
        if strand[fields[1]][p1] == '+':
            fields[2] = str(int(fields[2]) + st1)

            fields[1] = new_sca[fields[1]][p1]
        else:
            fields[2] = st1 - int(fields[2])
            fields[1] = new_sca[fields[1]][p1]
        if strand[fields[5]][p2] == '+':
            fields[6] = str(int(fields[6]) + st2)

            fields[5] = new_sca[fields[5]][p2]
        else:
            fields[6] = st2 - int(fields[6])
            fields[5] = new_sca[fields[5]][p2]
        print(' '.join(str(x) for x in fields))

