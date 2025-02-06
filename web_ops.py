import requests
from bs4 import BeautifulSoup
import re
import random

def decode_cite_text(text):
    author_pattern = re.compile(r'author\s*=\s*\{(.*?)\}', re.DOTALL)
    match = author_pattern.search(text)
    authors = []
    if match:
        authors = match.group(1).split(' and ')
        authors = [author.strip().replace(' ','').replace(',',' ') for author in authors]
    return authors

def get_random_ua():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.54',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.2 Safari/605.1.15',

    ]
    return random.choice(user_agents)

def get_random_cookie():
    cookies = [
        "__cfduid=d25efa21dde4a114e7dd96b477e0aba381531100939; FR24ID=0l69ten5b83uoqjui6ufipkbb14hb2li3pd8hcfqtar0uptt84r0; __utma=177865842.2011292994.1531100944.1531100944.1531100944.1; __utmc=177865842; __utmz=177865842.1531100944.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=177865842.1.10.1531100944",
        "__Secure-ENID=21.SE=AahQx5gYvJ-uxVfRpFaLXAi30qm23F3UVYSYaVHf2dhSeAA42kOONEoajw6hlPGetOS-PXHKSwCx3dwJls0S7vLQTE47CjYEs3p_SOmxbR_4rod80TkGV8HXWyvSR2ye4t3T4b_tMZURHU1zvcgrjlM9ZHjDPmrwbNxvRCQ7g5vA2bIyiFlV2mfIAwPaQfc9RwMYf2AsWgQ8n71QEAnYfzTCNE9144tafZwfLa8eIafyhXfeK7WnoiKp9acpzoxLGwTdSrFm2urUthRXp0EWJooc9kE2Jfoj0Ecjm20; HSID=AEmGbzz4ZvrmDfvnU; SSID=Atrpx2xqPy1sbd23O; APISID=585xvnk1N5J95HbV/Ac9xiINqoXJptMa85; SAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; __Secure-1PAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; __Secure-3PAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; GSP=A=KhlVtQ:CPTS=1732600504:LM=1732600504:S=o5pGDcQSM1TCFVC8; SID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASly_nDKBf1YUcCE0QigknGAACgYKAbkSARESFQHGX2Mi5TX6r0WWWf3EX9Z6Ku78mRoVAUF8yKqXU1TTnDuZzRmd7mvGCoLE0076; __Secure-1PSID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASjz77ReXb4rwvz6Sf1QS5WgACgYKAVQSARESFQHGX2MipDJ0Q8El9Bo1ZVPUanGeMhoVAUF8yKpj1sF7MedsYCsWKbalHHSG0076; __Secure-3PSID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASElRIm5qtI1Fm23QrYowHcgACgYKAdISARESFQHGX2MiNImDRPQDhuTDvnqdG3zPNxoVAUF8yKqohZnrp6GtEIYk6cfWLiLS0076; SEARCH_SAMESITE=CgQIgZ0B; AEC=AZ6Zc-VoPElF8Q8p3o7M5xHNX2TweC5SKWn73RHXEEOPFnWaUJEgN3makA; __Secure-1PSIDTS=sidts-CjIBmiPuTfNCC7sODJGt0tIAUTWmNT1g6qz3ArW4EhUkI2Z6BGxkSdtMzPQObCnwE1498hAA; __Secure-3PSIDTS=sidts-CjIBmiPuTfNCC7sODJGt0tIAUTWmNT1g6qz3ArW4EhUkI2Z6BGxkSdtMzPQObCnwE1498hAA; NID=520=DYXabZX9E0Owkf8qWSZReqfSfmmLd2_58HAEWWV90HfpISvMrJi7IFRcPp7lvupyyaZ-lcJm03_Iqk0ZvWm8x-oKBmHskfrx8uSfxal1eee6ovRGKU553U3GXYnCaxMt7ZCAXb03HUE78LUFRp7WRrcNkUMoSDGVuwUrcq4r91AP-JMrySZD8a_w3lDV63ZeAhK3qsvBV9zl3X09PFEhc1c41UhKizk-Lg00MWgUS_ECIxPjCrjUnJjckjdYSlqQd05eBwtyP-IAz6H4ko2YzrqHS7vOx9983YGp412r7czdAMWI7L2utNl2YUE1qEEAFaeVrXa_Krt9O6pfDJXMGtjf51BunBsbDWwE61ArrJqibHscu0dzGvv_6xpdfxka6ChqgVz1d6qMTzArytDwgxlE2FOrPY8QXwsKwKovQh9tz-PCz6x0pb8LSzkjwfntRwE0IUjQB55cEs1ULhvWxgW2KUqD3XXP15NJe2tv-sdXfO5wO_BiQKtPb5O1TxCI-uu6kJjKvAnaeCXghDov4IoxAkLPTClji5d5zw9t0gNkvogxw5mAMSVil_FfPHltVd8IUb9Xiea-J3uZG4pweuBaVT9QpdufGT7tNX-3--9EHh0EqDCThNVQm5AadZRtzSt_2z__3lRLwgbbIPQ3WUoqdJBDoULmIUpQnaDwdKDR8KfEHSw717sTwMgbjkn1cx390ta9cWqxYIsm2UNKjLpA0-c4bVa3oZLPttX3eN3rdJz5499zxEfCrjl9SwehEmicRf1ReZjG5EWwIXK_8HOJ_LHIHyoMzrW06--tV6dRRqAbyx3kqd8rklrLCYgsiro1Wkl0IehfN9bS9kGSYQ; SIDCC=AKEyXzWg6Ay7crhnfb9pZWKRbbfOPfj63wk-hcCv6k-L9iWWt2-rwjsuen9M8flj-N6j0evpDl4; __Secure-1PSIDCC=AKEyXzW_USqd9nsX7by10zsepLJIGIl3a6qkKCbMeQ98bTk37YKDtDIX7CFxKW9ga3eIaxDzzQ; __Secure-3PSIDCC=AKEyXzVnxY9_C1gzcHHcriOx96Yc5ye5ll10DuJHOJXh51Z4kisHnKWDBQCc-JYZvrB16p0M3cM",
        

    ]
    return random.choice(cookies)


