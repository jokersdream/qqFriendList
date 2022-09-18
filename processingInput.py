import json
import os
import requests

downloadPath = 'output'  # {downloadPath/xxx}
if not os.path.exists(downloadPath):
    os.mkdir(downloadPath)


def saveImg(uin: int):
    url = "http://qlogo4.store.qq.com/qzone/" + str(uin) + "/" + str(uin) + "/30"
    file = downloadPath + '/Pic/' + str(uin) + '.png'
    r = requests.get(url,  stream=True)
    if r.status_code == 200:
        open(file, 'wb').write(r.content)  # 将内容写入图片
        print('download', url)
    else:
        print('error! uin =', uin)
    r.close()


with open('input.json', 'r', encoding='utf-8') as fin:
    data = json.load(fin)
    qFriend = data['items']
    qGroup = data['gpnames']
    fin.close()


qGroupMap = dict()
for group in qGroup:
    qGroupMap[group['gpid']] = group['gpname']
for friend in qFriend:
    friend['gpname'] = qGroupMap[friend['groupid']]
    saveImg(friend['uin'])
    del friend['groupid']
    del friend['yellow']
    del friend['online']
    del friend['v6']

with open('output/output.json', 'w', encoding='utf-8') as fout:
    json.dump(qFriend, fout, indent=2, ensure_ascii=False)
    fout.close()
