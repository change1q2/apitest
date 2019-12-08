'''
作者：seak
时间：
项目：
题目：
作用：
备注：
请求项目接口方法
'''

#首先导入requests模块

import requests

#写请求的一些信息
#请求地址
register_url = "http://api.lemonban.com/futureloan/member/register"
#请求体
data = {
    "mobile_phone":"13896375672",
    "pwd": "123456qwe",
    "type": 0,
    "reg_name":"seak"
}
#请求头
header = {
    "X-Lemonban-Media-Type":"lemonban.v3",
    "Content-Type":"application/json",
    "Authorization":"Bearer Token"
}

#发送post请求
#json类型的参数，一定使用json去传递
response = requests.post(url=register_url,json=data,headers=header)
#表单类型的参数Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# 使用data进行传递
# response = requests.post(url=register_url, data=data, headers=header)

# post请求上传文件: 使用files来上传文件
# res = requests.post(url=register_url,files=None)
# print(type(response.text))#转成文本形式会有乱码
# print(type(response.content.decode("utf8")))#将文本转化为utf8格式就没有乱码了

# json方法可以将json字符串转换成对应的python类型的数据
# print(type(response.json()))
print(response.json())
# 需要做自动化的（http/https协议）接口返回的数据99%是json类型的
