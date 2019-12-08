<<<<<<< HEAD
from configparser import ConfigParser


class MyConf(ConfigParser):

    def __init__(self, filename, encoding):
        super().__init__()
        self.filename = filename
        self.encoding = encoding
#读取数据
    def read_(self):
        return super().read(filenames=self.filename, encoding=self.encoding)

    def get(self, section, option):
        return super().get(section, option)

    def write(self, section, option, value):
        super().set(section, option, value)

"""
这个类封装没讲完，可以先不写 下节课讲完再写


"""
=======
"""
============================
作者:seak
时间:
邮件:274882401@qq.com
作用：
题目：
============================
"""
import os
from configparser import ConfigParser

#使用继承的方法，会方便很多，不用一个个定义
#定义一个MyConf2类继承ConfigParser方法    继承格式：  类名.(继承的类名)
from common.contants import CONF_DIR


class MyConf:

    def __init__(self, filename, encoding="utf8"):
        """

        :param filename: 配置文件名
        :param encoding: 文件编码方式
        """
        self.filename = filename
        self.encoding = encoding
        # 创建一个文件解析对象，设为对象的conf
        self.conf = ConfigParser()
        # 使用解析器对象，加载配置文件中的内容
        self.conf.read(filename, encoding)

    def get_str(self, section, option):
        """
        读取数据
        :param section: 配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.get(section, option)

    def get_int(self, section, option):
        """
        读取数据
        :param section: 配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.getint(section, option)

    def get_float(self, section, option):
        """
        读取数据
        :param section: 配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.getfloat(section, option)

    def get_bool(self, section, option):
        """
        读取数据
        :param section: 配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.getboolean(section, option)

    def write_data(self, section, option, value):
        """
        写入数据
        :param section: 配置块
        :param option: 配置项
        :param value:  配置项对应的值
        """
        # 写入内容
        self.conf.set(section, option, value)
        # 保存到文件
        self.conf.write(open(self.filename, "w", encoding=self.encoding))


# 获取配置文件的绝对路径
conf_path = os.path.join(CONF_DIR, "conf.ini")
conf = MyConf(conf_path)

>>>>>>> company
