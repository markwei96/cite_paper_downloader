import requests
from bs4 import BeautifulSoup
import re
import json
import time

def decode_cite_text(text):
    author_pattern = re.compile(r'author\s*=\s*\{(.*?)\}', re.DOTALL)
    match = author_pattern.search(text)
    authors = []
    if match:
        authors = match.group(1).split(' and ')
        authors = [author.strip().replace(' ','').replace(',',' ') for author in authors]
    return authors


def get_authors(paper_id):
    if paper_id == '':
        return []
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
    
    url = f'https://scholar.google.com/scholar?q=info:{paper_id}:scholar.google.com/&output=cite&scirp=0&hl=en'

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        bibtex_link = soup.find('a', string='BibTeX')['href']
        res = requests.get(bibtex_link, headers=headers, timeout=10)
        aths = decode_cite_text(res.text)
        return aths                   
    except :
        pass
    return []


