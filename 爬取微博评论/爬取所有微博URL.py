import requests
import json
import pandas

XHRUrl = 'https://m.weibo.cn/api/container/getIndex?containerid=2304136486443586_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={}'

cookie = '_T_WM=9fdf4b68b96b81997db697c6bf9a85c5; SCF=AlpahVmy9v4gxnFcFTPWI_1zUZ1zanUb4BMYZNCUTiWTg8uo4VhYhAzCqTt8j8eTv4mDs0s8rXSrvTuQt2rZjiA.; SUB=_2A25xigTiDeRhGeVO6VsQ-SjJyTmIHXVTdKyqrDV6PUJbktAKLXHlkW1NTTEYWXDkZ-mSXUI88HNP0jt3Ub_AVoMY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhiS2RxWUJdRHEyDP5aMMh15JpX5KzhUgL.Foe7eo.p1Kqfeo-2dJLoI7_sMJHLKJHXIPDLdntt; SUHB=0h1JXLbCm0gvLE; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=5e87b4; M_WEIBOCN_PARAMS=oid%3D4352605255524896%26lfid%3D4352605255524896%26luicode%3D20000174%26uicode%3D20000174'
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
header = {'User-Agent': user_agent, 'Cookie': cookie}
WBIDList = []
n = 18
for i in range(n):
    try:
        #i = 1
        r = requests.get(XHRUrl.format(i), headers=header)
        #print(r.text)
        json_str = r.text
        #print(type(json_str))
        dict_ = json.loads(json_str)
        #print(dict_)
        #print(len(dict_['data']['cards']))
        for index, card in enumerate(dict_['data']['cards']):
            #if dict_['data']['cards'][0]['card_type'] == '9':
            #print(type(dict_['data']['cards']))
            if dict_['data']['cards'][index]['card_type'] == 9:
                print(dict_['data']['cards'][index]['mblog']['id'])
                WBIDList.append(dict_['data']['cards'][index]['mblog']['id'])
        print("\r当前进度:{:.2f}%".format(i*100/n), end=' ')
    except:
        print("\r当前进度:{:.2f}%".format(i * 100 / n), end=' ')
print(len(WBIDList))
print(WBIDList)
df = pandas.DataFrame(WBIDList)
file_path = r'C:\Users\CY\Desktop\WBID.csv'
df.to_csv(file_path, mode='a')

