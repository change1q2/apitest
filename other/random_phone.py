"""
============================
Author:柠檬班-木森
Time:2019/12/4
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import random


def random_phone():
    """生成随机的手机号码"""
    phone = "133"
    for i in range(8):
        phone += str(random.randint(0, 9))

    return phone

# 随机生成手机号码
phone = random_phone()


str1 = '{"mobile_phone":"#phone#","pwd":"12345678","type":1,"reg_name":"34254sdfs"}'

# 使用成员运算符判断是否有需要替换的手机号码
if "#phone#" in str1:
    str2 = str1.replace("#phone#",phone)

    print(str2)