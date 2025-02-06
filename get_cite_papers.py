from tqdm import tqdm
import argparse
import os
import requests
from bs4 import BeautifulSoup

from web_ops import get_authors_proxy,safe_bot_request_proxy,checkProxyUsingArea



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find_Your_Paper_Citer')

    parser.add_argument('-p', '--paper_name', type=str, required=True,help='Paper Name')
    parser.add_argument('-d', '--base_dir', type=str,default='./', help='Save Path')
    parser.add_argument('-dp', '--is_download_pdf', type=bool, default=False, help='Set True to download PDF')
    parser.add_argument('-m', '--max_wait', type=int, default=5, help='Max Waitting Time')
    parser.add_argument('-da', '--is_authors', type=bool, default=True, help='Set True to get authors info')

    parser.add_argument('-b', '--debug', type=bool, default=False, help='Debug mode')

    args = parser.parse_args()

    paper_name = args.paper_name
    base_dir = args.base_dir
    is_debug = args.debug
    is_authors = args.is_authors

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


    x = requests.utils.quote(paper_name.replace(' ','+'),safe='+')
    url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={x}&oq="
    
    res = safe_bot_request_proxy(url,is_debug)

    soup = BeautifulSoup(res.text, "html.parser")
    divs_with_gs_or = soup.find_all("div", class_="gs_or")

    cited_by_link = ''
    for div in divs_with_gs_or:
        tag = div.find_all('div')
        for xx in tag:
                class_names = xx.get('class')
                if class_names:
                    if class_names[0] == 'gs_ri':
                        h3_box = xx.find('h3')
                        a_box = h3_box.find('a')
                        if a_box:
                            title = a_box.get_text()
                        else:
                            sp_box = h3_box.find_all('span')
                            title = sp_box[-1].get_text()
                    elif class_names[0] == 'gs_fl':
                        a_boxs = xx.find_all('a')
                        for a_box in a_boxs:
                            if a_box.get_text().startswith('Cited by'):
                                cited_by_link = a_box.get('href')
                                break
        if title == paper_name:
            break
    
    url = f"https://scholar.google.com{cited_by_link}"

    response = safe_bot_request_proxy(url,is_debug)

    datass = []

    file = open(f'./{save_path}/full_report.csv','w',encoding='utf-8',errors='ignore')
    file.write('title,authors,title_link,pdf_link,save_path\n')
    file.write(',,,,for save_path 0-not download 1-download path set in code 2-system default download path\n')
    file.close()

    page = 0
    auth_get_count = 0
    wait_count = 1

    while 1:
        text2 = response.text
        soup = BeautifulSoup(text2, "html.parser")
        divs_with_gs_or = soup.find_all("div", class_="gs_or")
        #  get items in result for title,title_link,pdf_link,paper_id
        for div in divs_with_gs_or:
            tag = div.find_all('div')
            pdf_link,title,title_link,paper_id = '','','',''
            for xx in tag:
                class_names = xx.get('class')
                if class_names[0] == 'gs_or_ggsm':
                    pdf_link = xx.find('a').get('href')
                elif class_names[0] == 'gs_ri':
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
            datass.append([title,[],title_link, pdf_link,0])
            with open(f'./{save_path}/full_report.csv','a',encoding='utf-8',errors='ignore') as f:
                tex = f"{title.replace(',','_')},,{title_link},{pdf_link},0"
                f.write(f'{tex}\n')
            with open(f'./{save_path}/authors_infos.csv','a',encoding='utf-8',errors='ignore') as f:
                f.write(f'{title};{paper_id}\n')
            if is_debug:
                print(tex)
                with open(f'./{save_path}/debug.txt','a',errors='ignore') as f:
                    f.write(f'{title};{paper_id}\n')
        next_btn_link = ''
        next_btn = soup.find_all("div", id="gs_n")[0].find_all('td')[-1].find('a')
        if next_btn:
            next_btn_link = next_btn.get('href')
        if next_btn_link == '':
            break
        else:
            url = f"https://scholar.google.com{next_btn_link}"
            response = safe_bot_request_proxy(url,is_debug)

    print(f'cite paper info is ready in ./{paper_namex}_full_report.csv')

    if is_authors:
        ath_get_count = 0
        wait_count = 1
        need_get = []
        al_get = []
        with open(f'./{save_path}/authors.csv','a',encoding='utf-8',errors='ignore') as f:
            f.write('title,authors\n')
        with open(f'./{save_path}/authors_infos.csv','r',encoding='utf-8',errors='ignore') as f:
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
        print("Maybe have serval processbar don't worry,it's just re-get some fail info")
        while 1:
            if len(al_get) == 0:
                break
            exit_mark = True
            for key,value in get_count.items():
                if value == -1:
                    continue
                if value < 5:
                    exit_mark = False
            if exit_mark:
                print("Some paper has max retry:")
                for key,value in get_count.items():
                    if not value < 5:
                        print(key)
            for pp in tqdm(need_get,desc='Getting authors...'):
                if not pp in al_get:
                    continue
                authors = get_authors_proxy(pp[0],is_debug)
                if is_debug:
                    with open(f'./{save_path}/debug.log','a') as f:
                        f.write(str(authors)+'\n')
                        f.write('\n')
                if len(authors) > 0:
                    with open(f'./{save_path}/authors.csv','a',encoding='utf-8',errors='ignore') as f:
                        f.write(f"{pp[1]},{';'.join(authors)}\n")
                    al_get.remove(pp)
                    get_count[pp[1]] = -1
                else:
                    get_count[pp[1]] +=1

    
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

        for _,ath,a_link in tqdm(athss,desc='Getting detials...'):
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

    print('Every thing done!')