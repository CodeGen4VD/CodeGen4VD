import os
import glob


def main():

    input_dir = '/home/llm/data/5_slices/vul/'
    func_list = os.listdir(input_dir)
    for func_name in func_list:
        func_path = os.path.join(input_dir,func_name)
        # print(func_path)
        dots_tmp = glob.glob(func_path + '/' + '*.dot')
        for dot in dots_tmp:
            # with open(dot,'r+') as fp:
            #     flists=fp.readlines()
            # for flist in flists:
            #     if '\\\\\"' in flist:
            #         print(flist)
            with open(dot,'r') as f:
                content = f.read()
            with open(dot,'w') as f:
                f.write(content.replace('\\\\\"',''))

    
if __name__ == '__main__':
    main()

