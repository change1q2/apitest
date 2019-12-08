"""
============================
作者:seak
时间:
邮件:274882401@qq.com
作用：
题目：继承的理解
============================
"""


class Person(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.weight = 'weight'

    def talk(self):
        print("person is talking....")


class Chinese(Person):

    def __init__(self, name, age, language):  # 先继承，在重构
        #Person.__init__(self, name, age)  # 继承父类的构造方法，也可以写成：super(Chinese,self).__init__(name,age)
        super(Chinese, self).__init__(name, age)
        self.language = language  # 定义类的本身属性

    def walk(self):
        print('is walking...')


class American(Person):
    pass


c = Chinese('bigberg', 22, 'Chinese')