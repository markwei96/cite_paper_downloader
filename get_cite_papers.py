from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import random
from tqdm import tqdm
import argparse
import os
import requests
from bs4 import BeautifulSoup

from web_ops import get_authors_proxy,get_random_ua,decode_cite_text,safe_bot_request_proxy

def setWebDriver(save_path):
    service=Service('./web_driver/msedgedriver.exe')
    options = webdriver.EdgeOptions()
    prefs = {
        "download.default_directory": save_path,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    headers = {
            "User-Agent": get_random_ua(),
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cache-control": "max-age=0",
            # "cookie": "__cfduid=d25efa21dde4a114e7dd96b477e0aba381531100939; FR24ID=0l69ten5b83uoqjui6ufipkbb14hb2li3pd8hcfqtar0uptt84r0; __utma=177865842.2011292994.1531100944.1531100944.1531100944.1; __utmc=177865842; __utmz=177865842.1531100944.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=177865842.1.10.1531100944"
            "cookie": "__Secure-ENID=21.SE=AahQx5gYvJ-uxVfRpFaLXAi30qm23F3UVYSYaVHf2dhSeAA42kOONEoajw6hlPGetOS-PXHKSwCx3dwJls0S7vLQTE47CjYEs3p_SOmxbR_4rod80TkGV8HXWyvSR2ye4t3T4b_tMZURHU1zvcgrjlM9ZHjDPmrwbNxvRCQ7g5vA2bIyiFlV2mfIAwPaQfc9RwMYf2AsWgQ8n71QEAnYfzTCNE9144tafZwfLa8eIafyhXfeK7WnoiKp9acpzoxLGwTdSrFm2urUthRXp0EWJooc9kE2Jfoj0Ecjm20; HSID=AEmGbzz4ZvrmDfvnU; SSID=Atrpx2xqPy1sbd23O; APISID=585xvnk1N5J95HbV/Ac9xiINqoXJptMa85; SAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; __Secure-1PAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; __Secure-3PAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; GSP=A=KhlVtQ:CPTS=1732600504:LM=1732600504:S=o5pGDcQSM1TCFVC8; SID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASly_nDKBf1YUcCE0QigknGAACgYKAbkSARESFQHGX2Mi5TX6r0WWWf3EX9Z6Ku78mRoVAUF8yKqXU1TTnDuZzRmd7mvGCoLE0076; __Secure-1PSID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASjz77ReXb4rwvz6Sf1QS5WgACgYKAVQSARESFQHGX2MipDJ0Q8El9Bo1ZVPUanGeMhoVAUF8yKpj1sF7MedsYCsWKbalHHSG0076; __Secure-3PSID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASElRIm5qtI1Fm23QrYowHcgACgYKAdISARESFQHGX2MiNImDRPQDhuTDvnqdG3zPNxoVAUF8yKqohZnrp6GtEIYk6cfWLiLS0076; SEARCH_SAMESITE=CgQIgZ0B; AEC=AZ6Zc-VoPElF8Q8p3o7M5xHNX2TweC5SKWn73RHXEEOPFnWaUJEgN3makA; __Secure-1PSIDTS=sidts-CjIBmiPuTfNCC7sODJGt0tIAUTWmNT1g6qz3ArW4EhUkI2Z6BGxkSdtMzPQObCnwE1498hAA; __Secure-3PSIDTS=sidts-CjIBmiPuTfNCC7sODJGt0tIAUTWmNT1g6qz3ArW4EhUkI2Z6BGxkSdtMzPQObCnwE1498hAA; NID=520=DYXabZX9E0Owkf8qWSZReqfSfmmLd2_58HAEWWV90HfpISvMrJi7IFRcPp7lvupyyaZ-lcJm03_Iqk0ZvWm8x-oKBmHskfrx8uSfxal1eee6ovRGKU553U3GXYnCaxMt7ZCAXb03HUE78LUFRp7WRrcNkUMoSDGVuwUrcq4r91AP-JMrySZD8a_w3lDV63ZeAhK3qsvBV9zl3X09PFEhc1c41UhKizk-Lg00MWgUS_ECIxPjCrjUnJjckjdYSlqQd05eBwtyP-IAz6H4ko2YzrqHS7vOx9983YGp412r7czdAMWI7L2utNl2YUE1qEEAFaeVrXa_Krt9O6pfDJXMGtjf51BunBsbDWwE61ArrJqibHscu0dzGvv_6xpdfxka6ChqgVz1d6qMTzArytDwgxlE2FOrPY8QXwsKwKovQh9tz-PCz6x0pb8LSzkjwfntRwE0IUjQB55cEs1ULhvWxgW2KUqD3XXP15NJe2tv-sdXfO5wO_BiQKtPb5O1TxCI-uu6kJjKvAnaeCXghDov4IoxAkLPTClji5d5zw9t0gNkvogxw5mAMSVil_FfPHltVd8IUb9Xiea-J3uZG4pweuBaVT9QpdufGT7tNX-3--9EHh0EqDCThNVQm5AadZRtzSt_2z__3lRLwgbbIPQ3WUoqdJBDoULmIUpQnaDwdKDR8KfEHSw717sTwMgbjkn1cx390ta9cWqxYIsm2UNKjLpA0-c4bVa3oZLPttX3eN3rdJz5499zxEfCrjl9SwehEmicRf1ReZjG5EWwIXK_8HOJ_LHIHyoMzrW06--tV6dRRqAbyx3kqd8rklrLCYgsiro1Wkl0IehfN9bS9kGSYQ; SIDCC=AKEyXzWg6Ay7crhnfb9pZWKRbbfOPfj63wk-hcCv6k-L9iWWt2-rwjsuen9M8flj-N6j0evpDl4; __Secure-1PSIDCC=AKEyXzW_USqd9nsX7by10zsepLJIGIl3a6qkKCbMeQ98bTk37YKDtDIX7CFxKW9ga3eIaxDzzQ; __Secure-3PSIDCC=AKEyXzVnxY9_C1gzcHHcriOx96Yc5ye5ll10DuJHOJXh51Z4kisHnKWDBQCc-JYZvrB16p0M3cM"
        }

    for key, value in enumerate(headers):
        capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
        webdriver.DesiredCapabilities.CHROME[capability_key] = value

    options.add_experimental_option("prefs", prefs)
    options.add_argument('--ignore-certificate-errors')

    driver=webdriver.Edge(options=options,service=service)
    driver.set_window_size(width=800,height=1000)
    return driver



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find_Your_Paper_Citer')

    parser.add_argument('-p', '--paper_name', type=str, required=True,help='Paper Name')
    parser.add_argument('-d', '--base_dir', type=str,default='./', help='Save Path')
    parser.add_argument('-dp', '--is_download_pdf', type=bool, default=False, help='Set True to download PDF')
    parser.add_argument('-m', '--max_wait', type=int, default=5, help='Max Waitting Time')
    parser.add_argument('-da', '--is_authors', type=bool, default=False, help='Set True to get authors info')

    parser.add_argument('-b', '--debug', type=bool, default=False, help='Debug mode')

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

    # driver = setWebDriver(save_path)
    

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

    file = open(f'./{paper_namex}_full_report.csv','w',encoding='utf-8',errors='ignore')
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
            with open(f'./{paper_namex}_full_report.csv','a',encoding='utf-8',errors='ignore') as f:
                tex = f"{title.replace(',','_')},,{title_link},{pdf_link},0"
                f.write(f'{tex}\n')
            with open(f'./{paper_namex}_authors_infos.csv','a',encoding='utf-8',errors='ignore') as f:
                f.write(f'{title};{paper_id}\n')
            if is_debug:
                print(tex)
                with open('./debug.txt','a',errors='ignore') as f:
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
            get_count[item[0]] = 0
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
                    with open('./debug.log','a') as f:
                        f.write(str(authors)+'\n')
                        f.write('\n')
                if len(authors) > 0:
                    with open(f'./{paper_namex}_authors.csv','a',encoding='utf-8',errors='ignore') as f:
                        f.write(f"{pp[1]},{';'.join(authors)}\n")
                    al_get.remove(pp)
                    get_count[pp[0]] = -1
                else:
                    get_count[pp[0]] +=1

    print('Every thing done!')