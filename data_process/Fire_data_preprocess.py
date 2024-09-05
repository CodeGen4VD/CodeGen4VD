import pandas as pd
import os
import difflib
import pickle
from pathlib import Path
import glob


def process_raw_data(raw_path,vul_path,novul_path):
    p1 = Path(vul_path)
    p1.mkdir(parents=True, exist_ok=True)
    p2 = Path(novul_path)
    p2.mkdir(parents=True, exist_ok=True)
    cnt = 0
    for dirpath, dirname, files in os.walk(raw_path):

        # print(f'Found directory: {dirpath}')
        if 'CVE' not in dirpath.split('/')[-1]:
            continue
        for file_name in files:

            file = os.path.join(dirpath,file_name.replace(" ","\ "))
            file_name = file_name.replace(" ","")
            if 'OLD' in file_name:
                cnt+=1
                vul_file = os.path.join(vul_path,'1_'+file_name.split('_OLD')[0]+'.c')
                if os.path.exists(vul_file):
                    continue
                print(file)
                os.system("cp " + file +" "+vul_file)
            else:
                novul_file = os.path.join(novul_path,'0_'+file_name.split('_NEW')[0]+'.c')
                if os.path.exists(novul_file):
                    continue
                print(file)
                os.system("cp " + file +" "+novul_file)

def label(f_vul, f_novul ,label_dict, outfile):
    diff = list(difflib.unified_diff(f_novul.splitlines(), f_vul.splitlines()))
    split_list = [i for i,line in enumerate(diff) if line.startswith("@@")]
    split_list.append(len(diff))
    i = 0
    for i in range(len(split_list) - 1):
        start = split_list[i]
        del_linenum = diff[start].split("@@ -")[-1].split(",")[0].split('+')[-1].strip()
        end = split_list[i + 1]
        
        line_num = int(del_linenum)
        for line in diff[start+1 : end]:
            if line.startswith("-"):
                label_dict[outfile].append(line_num)
            elif line.startswith("+"):
                line_num -= 1
            line_num += 1
        i += 1

def main():
    raw_path = "/home/pc/dataset/old-new-and-patchdb"
    dataset_path = '/home/llm/data/rawdata/'
    out_path_before = dataset_path+'vul'
    out_path_after = dataset_path+'novul'
    out_path_diff = dataset_path+'diff'
    process_raw_data(raw_path,out_path_before,out_path_after)
    label_pkl_file = 'fire_label_pkl.pkl'

    pkl_path = dataset_path + label_pkl_file

    vul_files = glob.glob(out_path_before+'/*.c')

    label_dict = {}

    for vul_file in vul_files:
        file_name = vul_file.split('/')[-1][2:]
        novul_file = os.path.join(out_path_after,'0_'+file_name)
        if not os.path.exists(novul_file):
            continue

        label_dict[file_name] = []
        print(file_name)
        with open(vul_file, errors='ignore') as f:
            vul_func = f.read()
        with open(novul_file, errors='ignore') as f:
            novul_func = f.read()

        diff_file = os.path.join(out_path_diff,file_name)
        diff = list(difflib.unified_diff(vul_func.splitlines(), novul_func.splitlines()))
        flag = label(diff,label_dict,file_name)
        if flag == 0:
            continue
        with open(diff_file, 'w', encoding='utf-8') as patch:
            for line in diff:
                patch.write(line)
                patch.write('\n')

    with open(pkl_path,'wb') as f:
        pickle.dump(label_dict, f)


if __name__ == '__main__':
    main()

