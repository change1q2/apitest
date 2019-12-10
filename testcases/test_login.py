"""
============================
作者:seak
时间:
邮件:274882401@qq.com
作用：
题目：
============================
"""
import unittest
import os
from common.readexcel import ReadExcel
from common.contants import DATA_DIR
from library.ddt import ddt, data
from common.myconfig import conf
from common.handle_request import HandleRequest
from common.mylogger import my_log

data_file_path = os.path.join(DATA_DIR, "apicases.xlsx")


@ddt
class TestLogin(unittest.TestCase):
    excel = ReadExcel(data_file_path, "login")
    cases = excel.read_data()
    http = HandleRequest()

    @data(*cases)
    def test_login(self, case):
        # ------第一步：准备用例数据------------
        # 拼接完整的接口地址
        url = conf.get_str("env", "url") + case["url"]
        # 请求的方法
        method = case["method"]
        # 请求参数
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get_str("env", "headers"))
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在表单的中所在行
        row = case["case_id"]+1

        # ------第二步：发送请求到接口，获取实际结果--------
        response = self.http.send(url=url, method=method, json=data, headers=headers)
        result = response.json()

        # -------第三步：比对预期结果和实际结果-----
        try:
            # 业务码断言
            self.assertEqual(expected["code"], result["code"])
            # msg断言
            self.assertEqual((expected["msg"]), result["msg"])
        except AssertionError as e:
            # excel中回写结果
            self.excel.write_data(row=row,column=8,value="未通过")
            # 记录apicases.xlsx日志
            my_log.info("用例：{}--->执行未通过".format(case["title"]))
            my_log.error(e)
            # 报告中打印预期和实际结果
            print("预取结果：{}".format(expected))
            print("实际结果：{}".format(result))
            raise e
        else:
            # excel中回写结果
            self.excel.write_data(row=row, column=8, value="通过")
            # 记录日志
            my_log.info("用例：{}--->执行通过".format(case["title"]))









