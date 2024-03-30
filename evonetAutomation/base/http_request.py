# -*- coding: utf-8 -*-

from RequestsLibrary import RequestsKeywords
from config.evopay.evopay_conf import EvopayConf
import json
import urllib3
import requests
import datetime
from robot.api import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Http(RequestsKeywords):
    '''
          基本的http操作
    '''

    def __init__(self):
        super(Http, self).__init__()

    def http_post(self, url, uri, **kwargs):
        '''
        - 功能：发post请求
        - 参数如下：
        - url：接口url
        - uri：对应接口api
        - alias(可选)保持session会话的标识,默认为post_api
        - session_headers(可选):一个会话中公共请求头
        - session_cookies(可选)：一个会话中公共cookie请求头,格式类型为cookiejar，一般通过上次请求响应cookie获取
        - headers(可选): 发送POST请求的请求头，具体某一个请求，一个会话中可以有多个请求
        - data（可选）：请求体，格式为json
        - file_data(可选)：文件以请求体形式发送 ，格式为文件路径
        - files（可选）: 上传附件。格式为json，key为文件名，value为文件路径
        - allow_redirects(可选)：是否选择自动跳转。TRUE允许跳转，FALSE不允许跳转
        - context(可选):上下文联系参数,当需要进行上下文请求时选用该参数，与创建session中alias参数值保持一致
        - RobotFramwork脚本写法示例如下：
        | http_post | http://6.test.ums86.com/ | api/post.do | alias=post_api | session_cookies=${before_cookie}
        | session_headers={"Content-Type":"application/json"} | headers={"charset":"utf-8"} | data={"name": "liwei"}
        | file_data="C:/a.jpg" | files={"file1":"C:/a.txt"} | context="上文API" | allow_redirects=${false} |
        '''
        session_headers = {}
        session_cookies = None
        post_headers = None
        post_data = None
        post_files = {}
        post_allow_redirects = None
        alias = 'post_api'
        if 'alias' in kwargs and kwargs['alias'] != '':
            alias = kwargs['alias']
        if 'session_headers' in kwargs and kwargs['session_headers'] != '':
            session_headers = kwargs['session_headers']
        if 'session_cookies' in kwargs and kwargs['session_cookies'] != '':
            session_cookies = kwargs['session_cookies']
        if 'headers' in kwargs and kwargs['headers'] != '':
            post_headers = kwargs['headers']
        if 'data' in kwargs and kwargs['data'] != '':
            post_data = kwargs['data']
        if "json" in kwargs and kwargs['json'] != "":
            post_json = kwargs["json"]
        if 'file_data' in kwargs and kwargs['file_data'] != '':
            post_data = open(kwargs['file_data'], 'rb')
        if 'files' in kwargs and kwargs['files'] != '':
            files_dict = json.loads(kwargs['files'])
            for key in files_dict:
                post_files[key] = open(files_dict[key], 'rb')
        if 'allow_redirects' in kwargs and kwargs['allow_redirects'] != '':
            post_allow_redirects = kwargs['allow_redirects']
            print(type(post_allow_redirects))
        if 'context' not in kwargs:
            self.create_session(alias, url, session_headers, cookies=session_cookies)
        else:
            alias = kwargs['context']
        itf_result = self.post_request(alias, uri, json=post_json, data=post_data, headers=post_headers,
                                       files=post_files, allow_redirects=post_allow_redirects, timeout=5)
        if 'context' not in kwargs:
            self.delete_all_sessions()
        return itf_result

    def http_get(self, url, uri, **kwargs):
        '''
        - 功能：发get请求
        - 参数如下：
        - url：接口url
        - uri：对应接口uri
        - alias(可选)保持session会话的标识,默认为get_api
        - session_headers(可选):一个会话中公共请求头，格式为json
        - session_cookies(可选)：一个会话中公共cookie请求头,格式为json
        - headers(可选): 发送GET请求的请求头，具体某一个请求，一个会话中可以有多个请求
        - params（可选）：请求参数，格式为json
        - json(可选)：以json方式发送请求体 ，格式为json
        - allow_redirects(可选)：是否选择自动跳转。TRUE允许跳转，FALSE不允许跳转
        - context(可选):上下文联系参数,当需要进行上下文请求时选用该参数，与创建session中alias参数值保持一致
        - RobotFramwork脚本写法示例如下：
        | http_get | http://6.test.ums86.com/ | api/getlist.do | alias=get_api | session_cookies=${before_cookie} | session_headers={"Content-Type":"application/x-www-form-urlencoded} | headers={"charset":"utf-8"} | params={"name": "liwei","password":"123"} | json={"data":"123"} | context="上文API" | allow_redirects=${false} |
        '''
        session_headers = {}
        session_cookies = None
        get_headers = {}
        get_params = None
        get_json = None
        get_allow_redirects = None
        alias = "get_api"
        if 'alias' in kwargs and kwargs['alias'] != '':
            alias = kwargs['alias']
        if 'session_headers' in kwargs and kwargs['session_headers'] != '':
            session_headers = kwargs['session_headers']
        if 'session_cookies' in kwargs and kwargs['session_cookies'] != '':
            session_cookies = kwargs['session_cookies']
        # 解析headers#
        if 'headers' in kwargs and kwargs["headers"] != "":
            get_headers = kwargs["headers"]
        # 解析params#
        if "params" in kwargs and kwargs["params"] != "":
            get_params = json.loads(kwargs["params"])
        if "json" in kwargs and kwargs['json'] != "":
            get_json = json.loads(kwargs["json"])
        if "allow_redirects" in kwargs and kwargs['allow_redirects'] != "":
            get_allow_redirects = kwargs['allow_redirects']

        if 'context' not in kwargs:
            self.create_session(alias, url, session_headers, cookies=session_cookies)
        else:
            alias = kwargs['context']
        # 调get接口，保存结果#
        itf_result = self.get_request(alias, uri, headers=get_headers, json=get_json, params=get_params,
                                      allow_redirects=get_allow_redirects)
        if 'context' not in kwargs:
            self.delete_all_sessions()
        # 返回响应结果#
        return itf_result


class HttpRequest(object):
    '''
    封装request方法
    '''

    def send(self, url, method, params=None, data=None, json=None, headers=None):
        if method == "post":
            return requests.post(url=url, json=json, data=data, headers=headers, verify=False)
        elif method == "patch":
            return requests.patch(url=url, json=json, data=data, headers=headers, verify=False)
        elif method == "get":
            return requests.get(url=url, headers=headers, verify=False)
            # 为什么重写了这个方法，因为，上面的send方法中的get请求 之前没有传 paramers,怕加上之后当前的用例执行会失败



    # 触发task表的定时任务
    def mdaq_task_request(self, task_name, task_handler, time=None):

        # 默认为现在时间
        if not time:
            time = datetime.datetime.today().strftime("%Y%m%d %H%M%S.%f")
        header = {
            'Content-Type': 'application/json'
        }

        data = {
            "taskName": task_name,
            "handler": task_handler,
            "settleDate": time
        }
        result = requests.post(url=EvopayConf("test").mdap_func_url, headers=header, json=data)
        return result


if __name__ == '__main__':
    a = HttpRequest()
    c = a.mdaq_task_request("MDaqSubmitBatchAdvice", "SubmitBatchAdvice")
    res = c.json()
    print(res['status'])
    print(res['traceID'])
