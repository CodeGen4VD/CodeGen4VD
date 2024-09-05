import glob
import os
from pathlib import Path

diff_path = "/home/llm/data/rawdata/diff"
mod_types = ['del_add','add']

for mod_type in mod_types:
    fliter_path = '/home/llm/data/1-fliter/diff/'+mod_type
    p = Path(fliter_path)
    p.mkdir(parents=True, exist_ok=True)
    diff_files = glob.glob(diff_path+'/*.c')
    cnt = 0

    for diff_file in diff_files:
        file_name = diff_file.split('/')[-1]
        flag = 1
        with open(diff_file) as f:
            diff = f.readlines()
        split_list = [i for i,line in enumerate(diff) if line.startswith("@@")]
        split_list.append(len(diff))
        if len(split_list) == 2:
            for i in range(len(split_list) - 1):
                del_index = []
                add_index = []
                start = split_list[i]
                end = split_list[i + 1]
                for index in range(start+1,end):
                    if diff[index].startswith("-"):
                        del_index.append(index)
                    elif diff[index].startswith("+"):
                        add_index.append(index)
                if mod_type == 'del_add':
                    #del_add
                    if add_index == [] or del_index == []:
                        flag = 0
                        continue
                else:
                    # add
                    if add_index == [] or del_index != []:
                        flag = 0
                        continue
                all_index = del_index + add_index
                for i in range(len(all_index) - 1):
                    if all_index[i] + 1 != all_index[i + 1]:
                        flag = 0
                        break
                i += 1
            if flag:
                fliter_diff = os.path.join(fliter_path,file_name)
                if os.path.exists(fliter_diff):
                    continue
                os.system('cp '+ diff_file +' '+fliter_diff)
                cnt+=1

    print(cnt)