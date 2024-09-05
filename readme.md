## CodeGen4VD
We implement CodeGen4VD, a novel method to improve vulnerability detection by leveraging the code generation capabilities of CodeLLMs. 

## Dataset

The Dataset we used in the paper:
Fan et al / MSR'20: https://drive.google.com/file/d/1-0VhnHBp9IGh90s2wCNjeCMuy70HPl8X/view?usp=sharing


## Environment
- Joern 1.1.172.
You can find it in Joern's historical releases:  https://github.com/joernio/joern
- Networkx 2.4 / 2.5
- Pytorch 1.5
- transformers 4.40.0
- tqdm 4.64.1
- numpy 1.23.3
- sklearn 1.1.2
- CodeLlama-7B
You can find it in Hugging Face:  https://huggingface.co/meta-llama/CodeLlama-7b-hf
- CodeShell-7B
You can find it in Hugging Face:  https://huggingface.co/WisdomShell/CodeShell-7B
- StableCode-3B
You can find it in Hugging Face:  https://huggingface.co/stabilityai/stable-code-3b
- StarCoder-3B
You can find it in Hugging Face:  https://huggingface.co/bigcode/starcoderbase-3b
  
## Preprocess
1.Run data_process file folder  ```Bigvul_data_preprocess.py``` to get codes from MSR dataset.

2.Run data_process file folder  ```Fire_data_preprocess.py``` to get codes from Fire dataset.

3.Run data_process file folder  ```diff_fliter``` to fliter our dataset.

4.Run data_process file folder  ```diff_func``` to use diff files to match vul files and novul files in our dataset.

## Training Phase
### Code Generation
Run code_generation/train file folder  ```codellama.py```,```codeshell.py```,```stablecode.py```,```starcoder.py``` to use CodeLLMs to generate code for train data,respectively.
### Feature Extraction
Run feature_extraction file folder  ```diff_token.py``` to extract the feature vector of train data for 4 CodeLLMs.

## Testing Phase
### Mask Localization
1.Run masked_line_selection/data_process/code_normalize file folder  ```normalization.py``` to normalize the codes.

2.Use joern to generate PDG graphs, we give py scripts in masked_line_selection/data_process/ file folder. 
```python joern_graph_gen.py -t pasre``` to get .bin file.
```python joern_graph_gen.py -t export -r pdg``` to get .dot file.
```python joern_graph_gen.py -t export -r json``` to get line_info.json.

3.Run masked_line_selection/slice file folder ```main.py``` to slice the pdg.

4.Run masked_line_selection file folder ```train_embedding.py``` to get trained w2v model.

5.Run masked_line_selection file folder ```joern_to_model.py``` to get the data required by the VD model.

6.Run masked_line_selection/slice_model file folder ```slice_detector.py``` to predict results of slices.

7.Run masked_line_selection file folder ```line_sorce.py``` to locate the candidate masked lines.
### Code Generation
Run code_generation/test file folder  ```codellama.py```,```codeshell.py```,```stablecode.py```,```starcoder.py``` to use CodeLLMs to generate code for test data,respectively.
### Feature Extraction
Run feature_extraction file folder  ```test_diff_token.py``` to extract the feature vector of test data for 4 CodeLLMs.

## Vulnerability Detection
1.Run vulnerability detection file folder  ```classification.py``` to detect whether the test code is vulnerable.

2.Run vulnerability detection file folder  ```evaluate.py``` to evaluate the preformance of the system.

 
