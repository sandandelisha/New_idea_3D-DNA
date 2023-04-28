import os
import re

# 定义输入文件和输出文件夹的路径
input_file = "Vmanfinal.curated.fasta.small.fa"
chr_list_files = ["Vmanfinal.curated.fasta.small.fa.chrlist.{}".format(i) for i in range(1, 11)]
output_dir = "split_files"

# 如果输出文件夹不存在，则创建该文件夹
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# 读取染色体长度信息并存储到十个字典中
chr_lengths1, chr_lengths2, chr_lengths3, chr_lengths4, chr_lengths5, \
chr_lengths6, chr_lengths7, chr_lengths8, chr_lengths9, chr_lengths10 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
chr_length_dict_list = [chr_lengths1, chr_lengths2, chr_lengths3, chr_lengths4, chr_lengths5,
                        chr_lengths6, chr_lengths7, chr_lengths8, chr_lengths9, chr_lengths10]
for i in range(len(chr_list_files)):
    with open(chr_list_files[i]) as f:
        for line in f:
            line = line.strip()
            if line:
                chr_name, chr_len = re.split(r'\s+', line)
                chr_length_dict_list[i][chr_name] = int(chr_len)

# 定义要生成的文件数量
num_files = 10

# 打开输出文件并进行初始化
output_files = []
for file_num in range(num_files):
    output_filename = os.path.join(output_dir, "Vmanfinal.curated.fasta.small.{}.fa".format(file_num + 1))
    output_file = open(output_filename, "w")
    output_files.append(output_file)

current_file_index = -1
current_file_length = 0

# 逐行读取输入文件，并将序列写入到相应的输出文件中
with open(input_file) as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            # 如果读到一个新的序列，更新当前染色体的名称
            chr_name = line[1:]
            # 如果该染色体存在于长度字典中
            for i in range(len(chr_length_dict_list)):
                if chr_name in chr_length_dict_list[i]:
                    # 写入染色体的名称
                    current_file_index = i
                    break
            else:
                # 如果该染色体不存在于长度字典中，则跳过该序列
                current_file_index = -1
                continue
        else:
            # 如果当前正在写入的文件已经达到了指定长度，则切换到下一个文件
            if current_file_length >= chr_length_dict_list[current_file_index][chr_name]:
                current_file_length = 0
                output_files[current_file_index].write("\n")
                output_files[current_file_index].write(">{}\n".format(chr_name))
            # 将当前行写入正在写入的文件，并更新该文件已写入的序列长度
            output_files[current_file_index].write(line + "\n")
            current_file_length += len(line)

# 关闭所有输出文件
for output_file in output_files:
    output_file.close()

