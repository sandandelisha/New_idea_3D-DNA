import os
import sys

# 创建 目录
output_dir = "output_files"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 创建空字典列表，用于存储 ctgID 文件中第一列的值
hash_dicts = [{} for _ in range(10)]

# 分别打开 ctgID 文件，并将其中的第一列值添加到相应的字典中
for i in range(1, 11):
    ctg_file_name = "Vmanfinal.curated.fasta.small.fa.chrlist.{}".format(i)
    with open(ctg_file_name, 'r') as ctg_file:
        for line in ctg_file:
            line = line.strip()
            if not line:
                continue
            fields = line.split()
            hash_dicts[i-1][fields[0]] = 1

# 分别打开 sort 文件，并匹配其中第二列和第六列的值是否在 ctgID 中出现过
# 如果出现过，则将该行写入相应的输出文件中
sort_file_name = sys.argv[1]
with open(sort_file_name, 'r') as sort:
    out_files = [open(os.path.join(output_dir, "merged_nodups.{}.txt".format(i)), 'w') for i in range(1, 11)]
    for line in sort:
        line = line.strip()
        fields = line.split()
        for i, hash_dict in enumerate(hash_dicts):
            if hash_dict.get(fields[1]) and hash_dict.get(fields[5]):
                out_files[i].write(line + "\n")
    for out_file in out_files:
        out_file.close()

