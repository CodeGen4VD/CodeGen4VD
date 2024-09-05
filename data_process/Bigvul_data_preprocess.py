import pandas as pd
import os
import difflib
import pickle

def process_raw_data(filter_csv_path, raw_csv_path):
    if os.path.exists(filter_csv_path):
        pd_filter = pd.read_csv(filter_csv_path)
        # pd_filter = pd.read_csv('/home/MSR_data_cleaned_pairs_Test.csv')

    else:
        pd_raw = pd.read_csv(raw_csv_path)
        filter_csv = pd_raw.loc[pd_raw["vul"] == 1]
        filter_csv.to_csv(filter_csv_path)
        pd_filter = pd.read_csv(filter_csv_path)
    return pd_filter

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
    dataset_path = '/home/llm/data/rawdata/'
    raw_data_filename = 'MSR_data_cleaned.csv'
    filter_data_filename = 'MSR_data_cleaned_pairs.csv'
    
    
    filter_csv_path = dataset_path + filter_data_filename
    raw_csv_path = dataset_path + raw_data_filename
    out_path_before = dataset_path+'vul'
    out_path_after = dataset_path+'novul'
    out_path_diff = dataset_path+'diff'
    label_pkl_file = 'bigvul_label_pkl.pkl'
    pkl_path = dataset_path + label_pkl_file

    pd_filter = process_raw_data(filter_csv_path, raw_csv_path)
    file_cnt = pd_filter.shape[0]
    file_num = 0
    label_dict = {}
    cnt_1 = 0

    for index, row in pd_filter.iterrows():
        file_num += 1
        print(str(file_cnt) + ' / ' + str(file_num))
        cve_id = row['CVE ID']
        cwe_id = row['CWE ID']
        project_name = row["project"]
        hash_vaule = row['commit_id']
        try:
            file_name = cve_id + "_" + project_name + "_" + cwe_id + "_" + hash_vaule
        except:
            try:
                file_name = cve_id + "_" + project_name + "_"  + hash_vaule
            except:
                continue
        outfile = file_name

        file_name_cnt = 1
        outfile_new = outfile
        while outfile_new in label_dict.keys():
            outfile_new = outfile + '_' + str(file_name_cnt)
            file_name_cnt += 1
        label_dict[outfile_new] = []

        func_before = row['func_before']
        func_after = row["func_after"]
        diff = list(difflib.unified_diff(func_before.splitlines(), func_after.splitlines()))

        with open(out_path_before + '/'+ '1_'+outfile_new+'.c', 'w', encoding='utf-8') as f_vul:
            f_vul.write(func_before)
            cnt_1 += 1

        with open(out_path_after + '/' + '0_'+outfile_new+'.c', 'w', encoding='utf-8') as f_novul:
            f_novul.write(func_after)
            cnt_1 += 1
        
        with open(out_path_diff + '/' + outfile_new+'.c', 'w', encoding='utf-8') as patch:
            for line in diff:
                patch.write(line)
                patch.write('\n')
        label(func_before, func_after, label_dict, outfile_new)

    with open(pkl_path,'wb') as f:
        pickle.dump(label_dict, f)
        
    print(cnt_1)


if __name__ == '__main__':
    main()

