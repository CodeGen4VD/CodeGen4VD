import os
from pathlib import Path

mod_types = ['del_add','add']

vul_path = "/home/llm/data/rawdata/vul"
novul_path = "/home/llm/data/rawdata/novul"
for mod_type in mod_types:

    fliter_diff = '/home/llm/data/1-fliter/diff/'+mod_type#del_add
    fliter_vul = "/home/llm/data/1-fliter/vul/"+mod_type
    fliter_novul = "/home/llm/data/1-fliter/novul/"+mod_type
    p1 = Path(fliter_vul)
    p1.mkdir(parents=True, exist_ok=True)
    p2 = Path(fliter_novul)
    p2.mkdir(parents=True, exist_ok=True)

    files = os.listdir(fliter_diff)
    for file in files:
        vul = '1_'+file
        novul = '0_'+file
        vul_file = os.path.join(vul_path,vul)
        novul_file = os.path.join(novul_path,novul)
        os.system('cp ' + vul_file + ' '+fliter_vul)
        os.system('cp ' + novul_file +' '+fliter_novul)