def get_authors(paper_id,page,i,is_debug=False):
    

    if paper_id == '':
        return []
    headers = {
            "User-Agent": get_random_ua(),
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cache-control": "max-age=0",
            # "cookie": get_random_cookie()
            }
    
    if page == 0:
        id = f'{i}'
    else:
        id = f'{page}{i}'

    url = f'https://scholar.google.com/scholar?q=info:{paper_id}:scholar.google.com/&output=cite&scirp={id}&hl=en'

    try:
        # time.sleep(random.randint(1, 5))
        res = requests.get(url, headers=headers, timeout=10)
        
        if is_debug:
            with open('./debug.log','a') as f:
                f.write(str(res.status_code)+'\n')
                f.write(str(res.text)+'\n')
                f.write('\n')

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            bibtex = soup.find('a', string='BibTeX')
            if bibtex:
                bibtex_link = bibtex['href']
                res = requests.get(bibtex_link, headers=headers, timeout=10)
                if res.status_code == 200:
                    if is_debug:
                        with open('./debug.log','a') as f:
                            f.write(str(res.status_code)+'\n')
                            f.write(str(res.text)+'\n')
                            f.write('\n')
                    aths = decode_cite_text(res.text)
                    if is_debug:
                        with open('./debug.log','a') as f:
                            f.write(';'.join(aths)+'\n')
                            f.write('\n')
                    return aths
            else:
                return []
    except :
        pass
    return []

