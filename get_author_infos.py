from tqdm import tqdm
import argparse
import os
import requests
from bs4 import BeautifulSoup

from web_ops import safe_bot_request_proxy,checkProxyUsingArea

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find_Your_Paper_Citer')

    parser.add_argument('-p', '--paper_name', type=str, required=True,help='Paper Name')
    parser.add_argument('-d', '--base_dir', type=str,default='./', help='Save Path')
    parser.add_argument('-dp', '--is_download_pdf', type=bool, default=False, help='Set True to download PDF')
    parser.add_argument('-m', '--max_wait', type=int, default=5, help='Max Waitting Time')
    parser.add_argument('-da', '--is_authors', type=bool, default=False, help='Set True to get authors info')

    parser.add_argument('-sk', '--skip', type=int, default=-1, help='Set start pos')

    parser.add_argument('-b', '--debug', type=bool, default=False, help='Debug mode')

    args = parser.parse_args()

    paper_name = args.paper_name
    base_dir = args.base_dir
    is_debug = args.debug
    is_authors = args.is_authors
    start = args.skip

    checkProxyUsingArea()

    if base_dir[-1] == '/':
        base_dir = base_dir[:-1]

    max_wait = args.max_wait
    is_download_pdf = args.is_download_pdf

    paper_namex = paper_name.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace(' ', '_')
    save_path = f'{base_dir}/{paper_namex}'
    pdf_path = f'{base_dir}/{paper_namex}/pdf'
    if not os.path.exists(pdf_path):
        os.makedirs(pdf_path)
    datas =[]
    with open(f'./{save_path}/authors.csv','r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('title') or line =='':continue
            items = line.split(',')
            authours = items[-1].split(';')
            cite_title = ','.join(items[:-1])
            datas.append([cite_title,authours])

    athss = []
    miss = []

    if start == -1:

        for cite_title,authours in tqdm(datas,desc='Getting authors info...'):
            x = requests.utils.quote(cite_title.replace(' ','+'),safe='+')
            url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={x}&btnG="
            res = safe_bot_request_proxy(url,is_debug)
            soup = BeautifulSoup(res.text, "html.parser")
            divs_with_gs_or = soup.find_all("div", class_="gs_or")
            for div in divs_with_gs_or:
                tag = div.find_all('div')
                pdf_link,title,title_link,paper_id = '','','',''
                for xx in tag:
                    class_names = xx.get('class')
                    if class_names:
                        if class_names[0] == 'gs_ri':
                            h3_box = xx.find('h3')
                            a_box = h3_box.find('a')
                            if a_box:
                                title = a_box.get_text()
                                title_link = a_box.get('href')
                                paper_id = a_box.get('id')
                            else:
                                sp_box = h3_box.find_all('span')
                                title = sp_box[-1].get_text()
                                paper_id = sp_box[-1].get('id')
                        elif class_names[0] == 'gs_fmaa':
                            a_boxs = xx.find_all('a')
                            for a_box in a_boxs:
                                ath = a_box.get_text()
                                a_link = a_box.get('href')
                                if title == cite_title:
                                    athss.append([title,ath,a_link])
                                else:
                                    miss.append([title,ath,a_link])

        with open(f'./{save_path}/authors_full.csv','w',encoding='utf-8',errors='ignore') as f:
            for title,ath,a_link in athss:
                f.write(f'{title},{ath},{a_link}\n')

        with open(f'./{save_path}/authors_miss.csv','w',encoding='utf-8',errors='ignore') as f:
            for title,ath,a_link in miss:
                f.write(f'{title},{ath},{a_link}\n')

        with open(f'./{save_path}/authors_full_info.csv','a',encoding='utf-8',errors='ignore') as f:
            f.write(f'full_name,depertment,homepage_link,cite_num,cite_num_2022,N/S/PNAS\n')

    if start >= 0:
        with open(f'./{save_path}/authors_full.csv','r',encoding='utf-8',errors='ignore') as f:
            for line in f:
                line = line.strip()
                items = line.split(',')
                athss.append([','.join(items[:-2]),items[-2],items[-1]])
        if start == 0:
            with open(f'./{save_path}/authors_full_info.csv','a',encoding='utf-8',errors='ignore') as f:
                f.write(f'full_name,depertment,homepage_link,cite_num,cite_num_2022,N/S/PNAS\n')

    cot = 0
    for _,ath,a_link in tqdm(athss,desc='Getting detials...'):
        cot+=1
        if cot < start:continue
        url = f"https://scholar.google.com{a_link}"
        response = safe_bot_request_proxy(url,is_debug)
        soup = BeautifulSoup(response.text, "html.parser")
        divs_full_name = soup.find("div", id="gsc_prf_in")
        full_name,depertment,homepage_link,cite_num,cite_num_2022 ='','','','',''
        if divs_full_name:
            full_name = divs_full_name.get_text()
        divs_infos = soup.find_all("div", class_="gsc_prf_il")
        if len(divs_infos) == 3:
            depertment = divs_infos[0].get_text()
            hl = divs_infos[1].find("a")
            homepage_link =''
            if hl:
                homepage_link = hl.get("href")
        cite_info = soup.find_all("td", class_="gsc_rsb_std")
        if len(cite_info) >= 2:
            cite_num = cite_info[0].get_text()
            cite_num_2022 = cite_info[1].get_text()

        with open(f'./{save_path}/authors_full_info.csv','a',encoding='utf-8',errors='ignore') as f:
            f.write(f"{full_name.replace(',','_')},{depertment.replace(',','_')},{homepage_link},{cite_num},{cite_num_2022}")

        round_count = 0
        n_num,s_num,pnas_num = 0,0,0

        pp_names = ['nature','proceedings of the national academy of sciences','science']
        
        while 1:
            url = f"https://scholar.google.com{a_link}&cstart={round_count * 100}&pagesize=100"
            response = safe_bot_request_proxy(url,is_debug)
            soup = BeautifulSoup(response.text, "html.parser")
            detials_tr = soup.find_all("tr", class_="gsc_a_tr")
            for dt in detials_tr:
                    pp = dt.find_all("div", class_="gs_gray")
                    if len(pp) > 0:
                        pp = pp[-1]
                        if pp:
                            stt = pp.get_text()
                            for i in range(len(pp_names)):
                                if pp_names[i] in stt.lower():
                                    if i == 0:
                                        with open(f'./{save_path}/authors_nature_list.csv','a',encoding='utf-8',errors='ignore') as f:
                                            f.write(f'{ath},{stt}\n')
                                        n_num += 1
                                    elif i == 1:
                                        with open(f'./{save_path}/authors_pnas_list.csv','a',encoding='utf-8',errors='ignore') as f:
                                            f.write(f'{ath},{stt}\n')
                                        pnas_num += 1
                                    elif i == 2:
                                        with open(f'./{save_path}/authors_science_list.csv','a',encoding='utf-8',errors='ignore') as f:
                                            f.write(f'{ath},{stt}\n')
                                        s_num += 1
            if len(detials_tr) < 100:
                break
            round_count += 1
        with open(f'./{save_path}/authors_full_info.csv','a',encoding='utf-8',errors='ignore') as f:
            f.write(f',{n_num}/{s_num}/{pnas_num}\n')