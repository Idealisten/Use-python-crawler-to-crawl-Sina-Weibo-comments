import requests
import json

WBUrl = 'https://m.weibo.cn/detail/4352605255524896'
WBID = WBUrl.split('/')[-1]
print(WBID)
HotfollowidUrl = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(WBID,WBID)
print(HotfollowidUrl)
cookie = '_T_WM=9fdf4b68b96b81997db697c6bf9a85c5; SCF=AlpahVmy9v4gxnFcFTPWI_1zUZ1zanUb4BMYZNCUTiWTg8uo4VhYhAzCqTt8j8eTv4mDs0s8rXSrvTuQt2rZjiA.; SUB=_2A25xigTiDeRhGeVO6VsQ-SjJyTmIHXVTdKyqrDV6PUJbktAKLXHlkW1NTTEYWXDkZ-mSXUI88HNP0jt3Ub_AVoMY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhiS2RxWUJdRHEyDP5aMMh15JpX5KzhUgL.Foe7eo.p1Kqfeo-2dJLoI7_sMJHLKJHXIPDLdntt; SUHB=0h1JXLbCm0gvLE; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=5e87b4; M_WEIBOCN_PARAMS=oid%3D4352605255524896%26lfid%3D4352605255524896%26luicode%3D20000174%26uicode%3D20000174'
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
header = {'User-Agent': user_agent, 'Cookie': cookie}
useridList = []
userNameList = []
commentTotalList = []

r = requests.get(HotfollowidUrl, headers=header)
json_str = r.text
json_to_dict = json.loads(json_str)

if json_to_dict['ok'] == 1:
    #print(json_to_dict['data']['data'])
    for comment in json_to_dict['data']['data']:
        #print(type(comment))
        #comment_text = comment['text']
        user_id = comment['user']['id']
        user_name = comment['user']['screen_name']
        if user_id not in useridList:
            useridList.append(user_id)
            userNameList.append(user_name)
            commentTotalList.append(1)

        else:
            id_index = useridList.index(user_id)
            commentTotalList[id_index] += 1
    for i in range(len(useridList)):
        print(useridList[i])  # 用户id
        print(userNameList[i])  # 用户昵称
        print(commentTotalList[i])  # 该用户评论次数





