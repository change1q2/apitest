"""
============================
作者:seak
时间:
邮件:274882401@qq.com
作用：
题目：
============================
"""

"""
封装的目的：
    1、可以隐藏内部细节，对外提供公共访问方式。

​	2、提高安全性，提高代码的复用性。


封装的需求：
    发送post请求，，发送get请求，发送patch请求，
    代码中如何做到不同请求方式的接口去发送不同的请求
    加判断
"""

import requests

#定义一个请求类叫HandleRequest
#methon请求方式 get,post,put,patch
#get请求可能使用的是parma，拼接在url后面。用None可以表示不传的使用默认为None，传的话就使用传的值
class HandleRequest:
    def send(self,url,method,params=None,data=None,json=None,headers=None):
        #有时后会将请求方式大写，可以默认转化为小写yonglower
        method = method.lower()
        if method == "post":
            return requests.post(url=url,json=json,data=data,headers=headers)
        elif method == "patch":
            return requests.patch(url=url,json=json,data=data,headers=headers)
        elif method == "get":
            return requests.get(url=url,params=params)


"""使用session鉴权的接口，使用这个类类发送请求"""
class HandleSessionRequest:
    #__init__方法中，只有一个self，指的是实例的本身，可以是一个空的结构，
        # 比如学生的表，当学生还没有进行考试时，他已经有了学生的姓名和成绩，当新的数据来的时候，可以直接添加进来。这个可以很方便的进行
    #def __init__(self, name, score):直接传入参数实列化，必须要传值不能为空
    def __init__(self):
        self.se = requests.session()

    def send(self,url,method,params=None,data=None,json=None,headers=None):
        #讲求请方法转化为小写lower
        method = method.lower()
        if method == "post":
            return requests.posts(url=url,json=json,data=data)
        elif method == "patch":
            return requests.patch(url=url,json=json,data=data,headers=headers)
        elif method == "get":
            return self.se.get(url=url, params=params)


#在 if __name__ == '__main__': 下的代码只有在文件作为脚本直接执行才会被执行，而 import 到其他脚本中是不会被执行的
if __name__ == '__main__':
    #登陆接口
    login_url = "http://api.lemonban.com/futureloan/member/login"

    #登陆的参数
    login_data = {
        "mobile_phone": "15867554893",
        "pwd": "123456qwe",
    }

    #登陆的请求头
    header = {
        "X-Lemonban-Media-Type": "lemonban.v2",
        "Content-Type": "application/json"
    }




    #接受定义的类，给其他代码调用使用
    http = HandleRequest()
    res = http.send(url=login_url,method="post",json=login_data,headers=header)
    print(res.json())