def get_authors_by_bibtex(link,is_debug=False):

    headers = {
            "User-Agent": get_random_ua(),
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cache-control": "max-age=0",
            # "cookie": "__cfduid=d25efa21dde4a114e7dd96b477e0aba381531100939; FR24ID=0l69ten5b83uoqjui6ufipkbb14hb2li3pd8hcfqtar0uptt84r0; __utma=177865842.2011292994.1531100944.1531100944.1531100944.1; __utmc=177865842; __utmz=177865842.1531100944.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=177865842.1.10.1531100944"
            # "cookie": "__Secure-ENID=21.SE=AahQx5gYvJ-uxVfRpFaLXAi30qm23F3UVYSYaVHf2dhSeAA42kOONEoajw6hlPGetOS-PXHKSwCx3dwJls0S7vLQTE47CjYEs3p_SOmxbR_4rod80TkGV8HXWyvSR2ye4t3T4b_tMZURHU1zvcgrjlM9ZHjDPmrwbNxvRCQ7g5vA2bIyiFlV2mfIAwPaQfc9RwMYf2AsWgQ8n71QEAnYfzTCNE9144tafZwfLa8eIafyhXfeK7WnoiKp9acpzoxLGwTdSrFm2urUthRXp0EWJooc9kE2Jfoj0Ecjm20; HSID=AEmGbzz4ZvrmDfvnU; SSID=Atrpx2xqPy1sbd23O; APISID=585xvnk1N5J95HbV/Ac9xiINqoXJptMa85; SAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; __Secure-1PAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; __Secure-3PAPISID=RKT6gZxPQybCIhyV/AGA2VMrM1eNAdKTxp; GSP=A=KhlVtQ:CPTS=1732600504:LM=1732600504:S=o5pGDcQSM1TCFVC8; SID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASly_nDKBf1YUcCE0QigknGAACgYKAbkSARESFQHGX2Mi5TX6r0WWWf3EX9Z6Ku78mRoVAUF8yKqXU1TTnDuZzRmd7mvGCoLE0076; __Secure-1PSID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASjz77ReXb4rwvz6Sf1QS5WgACgYKAVQSARESFQHGX2MipDJ0Q8El9Bo1ZVPUanGeMhoVAUF8yKpj1sF7MedsYCsWKbalHHSG0076; __Secure-3PSID=g.a000rwiClXYbQLfoAI4PS0lXVqKoBT5NX3MqEajXtcP_bF1LjzASElRIm5qtI1Fm23QrYowHcgACgYKAdISARESFQHGX2MiNImDRPQDhuTDvnqdG3zPNxoVAUF8yKqohZnrp6GtEIYk6cfWLiLS0076; SEARCH_SAMESITE=CgQIgZ0B; AEC=AZ6Zc-VoPElF8Q8p3o7M5xHNX2TweC5SKWn73RHXEEOPFnWaUJEgN3makA; __Secure-1PSIDTS=sidts-CjIBmiPuTfNCC7sODJGt0tIAUTWmNT1g6qz3ArW4EhUkI2Z6BGxkSdtMzPQObCnwE1498hAA; __Secure-3PSIDTS=sidts-CjIBmiPuTfNCC7sODJGt0tIAUTWmNT1g6qz3ArW4EhUkI2Z6BGxkSdtMzPQObCnwE1498hAA; NID=520=DYXabZX9E0Owkf8qWSZReqfSfmmLd2_58HAEWWV90HfpISvMrJi7IFRcPp7lvupyyaZ-lcJm03_Iqk0ZvWm8x-oKBmHskfrx8uSfxal1eee6ovRGKU553U3GXYnCaxMt7ZCAXb03HUE78LUFRp7WRrcNkUMoSDGVuwUrcq4r91AP-JMrySZD8a_w3lDV63ZeAhK3qsvBV9zl3X09PFEhc1c41UhKizk-Lg00MWgUS_ECIxPjCrjUnJjckjdYSlqQd05eBwtyP-IAz6H4ko2YzrqHS7vOx9983YGp412r7czdAMWI7L2utNl2YUE1qEEAFaeVrXa_Krt9O6pfDJXMGtjf51BunBsbDWwE61ArrJqibHscu0dzGvv_6xpdfxka6ChqgVz1d6qMTzArytDwgxlE2FOrPY8QXwsKwKovQh9tz-PCz6x0pb8LSzkjwfntRwE0IUjQB55cEs1ULhvWxgW2KUqD3XXP15NJe2tv-sdXfO5wO_BiQKtPb5O1TxCI-uu6kJjKvAnaeCXghDov4IoxAkLPTClji5d5zw9t0gNkvogxw5mAMSVil_FfPHltVd8IUb9Xiea-J3uZG4pweuBaVT9QpdufGT7tNX-3--9EHh0EqDCThNVQm5AadZRtzSt_2z__3lRLwgbbIPQ3WUoqdJBDoULmIUpQnaDwdKDR8KfEHSw717sTwMgbjkn1cx390ta9cWqxYIsm2UNKjLpA0-c4bVa3oZLPttX3eN3rdJz5499zxEfCrjl9SwehEmicRf1ReZjG5EWwIXK_8HOJ_LHIHyoMzrW06--tV6dRRqAbyx3kqd8rklrLCYgsiro1Wkl0IehfN9bS9kGSYQ; SIDCC=AKEyXzWg6Ay7crhnfb9pZWKRbbfOPfj63wk-hcCv6k-L9iWWt2-rwjsuen9M8flj-N6j0evpDl4; __Secure-1PSIDCC=AKEyXzW_USqd9nsX7by10zsepLJIGIl3a6qkKCbMeQ98bTk37YKDtDIX7CFxKW9ga3eIaxDzzQ; __Secure-3PSIDCC=AKEyXzVnxY9_C1gzcHHcriOx96Yc5ye5ll10DuJHOJXh51Z4kisHnKWDBQCc-JYZvrB16p0M3cM"
        }
    try:
        res = requests.get(link, headers=headers, timeout=10)
        if is_debug:
            with open('./debug.log','a') as f:
                f.write(str(res.status_code)+'\n')
                f.write(str(res.text)+'\n')
                f.write('\n')
        aths = decode_cite_text(res.text)
        if is_debug:
            with open('./debug.log','a') as f:
                f.write(';'.join(aths)+'\n')
                f.write('\n')
        return aths
    except:
          pass
    return []                 

