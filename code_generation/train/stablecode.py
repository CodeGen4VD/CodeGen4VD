from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import os
from pathlib import Path

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_id = "/home/llm/transformers/stablecode"


tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        ).to(device)

mod_types = ['del_add','add']

for mod_type in mod_types:

    fliter_path = '/home/llm/data/1-fliter/'
    diffpath = fliter_path+"diff/"+mod_type
    novulpath = fliter_path+"novul/"+mod_type
    vulpath = fliter_path+"vul/"+mod_type
    fillpath = fliter_path+"fill/stablecode/"+mod_type
    fullpath = fliter_path+"full/stablecode/"+mod_type
    p1 = Path(os.path.join(fillpath))
    p1.mkdir(parents=True,exist_ok=True)
    p2 = Path(os.path.join(fullpath))
    p2.mkdir(parents=True,exist_ok=True)

    for file_name in os.listdir(diffpath):

        novulfile = os.path.join(novulpath,'0_'+file_name)
        fill_file = os.path.join(fillpath,file_name)
        full_file = os.path.join(fullpath,file_name)
        if(os.path.exists(fill_file)):
            continue

        with open(os.path.join(diffpath,file_name),'r',encoding='utf-8') as f:
            codelines = f.readlines()

        for i,line in enumerate(codelines):
            if line.startswith("@@"):
                split_line = i
                break

        be_diff = ''
        for line in codelines[split_line:]:
            if line.startswith("+"):
                be_diff += line[1:]

        with open(novulfile,'r',encoding='utf-8', errors='ignore') as f:
            code = f.read()

        prompt = '<fim_prefix>'+ code.replace(be_diff,'<fim_suffix>\n') + '<fim_middle>\n'


        try:
            inputs = tokenizer(prompt, return_tensors='pt').to(device)
            outputs = model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.2,
                    do_sample=True,
                    )
            output = tokenizer.decode(outputs[0])
            filled = output.split('<fim_middle>')[1].split('<|endoftext|>')[0]
            print(fill_file)

            with open(fill_file,'w',encoding='utf-8') as f:
                f.write(filled)
            fulled = code.replace(be_diff,filled)
            with open(full_file,'w',encoding='utf-8') as f:
                f.write(fulled)
            
        except:
            with open('./stablecode_log.txt','w') as f:
                f.write(fill_file) 




