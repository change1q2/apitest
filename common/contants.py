"""
============================
作者:seak
时间:
邮件:274882401@qq.com
作用：
题目：
============================
该模块用来处理整个项目目录的路径,
项目目录路径的处理OS模块方法
"""
import os

#获取项目目录的绝对路径
res = os.path.dirname(__file__)
# print(res)#E:/py24_unittest/common获取py文件的文件夹的路劲
# BASEDIR = os.path.dirname(res)#E:/py24_unittest获取项目文件夹的路劲
# print(BASEDIR)
# # 获取当前文件的绝对路径abspath
# dir = os.path.abspath(__file__)
# print(dir)
# #print(__file__)

# 项目目录的路径 | 如果运行的时候项目目录路径出错，使用上面abspath的方式来获取当前文件的绝对路径
BASEDIR = os.path.dirname(os.path.dirname(__file__))#直接2层套，先获取py文件的文件夹的路劲
#print(BASEDIR)
#配置文件的路径
CONF_DIR = os.path.join(BASEDIR,"conf")#将项目目录路劲和文件路径进行拼接
#print(CONF_DIR)#E:/py24_unittest\conf
#日志文件路径
LOG_DIR = os.path.join(BASEDIR,"log")
#用例文件路径
DATA_DIR = os.path.join(BASEDIR,"data")
#测试报告路径
REPORT_DIR = os.path.join(BASEDIR,"report")
#测试用例代码块路径
CASE_DIR = os.path.join(BASEDIR,"testcases")
#第三方库的路劲
LIBRARY_DIR = os.path.join(BASEDIR,"libarary")

#其他文件
OTHER_DIR = os.path.join(BASEDIR,"other")

#启动文件
RUNNER_DIR = os.path.join(BASEDIR)