def get_authors_proxy(paper_id,is_debug=False):
    
    if paper_id == '':
        return []
    headers = {
            "User-Agent": get_random_ua(),
            "accept-language": "zh-CN,zh;q=0.9",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cache-control": "max-age=0",
            # "cookie": get_random_cookie()
            }
    
    

    
    url = f'https://scholar.google.com/scholar?q=info:{paper_id}:scholar.google.com/&output=cite&scirp=0&hl=en'

    try:

        # authkey = 'J2P4MW5D'
        # authpwd = '4DF1563E29B1'
        # exxx = f"http://{authkey}:{authpwd}:A990100@overseas-us.tunnel.qg.net:19862"

        proxyUrl = "http://%(user)s:%(password)s:A%(area)d@%(server)s" % {
            "user": 'JRZ7HQ48',
            "password": 'A7235B141A52',
            "server": 'overseas-us.tunnel.qg.net:10660',
            "area": 990100,
        }
        proxies = {
            "http": proxyUrl,
            "https": proxyUrl,
        }
        
        # print(exxx)

        res = requests.get(url, headers=headers, proxies=proxies,timeout=10)

        # curl_command = ["curl", url , '-H' , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0' , '-x' , exxx]
        # result = subprocess.run(curl_command, capture_output=True, text=True)

        if is_debug:
            with open('./debug.log','a') as f:
                f.write(str(res.status_code)+'\n')
                f.write(str(res.text)+'\n')
                f.write('\n')

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            bibtex_link = soup.find('a', string='BibTeX')['href']
            # exxx = f"http://{authkey}:{authpwd}@overseas-us.tunnel.qg.net:19862 {bibtex_link}"
            res = requests.get(bibtex_link, headers=headers, proxies=proxies, timeout=10)
            # curl_command = ["curl", bibtex_link , '-H' , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0' , '-x' , exxx]
            # result = subprocess.run(curl_command, capture_output=True, text=True)
            if res.status_code == 200:
                if is_debug:
                    with open('./debug.log','a') as f:
                        # f.write(str(res.status_code)+'\n')
                        f.write(str(res.text)+'\n')
                        f.write('\n')
                aths = decode_cite_text(res.text)
                if is_debug:
                    with open('./debug.log','a') as f:
                        f.write(';'.join(aths)+'\n')
                        f.write('\n')
                return aths
            else:
                return []
        else:
            return []
    except Exception as e:
        pass
        # print(e)
    return []

def safe_bot_request_proxy(url,is_debug=False):
    headers = {
            "User-Agent": get_random_ua(),
            "accept-language": "zh-CN,zh;q=0.9",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cache-control": "max-age=0",
            # "cookie": get_random_cookie()
            }

    proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
            "user": 'JRZ7HQ48',
            "password": 'A7235B141A52',
            "server": 'overseas-us.tunnel.qg.net:10660',
            
        }
    proxies = {
            "http": proxyUrl,
            "https": proxyUrl,
        }
    
    bot_count = 0
    while 1:
        # time.sleep(random.randint(3,8))
        res = requests.get(url, headers=headers, proxies=proxies,timeout=10)
        if is_debug:
            with open('debug.log','a') as f:
                f.write(str(res.status_code)+'\n')
                if not res.status_code == 200:
                    f.write(str(res.text)+'\n')
                f.write('\n')
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            bot_check = soup.find_all("div", id="gs_captcha_ccl")
            if len(bot_check) == 0:
                return res
        bot_count+=1
        # waitTime = random.randint(2,5)*10
        # print(f'find bot verify , wait for {waitTime} s')
        # time.sleep(waitTime)
        # if bot_count > 10:
        #     print("Error with loading web page")
        #     raise ValueError("Webpage Error, for most reason maybe banned by google!")


def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip', timeout=5)
        response.raise_for_status()
        data = response.json()
        ip_str = data.get('origin', '')
        ips = ip_str.split(', ')
        return ips[0] if ips else None
    except Exception as e:
        print(f"Get IP failed: {e}")
        return None

def get_ip_country(ip):
    try:
        response = requests.get(
            f'http://ip-api.com/json/{ip}?fields=status,countryCode',
            headers={'User-Agent': 'python-requests/ip-checker'},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            return data.get('countryCode')
        else:
            print(f"query failed: {data.get('message')}")
            return None
    except Exception as e:
        print(f"Nation code query failed: {e}")
        return None

def checkProxyUsingArea():
    public_ip = get_public_ip()
    if not public_ip:
        print("Unknow IP adderss")
        exit(1)
    
    country_code = get_ip_country(public_ip)
    if not country_code:
        print("Unknkw IP location")
        exit(1)
    
    if country_code.upper() == 'CN':
        print("Please using other server outside China")
        exit(1)