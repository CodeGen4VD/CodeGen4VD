import os
from re import I
from typing import Container
from preprocess import *
from complete_pdg import *
from slice_op import *
from json_to_dot import *
import argparse
from tqdm import tqdm
from pathlib import Path
import pickle


def main():
    export_path = '/home/llm/data/4-export/'
    bigvul_label_path = '/home/llm/data/rawdata/bigvul_label_pkl.pkl'
    fire_label_path = '/home/llm/data/rawdata/fire_label_pkl.pkl'
    with open(bigvul_label_path, 'rb') as f_label:
        label_dict1 = pickle.load(f_label)
    with open(fire_label_path, 'rb') as f_label:
        label_dict2 = pickle.load(f_label)
    label_dict = label_dict1 + label_dict2
    vuls = ['vul','novul']
    for vul in vuls:

        json_file = export_path+'json/'+vul
        pdg_dot_file = export_path+'pdg/'+vul
        sub_graph_path = '/home/llm/data/5_slices/'+vul
        dict_path='/home/llm/data/7_line2node/'+vul
        p1 = Path(sub_graph_path)
        p1.mkdir(parents=True,exist_ok=True)
        p2 = Path(dict_path)
        p2.mkdir(parents=True,exist_ok=True)

        container = joern_process(json_file)
        i = 0
        sub_cnt = 0
        for data in tqdm(container):
            i += 1
            if data == []:
                sub_cnt += 1
                continue
            data = data[0]
            data_nodes = {}
            idx = data[0]
            cpg = data[1]
            print("===========>>>>>  " + str(i))
            print(idx)

            pdg_edge_list = ddg_edge_genearate(pdg_dot_file, idx)
            if pdg_edge_list == []:
                continue
            data_nodes_tmp = parse_to_nodes(cpg)
            data_nodes = complete_pdg(data_nodes_tmp, pdg_edge_list)

            pointer_node_list = get_pointers_node(data_nodes)
            if pointer_node_list != []:
                _pointer_slice_list = pointer_slice(data_nodes, pointer_node_list)
                points_name = '@pointer'
                generate_sub_json(data_nodes, _pointer_slice_list, sub_graph_path, dict_path, idx, points_name, label_dict)

            arr_node_list = get_all_array(data_nodes)
            if arr_node_list != []:
                _arr_slice_list = array_slice(data_nodes, arr_node_list)
                points_name = '@array'
                generate_sub_json(data_nodes, _arr_slice_list, sub_graph_path, dict_path, idx, points_name, label_dict)

            integer_node_list = get_all_integeroverflow_point(data_nodes)
            if integer_node_list != []:
                _integer_slice_list = inte_slice(data_nodes, integer_node_list)
                points_name = '@integer'
                generate_sub_json(data_nodes, _integer_slice_list, sub_graph_path, dict_path, idx, points_name, label_dict)

            call_node_list = get_all_sensitiveAPI(data_nodes)
            if call_node_list != []:
                _call_slice_list = call_slice(data_nodes, call_node_list)
                points_name = '@API'
                generate_sub_json(data_nodes, _call_slice_list, sub_graph_path, dict_path, idx, points_name, label_dict)          

if __name__ == '__main__':
    main()
