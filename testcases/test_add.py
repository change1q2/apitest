'''
作者：seak
时间：
项目：
题目：
作用：
备注：
'''
import unittest
import os
import jsonpath
from common.contants import DATA_DIR
from common.myconfig import conf
from common.readexcel import ReadExcel
from library.ddt import ddt,data
from common.handle_data import replace_data, TestData
from common.handle_request import HandleRequest
from common.mylogger import my_log
from common.handle_db import HandleDB

file_path = os.path.join(DATA_DIR, "apicases.xlsx")


@ddt
class TestAdd(unittest.TestCase):
    excel = ReadExcel(file_path, "add")
    cases = excel.read_data()
    http = HandleRequest()
    db = HandleDB()

    @data(*cases)
    def test_add(self, case):
        #--------------第一步：准备用例数据-----------------
        #1.获取url
        url = conf.get_str("env", "url") + case["url"]
        #2.获取数据
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        #3.获取请求头
        headers = eval(conf.get_str("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "token_data")
        #预期结果
        expected = eval(case["expected"])
        #请求方法
        method = case["method"]
        print(method,type(method))
        #用例所在行
        row = case["case_id"] + 1

        #----------------第二步：发送请求---------------------
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            s_loan_num = self.db.count(sql)
        res = self.http.send(url=url, method=method, json=data, headers=headers)
        json_data = res.json()
        if case["interface"] == "login":
            # 如果是登录的用例，提取对应的token,和用户id,保存为TestData这个类的类属性，用来给后面的用例替换
            token_type = jsonpath.jsonpath(json_data, "$..token_type")[0]
            token = jsonpath.jsonpath(json_data, "$..token")[0]
            token_data = token_type + " " + token
            setattr(TestData, "token_data", token_data)
            id = jsonpath.jsonpath(json_data, "$..id")[0]
            setattr(TestData, "admin_member_id", str(id))

        '''补充知识：
               setattr() 函数对应函数 getattr()，用于设置属性值，该属性不一定是存在的。
               setattr(object, name, value),有就用新的属性值替换掉原来的，没有就自动创建一个属性值
               >>>class A(object):
               >>> bar = 1
               >>> a = A()
               >>> getattr(a, 'bar')          # 获取属性 bar 值
                    1
               >>> setattr(a, 'bar', 5)       # 设置属性 bar 值
               >>> a.bar
                    5
       '''
        #----------------第三步：断言-------------------------------
        try:
            self.assertEqual(expected["code"],json_data["code"])
            self.assertEqual(expected["msg"],json_data["msg"])
            # 判断是否需要sql校验
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                end_loan_num = self.db.count(sql)
                self.assertEqual(end_loan_num-s_loan_num,1)

        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            my_log.info("用例：{}--->执行未通过".format(case["title"]))
            print("预取结果：{}".format(expected))
            print("实际结果：{}".format(json_data))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例：{}--->执行通过".format(case["title"]))
