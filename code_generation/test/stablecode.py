from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import os
from pathlib import Path
import json

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_id = "/home/llm/transformers/stablecode"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        ).to(device)

function_level = ['one','two','three','four','five']
function_line_path = '/home/llm/code/fire/test/mVulPreter/function_line_5.json'
raw_data_path = '/home/llm/data/1-fliter/all'
fillpath = '/home/llm/data/8_test/fill/stablecode/'
fullpath = '/home/llm/data/8_test/full/stablecode/'
p1 = Path(os.path.join(fillpath))
p1.mkdir(parents=True,exist_ok=True)
p2 = Path(os.path.join(fullpath))
p2.mkdir(parents=True,exist_ok=True)

with open(function_line_path,'r',encoding='utf-8') as jf:
    content = jf.read()
function_line = json.loads(content)
for function_name in function_line:
    fillfile_path = os.path.join(fillpath,function_name)
    if not os.path.exists(fillfile_path):
        os.mkdir(fillfile_path)
    fullfile_path = os.path.join(fullpath,function_name)
    if not os.path.exists(fullfile_path):
        os.mkdir(fullfile_path)

    raw_file = os.path.join(raw_data_path,function_name+'.c')
    with open(raw_file,'r') as f:
        code = f.read()
    lines = code.split('\n')
    cnt = 0
    for line in function_line[function_name]:
        line = int(line)
        if line == 1:
            continue
        fillfile = os.path.join(fillfile_path,function_level[cnt]+'_'+
                                function_name + '.c')
        if os.path.exists(fillfile):
            continue      
        fullfile = os.path.join(fullfile_path,function_level[cnt]+'_'+
                                function_name + '.c')
        if os.path.exists(fullfile):
            continue
        prompt = '<fim_prefix>\n' + code.replace(lines[line-1],'<fim_suffix>') + '<fim_middle>\n'
        if prompt.count('<fim_suffix>') >1:
            continue

        try:
            inputs = tokenizer(prompt, return_tensors='pt').to(device)
            outputs = model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.2,
                    do_sample=True,
                    )
            output = tokenizer.decode(outputs[0])

            filling = output.split('<fim_middle>')[1].split('<|endoftext|>')[0]
            with open(fillfile,'w',encoding='utf-8') as f:
                f.write(filling)   
            print(fullfile)
            new_code = code.replace(lines[line-1],filling)
            with open(fullfile,'w',encoding='utf-8') as f:
                f.write(new_code)
            cnt += 1
        except:
            with open('./stablecode_log.txt','w') as f:
                f.write(fullfile) 




