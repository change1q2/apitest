'''
作者：seak
时间：
项目：
题目：
作用：
备注：

充值的测试,
几个问题：
1.如何做token提取
方式一：
setupclass中提取的用户id和token,如何在用例方法中使用？
1、设为全局变量

2、保存为类属性

3、写入到配置文件

4、保存在临时变量的类中（后面会讲的，先不要去研究）
classmethod 修饰符对应的函数不需要实例化，
不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，
可以来调用类的属性，类的方法，实例化对象等。
'''
import decimal
import os
import unittest
import jsonpath
from common.contants import DATA_DIR
from common.handle_db import HandleDB
from common.handle_request import HandleRequest
from common.myconfig import conf
from common.mylogger import my_log
from common.readexcel import ReadExcel
from library.ddt import ddt,data
data_file_path = os.path.join(DATA_DIR,"apicases.xlsx")

@ddt
class TestRecharge(unittest.TestCase):
    excel = ReadExcel(data_file_path,"recharge")
    cases = excel.read_data()
    http = HandleRequest()

    @classmethod
    def setUpClass(cls):# cls : 表示没被实例化的类本身
        #创建操作数据库的对象
        cls.db = HandleDB()
        # 登录，获取用户的id以及鉴权需要用到的token
        url = conf.get_str("env","url") + "/member/login"
        data = {
            "mobile_phone": conf.get_str("test_data","user"),
            "pwd":conf.get_str("test_data","pwd")
        }
        headers = eval(conf.get_str("env","headers"))
        response = cls.http.send(url=url,method="post",json=data,headers=headers)
        json_data = response.json()

        # -------登录之后，从响应结果中提取用户id和token-------------
        #1、提取用户id
        cls.member_id = jsonpath.jsonpath(json_data,"$..id")[0]
        #2、提取token
        token_type = jsonpath.jsonpath(json_data,"$..token_type")[0]
        token = jsonpath.jsonpath(json_data,"$..token")[0]
        cls.token_data = token_type + " " + token

    @data(*cases)
    def test_recharge(self,case):
        # ------第一步：准备用例数据------------
        # 拼接完整的接口地址
        url = conf.get_str("env", "url") + case["url"]
        # 请求的方法
        method = case["method"]
        #请求参数
        #判断是否有用户id需要替换
        if "#member_id#" in case["data"]:
            #进行替换
            case["data"] = case["data"].replace("#member_id#",str(self.member_id))

        data = eval(case["data"])

        #请求头
        headers = eval(conf.get_str("env","headers"))
        headers["Authorization"] = self.token_data

        #预期结果
        expected = eval(case["expected"])
        #改用例在表单中的所在行
        row = case["case_id"] + 1

    # ------第二步：发送请求到接口，获取实际结果--------
        #1.首先进行数据库的校验
        if case["check_sql"]:
            sql = case["check_sql"].format(conf.get_str("test_data",'user'))
            #获取充值之前的余额
            start_money = self.db.get_one(sql)[0]
        response = self.http.send(url=url,method=method,json=data,headers=headers)
        result = response.json()

        # -------第三步：比对预期结果和实际结果-----

        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual((expected["msg"]), result["msg"])
            if case["check_sql"]:
                sql = case["check_sql"].format(conf.get_str("test_data",'user'))
                #获取充值之前的余额
                end_money = self.db.get_one(sql)[0]
                recharge_money = decimal.Decimal(str(data["amount"]))#decimal只支持整数，如果有小数的话先转化成str就会自动保存1位小数
                my_log.info("充值之前金额为{}\n，充值金额为：{}\n，充值之后金额为{}，".format(start_money, recharge_money, end_money))
                # 进行断言
                self.assertEqual(recharge_money, end_money - start_money)
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            my_log.info("用例：{}---->执行通过".format(case["title"]))
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(result))
            raise e
        else:
            self.excel.write_data(row=row,column=8, value="通过")
            my_log.info("用例：{}--->执行通过".format(case["title"]))