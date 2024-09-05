from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import os
from pathlib import Path
import json

model_id = "/home/llm/transformers/codellama"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16
).to("cuda")

function_level = ['one','two','three','four','five']
function_line_path = '/home/llm/code/masked_line_selection/function_line_5.json'
raw_data_path = '/home/llm/data/1-fliter/all'
fillpath = '/home/llm/data/8_test/fill/codellama/'
fullpath = '/home/llm/data/8_test/full/codellama/'
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
        prompt = code.replace(lines[line-1],'<FILL_ME>')
        if prompt.count('<FILL_ME>') >1:
            continue

        try:
            input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"].to("cuda")
            output = model.generate(
                input_ids,
                max_new_tokens=200,
            )
            output = output[0].to("cpu")

            filling = tokenizer.decode(output[input_ids.shape[1]:], skip_special_tokens=True)

            with open(fillfile,'w',encoding='utf-8') as f:
                f.write(filling)   
            print(fullfile)
            new_code = code.replace(lines[line-1],filling)
            with open(fullfile,'w',encoding='utf-8') as f:
                f.write(new_code)
            cnt += 1
        except:
            with open('./codellama_log.txt','w') as f:
                f.write(fullfile)






