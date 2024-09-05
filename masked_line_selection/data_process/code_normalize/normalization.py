# coding=utf-8
import os
import re
import shutil
from clean_gadget import clean_gadget
from pathlib import Path



# 遍历预处理后的文件，对每个文件进行规范化
def normalize(path,vul):
    file_list = os.listdir(path)
    for _file in file_list:
        pro_one_file(os.path.join(path, _file),vul)


# 单个文件规范化
def pro_one_file(filepath,vul):
    # 去除头部注释
    print(filepath)
    linefeed='\n'
    with open(filepath, "r", errors='ignore') as file:
        code = file.read()
    annotations = re.findall('(?<!:)\\/\\/.*|\\/\\*(?:\\s|.)*?\\*\\/', code)
    #print(annotations)
    for annotation in annotations:
        lf_num = annotation.count('\n')
        if lf_num == 0:
            code = code.replace(annotation,'')
            continue
        code = code.replace(annotation,lf_num*linefeed)
    #code = re.sub('(?<!:)\\/\\/.*|\\/\\*(\\s|.)*?\\*\\/', '', code)
    file_name=filepath.split('/')[-1]
    #filepath = filepath.replace("all_novul_slices_src", "8-slices-src_without_comment")
    temp_file='/home/llm/data/2-normalize/temp/'+vul
    p = Path(temp_file)
    p.mkdir(parents=True,exist_ok=True)
    temp_file2=os.path.join(temp_file, file_name)
    #with open(filepath, "w") as file:
    with open(temp_file2, "w") as file:
        file.write(code.strip())
    # 规范化
    #with open(filepath, "r") as file:
    with open(temp_file2, "r") as file:
        org_code = file.readlines()
        nor_code = clean_gadget(org_code)

    norm_path="/home/llm/data/2-normalize/"+vul
    p = Path(norm_path)
    p.mkdir(parents=True,exist_ok=True)
    norm_path2=os.path.join(norm_path, file_name)
    #with open(filepath, "w") as file:
    with open(norm_path2, "w") as file:
        file.writelines(nor_code)


if __name__ == '__main__':
    vuls = ['novul','vul']
    for vul in vuls:
        normalize("/home/llm/data/1-fliter/"+vul+"/del_add",vul)




