import os
import csv
import Levenshtein
from pathlib import Path

title = ['file_name','LR/AF','JS/AF','JWS/AF','JSC/AF','DSC/AF','LR/B4','JS/B4','JWS/B4','JSC/B4','DSC/B4']
llms = ['codellama','codeshell','stablcode','starcoder']
mod_types = ['del_add','add']

for mod_type in mod_types:

    fliter_path = '/home/llm/data/1-fliter/'
    diffpath = fliter_path+"diff/"+mod_type
    fillpath = fliter_path+"fill/codellama/"+mod_type
    out_path = "/home/llm/data/cmp/train/"+mod_type
    p = Path(out_path)
    p.mkdir(parents=True,exist_ok=True)    

    difflist = os.listdir(diffpath)
    file_cnt = len(difflist)
    file_num = 0

    for file_name in difflist:
        print(file_name)
        file_num += 1
        print(str(file_cnt) + ' / ' + str(file_num))

        with open(os.path.join(diffpath,file_name),'r') as f:
            codelines = f.readlines()

        b4 = ''
        af = ''
        prefix = ''
        suffix = ''
        for i,line in enumerate(codelines):
            if line.startswith("@@"):
                start = i
        start += 2
        for j in range(start,len(codelines)):

            if codelines[j].startswith("-"):
                b4 += codelines[j][1:]
            elif codelines[j].startswith("+"):
                af += codelines[j][1:]
            else:
                if b4 == '' and af == '':
                    prefix += codelines[j]
                else:
                    suffix += codelines[j]
        b4 = prefix + b4 + suffix
        af = prefix + af + suffix
        b4_list = list(b4)
        af_list = list(af)
        # print('b4:' + b4)
        # print('af:' + af)

        for llm in llms:
        
            fill_file = os.path.join(fillpath,llm,mod_type,file_name)
            if not os.path.exists(fill_file):
                continue

            out = os.path.join(out_path,llm+'_cmp.csv')            
            if not os.path.exists(out):
                with open(out, 'w',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(title)
            
            with open(fill_file,'r') as f:
                fill = f.read()
            fill = prefix + fill + suffix
            fill_list = list(fill)
            
            # print(fill)
            # print('------------------------')
            # input()
            
            cmp_before_rat = Levenshtein.ratio(b4,fill)     
            cmp_after_rat = Levenshtein.ratio(af,fill)
            # Jaro similarity
            cmp_before_jaro = Levenshtein.jaro(b4,fill)     
            cmp_after_jaro = Levenshtein.jaro(af,fill)
            # Jaro-Winkler similarity
            cmp_before_jw = Levenshtein.jaro_winkler(b4, fill)      
            cmp_after_jw = Levenshtein.jaro_winkler(af, fill)
            # Jaccard similarity coefficient
            # if mod_type == 'add':
            #     if fill_list == b4_list:
            #         cmp_before_jsc = 1
            #     else:
            #         cmp_before_jsc = 0
            # else:
            cmp_before_jsc = len(set(b4_list).intersection(fill_list)) / len(set(b4_list).union(fill_list))     
            cmp_after_jsc = len(set(af_list).intersection(fill_list)) / len(set(af_list).union(fill_list))
            # Dice similarity coefficient
            # if mod_type == 'add':
            #     if fill_list == b4_list:
            #         cmp_before_dsc = 1
            #     else:
            #         cmp_before_dsc = 0
            # else:
            cmp_before_dsc= 2 * len(set(b4_list).intersection(fill_list)) / (len(set(b4_list)) + len(set(fill_list)))       
            cmp_after_dsc= 2 * len(set(af_list).intersection(fill_list)) / (len(set(af_list)) + len(set(fill_list)))
            
            data = [file_name,cmp_after_rat,cmp_after_jaro,cmp_after_jw,cmp_after_jsc,cmp_after_dsc,cmp_before_rat,cmp_before_jaro,cmp_before_jw,cmp_before_jsc,cmp_before_dsc]

            with open(out,'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)


