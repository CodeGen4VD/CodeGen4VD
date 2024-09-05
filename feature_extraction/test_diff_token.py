import os
import csv
import Levenshtein
from pathlib import Path
from tqdm import *
import difflib


title = ['file_name','LR','JS','JWS','JSC','DSC']
llms = ['codellama','codeshell','stablecode','starcoder']
function_level = ['one','two','three','four','five']
fullpath = '/home/llm/data/8_test/full/'
raw_data_path = '/home/llm/data/1-fliter/all'
out_path = '/home/llm/data/cmp/test'
p = Path(out_path)
p.mkdir(parents=True,exist_ok=True)    

for llm in llms:

    function_name_list = os.listdir(fullpath+llm)
    for function_name in tqdm(function_name_list):

        fullfile_path = os.path.join(fullpath,llm,function_name)
        raw_file = os.path.join(raw_data_path,function_name+'.c')
        with open(raw_file,'r') as f:
            code = f.read()

        for level in function_level:
            fullfile = os.path.join(fullfile_path,level+'_'+
                        function_name + '.c')
            if not os.path.exists(fullfile):
                continue

            with open(fullfile,'r') as f:
                full = f.read()

            diff = list(difflib.unified_diff(code.splitlines(), full.splitlines()))
            target = ''
            llm_code = ''
            prefix = ''
            suffix = ''
            for i,line in enumerate(diff):
                if line.startswith("@@"):
                    start = i
            start += 2
            for j in range(start,len(diff)):

                if diff[j].startswith("-"):
                    target += diff[j][1:]
                elif diff[j].startswith("+"):
                    llm_code += diff[j][1:]
                else:
                    if target == '' and llm_code == '':
                        prefix += diff[j]
                    else:
                        suffix += diff[j]
            target = prefix + target + suffix
            llm_code = prefix + llm_code + suffix

            target_list = list(target)
            llm_list = list(llm_code)

            out = os.path.join(out_path,llm+'_cmp.csv')            
            if not os.path.exists(out):
                with open(out, 'w',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(title)

            cmp_rat = Levenshtein.ratio(target,llm_code)     
            # Jaro similarity
            cmp_jaro = Levenshtein.jaro(target,llm_code)     
            # Jaro-Winkler similarity
            cmp_jw = Levenshtein.jaro_winkler(target, llm_code)
            # Jaccard similarity coefficient
            try:
                cmp_jsc = len(set(target_list).intersection(llm_list)) / len(set(target_list).union(llm_list))     
            except:
                cmp_jsc = 1.0
            # Dice similarity coefficient
            try:
                cmp_dsc= 2 * len(set(target_list).intersection(llm_list)) / (len(set(target_list)) + len(set(llm_list))) 
            except:
                cmp_dsc = 1.0
            file_name = fullfile.split('/')[-1]
            data = [file_name,cmp_rat,cmp_jaro,cmp_jw,cmp_jsc,cmp_dsc]

            with open(out,'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
