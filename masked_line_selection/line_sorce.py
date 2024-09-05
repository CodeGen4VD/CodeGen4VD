import networkx as nx
import numpy as np
import json
import os
from tqdm import *

os.path.exists
def slice_sorce(slice_score_file, threshold = 4):

    with open(slice_score_file, "r") as fp:
        line_list = fp.readlines()

    function = dict()
    for line in tqdm(line_list):
        function_name, slice_path = line.split(":")[0].split(",/home")
        slice_path = '/home'+slice_path
        score1, score2 = line.split(":")[1][8:-3].split(",")
        score1 = float(score1)
        score2 = float(score2)
        if function_name not in function:
            function[function_name] = [{"slice_path": slice_path, "score": score2-score1}]
        else:
            function[function_name].append({"slice_path": slice_path, "score": score2-score1})
    
    for function_name in function:
        # 使用 sorted 函数和 lambda 表达式按 'score' 键的值进行降序排序
        function[function_name] = sorted(
            function[function_name],
            key=lambda x: x['score'],
            reverse=True  # 设置 reverse=True 进行降序排序，如果你想升序排序，可以去掉这个参数或设置为 False
        )

        list_length = len(function[function_name])  # 获取列表的长度
        if list_length > 4:
            # 计算后25%的元素数量，使用 // 进行整数除法确保结果是整数
            items_to_remove = list_length // threshold
            # 切片操作，保留前75%的元素
            function[function_name] = function[function_name][:-1 * items_to_remove]
    return function


def line_sorce(slice_lines,score,_line_sorce):
    with open(slice_lines, "r") as fp:
        line_numbers = json.load(fp)
    
    line_set = set()
    for line_number in line_numbers:
        if line_number != -1:
            line_set.add(line_number)

    for line_number in line_set:
        if  line_number not in _line_sorce:
            _line_sorce[line_number] = score 
        else:
            _line_sorce[line_number] += score

def main():
    slice_score_file = './slice_model/data_loader/slice_probability.txt'
    function_line = './function_line_5.json'
    function = slice_sorce(slice_score_file)
    function_line_dict = dict()
    funcnum = len(function)
    cnt = 1
    for function_name in function:
        line_path = '/home/llm/data/7_line2node/'
        print(str(cnt)+'/'+str(funcnum))
        print(function_name)
        if function_name.startswith('0_'):
            line_path = os.path.join(line_path,'novul')
        elif function_name.startswith('1_'):
            line_path = os.path.join(line_path,'vul')
        line_func = os.path.join(line_path,function_name)

        _line_sorce = dict()
        list_length = len(function[function_name])  # 获取列表的长度
        for i in tqdm(range(list_length)):
            slice_line = line_func + '/' +function[function_name][i]['slice_path'].split('/')[-1]
            score = function[function_name][i]['score']
            line_sorce(slice_line,score,_line_sorce)
        _line_sorce_sort = sorted(_line_sorce.items(), key=lambda item: item[1], reverse=True)
        top_three_lines = [key for key,_ in list(_line_sorce_sort)[:10]]
        
        function_line_dict[function_name] = top_three_lines
        print(function_line_dict[function_name])
        print('-------------------')
        cnt+=1

    with open(function_line,'a') as f:
        f.write(json.dumps(function_line_dict))

if __name__ == "__main__":
    main()







