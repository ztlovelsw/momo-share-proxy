#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import tkinter
from tkinter import *
import hashlib
import time
from tkinter.ttk import Progressbar

import requests
import threading
LOG_LINE_NUM = 0


class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        # print('self.func', self.func)
        self.func(*self.args)

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("单词脚本_v1")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('500x240+10+10')
        # self.init_window_name["bg"] = "white"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="↓请在下方输入分享链接↓", width=70, anchor='center')
        self.init_data_label.grid(row=0, column=0)
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=70, height=3)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="点击开始运行", bg="lightblue", width=10,
                                              command=lambda: MyThread(self.str_trans_to_md5))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=20, column=0)
        #进度条
        self.progressbarOne = Progressbar(self.init_window_name, length=400)
        self.progressbarOne.grid(row=29, column=0)
        self.progressbarOne['maximum'] = 35
        self.progressbarOne['value'] = 0
        # 进度标签
        # self.progress_label = Label(self.init_window_name, anchor='center', width=5)
        # self.progress_label.grid(row=29, column=0)
        #日志
        self.log_data_Text = Text(self.init_window_name, width=70, height=9)  # 日志框
        self.log_data_Text.grid(row=31, column=0, columnspan=10)
        self.log_data_Text.insert(END, '输出日志'+"\n")
    #功能函数
    def str_trans_to_md5(self):
        share_url = self.init_data_Text.get(0.0, END).strip().replace("\n", "")
        print(f"DEBUG: 输入的分享链接: {share_url}")
        
        momo_url = 'https://www.maimemo.com'
        suc_num = 0
        
        if share_url[0:23] == momo_url:
            self.progressbarOne['value'] = 0
            self.write_log_to_Text("INFO: 开始运行任务...")
            print("DEBUG: 分享链接验证通过，开始运行")
            
            try:
                for i in range(35):
                    print(f"DEBUG: 第 {i+1}/35 次循环")
                    
                    if i != 0:
                        sleep_time = random.randint(60, 120)
                        print(f"DEBUG: 等待 {sleep_time} 秒...")
                        time.sleep(sleep_time)
                    
                    # 使用新的代理API格式
                    proxy_api_url = 'http://bapi.51daili.com/getapi2?linePoolIndex=-1&packid=2&time=1&qty=1&port=1&format=txt&dt=2&dtc=1&usertype=17&uid=59521'
                    print(f"DEBUG: 请求代理API: {proxy_api_url}")
                    
                    proxies = self.jl_api(proxy_api_url)
                    
                    if proxies is None:
                        self.write_log_to_Text(f"WARNING: 第{i+1}次 - 获取代理失败，跳过本次")
                        print(f"DEBUG: 第{i+1}次 - 代理获取失败")
                        self.progressbarOne['value'] += 1
                        self.init_window_name.update()
                        continue
                    
                    print(f"DEBUG: 使用代理: {proxies}")
                    result = self.run(share_url, suc_num, proxies)
                    
                    if result is not None:
                        suc_num = result
                        print(f"DEBUG: 第{i+1}次 - 成功，当前成功次数: {suc_num}")
                    else:
                        print(f"DEBUG: 第{i+1}次 - 失败")
                    
                    self.progressbarOne['value'] += 1
                    self.init_window_name.update()
                    self.write_log_to_Text("INFO: 进度 {}/35, 已成功{}次".format(i+1, suc_num))
                    
                    if i == 34:
                        self.write_log_to_Text("SUCCESS: 任务完成，总共成功{}次".format(suc_num))
                        print("DEBUG: 任务完成")
                        
            except Exception as e:
                error_msg = f"ERROR: 运行过程中发生异常: {str(e)}"
                print(error_msg)
                self.write_log_to_Text(error_msg)
        else:
            error_msg = "ERROR: 无效的分享链接，请检查链接格式"
            print(f"DEBUG: {error_msg}")
            self.write_log_to_Text(error_msg)

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)

    # def jl_api(self, api_url):
    #     # 获取API接口返回的代理IP
    #     proxy_ip = requests.get(api_url).text
    #     print(proxy_ip)
    #     # 用户名密码认证(动态代理/独享代理)
    #     username = ""
    #     password = ""
    #     proxies = {
    #         "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    #         "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    #     }
    #     # print(proxies)
    #     return proxies
    def jl_api(self, api_url):
        """获取代理IP并构建代理配置"""
        try:
            self.write_log_to_Text("INFO: 正在获取代理IP...")
            print(f"DEBUG: 请求代理API: {api_url}")
            
            # 获取API接口返回的代理IP
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            
            proxy_ip = response.text.strip()
            print(f"DEBUG: 获取到的代理IP: {proxy_ip}")
            
            if not proxy_ip:
                raise ValueError("获取到的代理IP为空")
            
            # 验证代理IP格式
            if ":" not in proxy_ip:
                raise ValueError(f"代理IP格式错误: {proxy_ip}")
            
            # 解析代理服务器
            proxy_parts = proxy_ip.split(":")
            if len(proxy_parts) != 2:
                raise ValueError(f"代理IP格式不正确: {proxy_ip}")
                
            proxyHost = proxy_parts[0]
            proxyPort = proxy_parts[1]
            
            # 验证端口是否为数字
            try:
                int(proxyPort)
            except ValueError:
                raise ValueError(f"代理端口格式错误: {proxyPort}")
            
            # 构建代理配置
            proxyMeta = f"http://{proxyHost}:{proxyPort}"
            proxies = {
                "http": proxyMeta,
                "https": proxyMeta  # 添加https支持
            }
            
            print(f"DEBUG: 代理配置: {proxies}")
            self.write_log_to_Text(f"INFO: 成功获取代理: {proxy_ip}")
            return proxies
            
        except requests.exceptions.Timeout:
            error_msg = "ERROR: 获取代理超时"
            print(error_msg)
            self.write_log_to_Text(error_msg)
            return None
            
        except requests.exceptions.RequestException as e:
            error_msg = f"ERROR: 请求代理API失败: {str(e)}"
            print(error_msg)
            self.write_log_to_Text(error_msg)
            return None
            
        except ValueError as e:
            error_msg = f"ERROR: 代理格式错误: {str(e)}"
            print(error_msg)
            self.write_log_to_Text(error_msg)
            return None
            
        except Exception as e:
            error_msg = f"ERROR: 获取代理时发生未知错误: {str(e)}"
            print(error_msg)
            self.write_log_to_Text(error_msg)
            return None

    def run(self, url_ls, suc_num, proxies):
        """执行请求并验证结果"""
        headers = {
            'authority': 'www.maimemo.com',
            'Proxy-Authorization': 'Basic ZDI0MjkxNjczNzU6bGM1ZjJ4cDQ=',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
        
        print(f"DEBUG: 开始请求URL: {url_ls}")
        print(f"DEBUG: 使用代理: {proxies}")
        
        try:
            # 设置重试次数
            requests.DEFAULT_RETRIES = 5
            session = requests.Session()
            session.keep_alive = False
            
            response = requests.get(
                url=url_ls,
                headers=headers,
                proxies=proxies,
                timeout=15,
                verify=False
            )
            
            print(f"DEBUG: 响应状态码: {response.status_code}")
            print(f"DEBUG: 响应头: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"WARNING: 非200状态码: {response.status_code}")
                return suc_num
            
            content = response.text
            content_length = len(content)
            print(f"DEBUG: 响应内容长度: {content_length}")
            
            # 检查是否包含目标关键词
            if "学习天数" in content:
                print("DEBUG: 成功找到'学习天数'关键词")
                suc_num += 1
                return suc_num
            else:
                print("DEBUG: 未找到'学习天数'关键词")
                # 打印部分内容用于调试
                if content_length > 200:
                    preview = content[:200] + "..."
                else:
                    preview = content
                print(f"DEBUG: 内容预览: {preview}")
                return suc_num
                
        except requests.exceptions.Timeout:
            print("ERROR: 请求超时")
            return suc_num
            
        except requests.exceptions.ProxyError as e:
            print(f"ERROR: 代理错误: {str(e)}")
            return suc_num
            
        except requests.exceptions.ConnectionError as e:
            print(f"ERROR: 连接错误: {str(e)}")
            return suc_num
            
        except Exception as e:
            print(f"ERROR: 请求过程中发生未知错误: {str(e)}")
            return suc_num
def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
