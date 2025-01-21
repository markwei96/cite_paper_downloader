import time
import random
from tqdm import tqdm
import argparse
import os
import requests

from web_ops import get_authors_proxy,get_random_ua,decode_cite_text,get_authors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find_Your_Paper_Citer')

    parser.add_argument('-p', '--paper_name', type=str,default='LibCity: An Open Library for Traffic Prediction', required=True,help='论文名称')
    parser.add_argument('-d', '--base_dir', type=str,default='./', help='保存路径')
    parser.add_argument('-dp', '--is_download_pdf', type=bool, default=False, help='是否下载PDF')
    parser.add_argument('-m', '--max_wait', type=int, default=5, help='最大等待时间')
    parser.add_argument('-da', '--is_authors', type=bool, default=True, help='是否获取作者信息')

    parser.add_argument('-b', '--debug', type=bool, default=True, help='Debug mode')

    args = parser.parse_args()

    paper_name = args.paper_name
    base_dir = args.base_dir
    is_debug = args.debug
    is_authors = args.is_authors

    if base_dir[-1] == '/':
        base_dir = base_dir[:-1]

    max_wait = args.max_wait
    is_download_pdf = args.is_download_pdf

    paper_namex = paper_name.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace(' ', '_')
    save_path = f'{base_dir}/{paper_namex}'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

        
    if is_authors:
        ath_get_count = 0
        wait_count = 1
        need_get = []
        al_get = []
        max_retry = 10
        with open(f'./{paper_namex}_authors.csv','a',encoding='utf-8',errors='ignore') as f:
            f.write('title,authors\n')
        with open(f'./{paper_namex}_authors_infos.csv','r',encoding='utf-8',errors='ignore') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('title'):
                continue
            line = line.strip().split(';')
            need_get.append([line[1],line[0]])
            al_get.append([line[1],line[0]])

        get_count = {}
        for item in need_get:
            get_count[item[1]] = 0
        while 1:
            if len(al_get) == 0:
                break
            exit_mark = True
            for key,value in get_count.items():
                if value == -1:
                    continue
                if value < max_retry:
                    exit_mark = False
            if exit_mark:
                t = 0
                
                for key,value in get_count.items():
                    if not value < max_retry:
                        print(key)
                        t+=1
                print(f"{t} papers has max retry , please manual op")
                break
            for pp in tqdm(need_get,desc='Getting authors...'):
                if not pp in al_get:
                    continue
                authors = get_authors_proxy(pp[0],is_debug)
                if is_debug:
                    with open('./debug.log','a') as f:
                        f.write(str(authors)+'\n')
                        f.write('\n')
                if len(authors) > 0:
                    with open(f'./{paper_namex}_authors.csv','a',encoding='utf-8',errors='ignore') as f:
                        f.write(f"{pp[1]},{';'.join(authors)}\n")
                    al_get.remove(pp)
                    get_count[pp[1]] = -1
                else:
                    get_count[pp[1]] +=1
                
    print('Every thing done!')