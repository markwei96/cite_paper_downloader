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

from web_ops import get_authors

def setWebDriver(save_path):
    service=Service(ChromeDriverManager().install())
    chrome_options = Options()
    prefs = {
        "download.default_directory": save_path,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
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

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--ignore-certificate-errors')

    driver=webdriver.Chrome(options=chrome_options,service=service)
    driver.set_window_size(width=800,height=1000)
    return driver

def bot_check(driver):
    items = driver.find_elements(By.ID, 'recaptcha-anchor-label')
    if len(items) > 0:
        input("Please complete the bot check and press enter to continue...")
        time.sleep(3)
        bot_check(driver)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find_Your_Paper_Citer')

    parser.add_argument('-p', '--paper_name', type=str, required=True,help='论文名称')
    parser.add_argument('-d', '--base_dir', type=str,default='./', help='保存路径')
    parser.add_argument('-dp', '--is_download_pdf', type=bool, default=False, help='是否下载PDF')
    parser.add_argument('-m', '--max_wait', type=int, default=5, help='最大等待时间')

    args = parser.parse_args()

    paper_name = args.paper_name
    base_dir = args.base_dir

    if base_dir[-1] == '/':
        base_dir = base_dir[:-1]

    max_wait = args.max_wait
    is_download_pdf = args.is_download_pdf

    paper_namex = paper_name.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace(' ', '_')
    save_path = f'{base_dir}/{paper_namex}'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    driver = setWebDriver(save_path)

    url ='https://scholar.google.com/'
    driver.get(url)
    google_scholar_search_box = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gs_hdr_tsi"]')))
    google_scholar_search_box.send_keys(paper_name)
    google_scholar_search_box.submit()

    while 1:
        try:
            bot_check = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.ID,'gs_captcha_ccl')))
            input("Please complete the bot check and press enter to continue...")

        except:
            break

    google_scholar_main_result = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gs_res_ccl_mid"]')))
    items_in_google = google_scholar_main_result.find_elements(By.CLASS_NAME, 'gs_or')

    for item in items_in_google:
        tag = item.find_element(By.XPATH,'.//div[1]').get_attribute('class')
        if tag == 'gs_ri':
            title = item.find_element(By.XPATH, f".//div[1]/h3").text
        else:
            title = item.find_element(By.XPATH, f".//div[2]/h3").text
        if paper_name.lower() in  title.lower():
            if tag == 'gs_ri':
                cite_btn = item.find_element(By.XPATH, f".//div[1]/div[5]/a[3]")
            else:
                cite_btn = item.find_element(By.XPATH, f".//div[2]/div[5]/a[3]")
            time.sleep(1)
            cite_btn.click()

    
    while 1:
        try:
            bot_check = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.ID,'gs_captcha_ccl')))
            input("Please complete the bot check and press enter to continue...")

        except:
            break

    btn_next = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gs_nm"]/button[2]')))
    items = driver.find_elements(By.CLASS_NAME, 'gs_or')
    datass = []

    while 1:
        
        while 1:
            try:
                bot_check = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.ID,'gs_captcha_ccl')))
                input("Please complete the bot check and press enter to continue...")

            except:
                break

        for i in range(len(items)):
            tag = items[i].find_element(By.XPATH,'.//div[1]').get_attribute('class')
            if tag == 'gs_ri':
                title = items[i].find_element(By.XPATH, f".//div[1]/h3").text
                try:
                    paper_id = items[i].find_element(By.XPATH, f".//div[1]/h3/a").get_attribute("id")
                except:
                    paper_id = items[i].find_element(By.XPATH, f".//div[1]/h3/span[2]").get_attribute("id")
                try:
                    title_link = items[i].find_element(By.XPATH, f".//div[1]/h3/a").get_attribute("href")
                except:
                    title_link = ''
                pdf_link = ''
            else:
                title = items[i].find_element(By.XPATH, f".//div[2]/h3").text
                try:
                    paper_id = items[i].find_element(By.XPATH, f".//div[2]/h3/a").get_attribute("id")
                except:
                    paper_id = items[i].find_element(By.XPATH, f".//div[2]/h3/span[2]").get_attribute("id")
                try:
                    title_link = items[i].find_element(By.XPATH, f".//div[2]/h3/a").get_attribute("href")
                except:
                    title_link = ''
                pdf_link = items[i].find_element(By.XPATH, f".//div[1]/div/div/a").get_attribute("href")

            authors = get_authors(paper_id)
            datass.append([title,';'.join(authors),title_link, pdf_link,0])
            # print(title, pdf_link)
        if btn_next.get_attribute("disabled") == None:
            time.sleep(random.randint(1, max_wait))
            btn_next.click()
            btn_next = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gs_nm"]/button[2]')))
            items = driver.find_elements(By.CLASS_NAME, 'gs_or')
        else:
            break
    
    with open(f'./{paper_namex}_full_report.csv','w',encoding='utf-8',errors='ignore') as f:
        f.write('title,authors,title_link,pdf_link,save_path\n')
        f.write(',,,,for save_path 0-not download 1-download path set in code 2-system default download path\n')
        for item in datass:
            f.write(f'{item[0].replace(',','_')},{item[1]},{item[2]},{item[3]},{item[4]}\n')

    print(f'cite paper info is ready in ./{paper_namex}_full_report.csv')

    download_to_system_download_floder = [0,[]]
    success = 0
    if is_download_pdf:
        download_to_system_download_floder = [0,[]]
        success = 0
        for i in tqdm(range(len(datass)),desc='Downloading...'):
            title = datass[i][0].replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace(' ', '_')
            pdf_link = datass[i][2]
            if pdf_link != '':
                if pdf_link.endswith('.pdf'):
                    pdf_name = title + '.pdf'
                    pdf_path = os.path.join(save_path, pdf_name)
                    response = requests.get(pdf_link)
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
                    if os.path.getsize(pdf_path)/1024 > 35:
                        datass[i][-1] = 1
                        success += 1
                else:
                    try:
                        driver.get(pdf_link)
                        items = driver.find_elements(By.TAG_NAME, 'iframe')
                        if items:
                            # pdf_frame_id = items[0].get_attribute('id')
                            driver.switch_to.frame(0)
                            download_btn = driver.find_element(By.ID,'download')
                            download_btn.click()
                            download_to_system_download_floder[0]+=1
                            download_to_system_download_floder[1].append(pdf_name)
                            datass[i][-1] = 2
                            driver.switch_to.default_content()
                    except:
                        pass
            else:
                url ='https://wellesu.com/'
                driver.get(url)
                search_text_box = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="request"]')))
                search_text_box.send_keys(title)
                search_btn = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="enter"]/button')))
                search_btn.click()
                try:
                    btn_download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="buttons"]/button[2]')))
                    download_link = btn_download.get_attribute('onclick')[15:-15].replace('\\', '')
                    title = title.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace(' ', '_')
                    pdf_name = title + '.pdf'
                    pdf_path = os.path.join(save_path, pdf_name)
                    response = requests.get(download_link)
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
                    if os.path.getsize(pdf_path)/1024 > 35:
                        datass[i][2] = download_link
                        datass[i][-1] = 1
                        success += 1
                except:
                    pass
                finally:
                    driver.get(url)
                    search_text_box = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located((By.XPATH, '//*[@id="request"]')))
                
        print(f'{success} papers are downloaded to {save_path}')
        print(f'{download_to_system_download_floder[0]} papers are downloaded to system download floder')
    
        with open(f'./{paper_namex}_full_report.csv','w') as f:
            f.write('title,title_link,pdf_link,save_path\n')
            f.write(',,,,for save_path 1-download path set in code 2-system default download path\n')
            for item in datass:
                f.write(f'{item[0].replace(',','_')},{item[1]},{item[2]},{item[3]}\n')

    driver.quit()
    print(f'Find cite paper {len(datass)} , Download {success + download_to_system_download_floder[0]}' )
    print('Every thing done!')
    

    



    