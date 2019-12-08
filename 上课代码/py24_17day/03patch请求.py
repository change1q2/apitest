'''
作者：seak
时间：
项目：
题目：
作用：
备注：
'''

import requests

header = {
    "X-Lemonban-Media-Type": "lemonban.v1",
    "Content-Type": "application/json"
}
data = {
    "member_id": 45504,
    "reg_name": "小柠檬888"
}

res = requests.patch(url="http://api.lemonban.com/futureloan/member/update", json=data, headers=header)
print(res.json())
