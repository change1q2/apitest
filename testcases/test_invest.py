'''
作者：seak
时间：
项目：
题目：
作用：
备注：
投标
'''
import unittest
import os
import jsonpath

from common.contants import DATA_DIR
from common.handle_data import replace_data, TestData
from common.handle_request import HandleRequest
from common.myconfig import conf
from common.mylogger import my_log
from common.readexcel import ReadExcel
from library.ddt import ddt,data

data_file_path = os.path.join(DATA_DIR, "apicases.xlsx")

@ddt
class TestInvest(unittest.TestCase):
    excel = ReadExcel(data_file_path, "invest")
    cases = excel.read_data()
    http = HandleRequest()

    @data(*cases)
    def test_invest(self,case):
        #----------第一步：准备用例数据------------
        url = conf.get_str("env", "url") + case["url"]
        #请求参数
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        #请求方法
        method = case["method"]
        #请求头
        headers = eval(conf.get_str("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "token_data")
            #添加请求头中的token
        #预期结果
        expected = eval(case["expected"])
        #用例所在行
        row = case["case_id"] + 1

        #------------第二步：发送请求-------------
        res = self.http.send(url=url, json=data, method=method, headers=headers)
        result = res.json()
        if case["interface"] == "login":
            #提取用户id和token
            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token
            id = jsonpath.jsonpath(result, "$..id")[0]
            setattr(TestData, "token_data", token_data)
            setattr(TestData, "member_id", str(id))

        elif case["interface"] == "add":
            #提取项目id
            loan_id = jsonpath.jsonpath(result, "$..id")[0]
            setattr(TestData, "loan_id", str(loan_id))

        #第三步：对比结果（断言
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            #判断是否需要sql校验

        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            my_log.info("用例：{}--->执行未通过".format(case["title"]))
            print("预期结果： {}".format(expected))
            print("实际结果： {}".format(result))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例： {}--->执行通过".format(case["title"]))
