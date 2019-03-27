import requests
import json
import pandas

cookie = '_T_WM=9fdf4b68b96b81997db697c6bf9a85c5; SCF=AlpahVmy9v4gxnFcFTPWI_1zUZ1zanUb4BMYZNCUTiWTg8uo4VhYhAzCqTt8j8eTv4mDs0s8rXSrvTuQt2rZjiA.; SUB=_2A25xigTiDeRhGeVO6VsQ-SjJyTmIHXVTdKyqrDV6PUJbktAKLXHlkW1NTTEYWXDkZ-mSXUI88HNP0jt3Ub_AVoMY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhiS2RxWUJdRHEyDP5aMMh15JpX5KzhUgL.Foe7eo.p1Kqfeo-2dJLoI7_sMJHLKJHXIPDLdntt; SUHB=0h1JXLbCm0gvLE; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=5e87b4; M_WEIBOCN_PARAMS=oid%3D4352605255524896%26lfid%3D4352605255524896%26luicode%3D20000174%26uicode%3D20000174'
cookie2 = 'SINAGLOBAL=9950174354986.695.1531981229855; SCF=AlpahVmy9v4gxnFcFTPWI_1zUZ1zanUb4BMYZNCUTiWTCHC00bOTvPy7yTlO1KyrOI9S_jCfEt-elmoYxuGSvmw.; SUHB=0S7CgJtAhyAAP2; ALF=1555989340; SUB=_2A25xkoYMDeRhGeVO6VsQ-SjJyTmIHXVTfCpErDV8PUJbkNAKLVLtkW1NTTEYWW_gCL6t8nmA4ZjCG5D-Ed2yks5g; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhiS2RxWUJdRHEyDP5aMMh15JpX5oz75NHD95Q0ehz4eK.cSKzfWs4DqcjTxriL9-4LUsLA9gRt; wvr=6; _s_tentry=-; Apache=959767253411.4965.1553397551959; ULV=1553397552128:11:2:1:959767253411.4965.1553397551959:1551495255016; VIP-G0=c82a2c3fe29499531400f46f7a79a2a9; UOR=,,www.google.com; WBStorage=201903251206|undefined; webim_unReadCount=%7B%22time%22%3A1553486806624%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
header = {'User-Agent': user_agent, 'Cookie': cookie2}
proxy = {
  "http": "http://127.0.0.1:1080",
  "https": "http://127.0.0.1:1080"
}

XHRUrl = 'https://m.weibo.cn/api/container/getIndex?containerid=2304136486443586_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={}'

useridList = []
userNameList = []
commentTotalList = []

WBIDList = []
n = 30
for i in range(n):
    try:
        r = requests.get(XHRUrl.format(i), headers=header)
        json_str = r.text
        dict_ = json.loads(json_str)
        for index, card in enumerate(dict_['data']['cards']):
            if dict_['data']['cards'][index]['card_type'] == 9:
                WBID = dict_['data']['cards'][index]['mblog']['id']
                # WBIDList.append(dict_['data']['cards'][index]['mblog']['id'])
                HotfollowidUrl = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(WBID, WBID)
                r = requests.get(HotfollowidUrl, headers=header)
                json_str = r.text
                json_to_dict = json.loads(json_str)
                if json_to_dict['ok'] == 1:  # 如果该条微博有评论
                    for comment in json_to_dict['data']['data']:
                        user_id = comment['user']['id']
                        user_name = comment['user']['screen_name']
                        if user_id not in useridList:
                            useridList.append(user_id)
                            userNameList.append(user_name)
                            commentTotalList.append(1)

                        else:
                            id_index = useridList.index(user_id)
                            commentTotalList[id_index] += 1

        print("\r当前进度:{:.2f}%".format((i+1)*100/n), end=' ')
    except:
        print("\r当前进度:{:.2f}%".format((i+1) * 100 / n), end=' ')
print('\n')
resultList = []
for i in range(len(useridList)):
    print(useridList[i], end='\t')  # 用户id
    print(userNameList[i].ljust(15), end='')  # 用户昵称
    print(str(commentTotalList[i]).rjust(3))  # 该用户评论次数
    result_dict = {'userid': useridList[i], 'username': userNameList[i], 'commentCount': commentTotalList[i]}
    resultList.append(result_dict)

df = pandas.DataFrame(resultList)
file_path = r'C:\Users\CY\Desktop\weiboComment.xlsx'
df.to_excel(file_path)


