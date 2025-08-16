#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import tkinter
from tkinter import *
import hashlib
import time
import socket
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
        self.init_window_name.title("Momo代理工具 v2.0")           #窗口名
        self.init_window_name.geometry('600x400+100+100')
        self.init_window_name.configure(bg='#f0f0f0')
        
        # 设置窗口图标和样式
        try:
            self.init_window_name.iconbitmap(default='')  # 可以添加图标路径
        except:
            pass
            
        # 主框架
        main_frame = Frame(self.init_window_name, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # 标题标签
        title_label = Label(main_frame, text="Momo分享链接自动化工具",
                           font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 分享链接输入区域
        link_frame = LabelFrame(main_frame, text="分享链接", font=('Arial', 10, 'bold'),
                               bg='#f0f0f0', padx=10, pady=10)
        link_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        
        self.init_data_label = Label(link_frame, text="请输入Momo分享链接：",
                                   font=('Arial', 10), bg='#f0f0f0')
        self.init_data_label.grid(row=0, column=0, sticky='w')
        
        self.init_data_Text = Text(link_frame, width=60, height=3, font=('Arial', 10),
                                  relief='solid', borderwidth=1)
        self.init_data_Text.grid(row=1, column=0, pady=(5, 0))
        
        # 配置参数区域
        config_frame = LabelFrame(main_frame, text="运行配置", font=('Arial', 10, 'bold'),
                                 bg='#f0f0f0', padx=10, pady=10)
        config_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        
        # 代理地址输入
        Label(config_frame, text="代理地址：", font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, sticky='w')
        self.proxy_url_var = tkinter.StringVar(
            value=""
        )
        self.proxy_url_entry = Entry(config_frame, textvariable=self.proxy_url_var,
                                   width=60, font=('Arial', 9), relief='solid', borderwidth=1)
        self.proxy_url_entry.grid(row=0, column=1, padx=(10, 0), sticky='ew', columnspan=3)
        
        # 运行次数输入
        Label(config_frame, text="运行次数：", font=('Arial', 10), bg='#f0f0f0').grid(row=1, column=0, sticky='w')
        self.run_count_var = tkinter.StringVar(value="35")
        self.run_count_entry = Entry(config_frame, textvariable=self.run_count_var,
                                   width=10, font=('Arial', 10), relief='solid', borderwidth=1)
        self.run_count_entry.grid(row=1, column=1, padx=(10, 0), sticky='w')
        
        # 配置网格权重
        config_frame.grid_columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = Frame(main_frame, bg='#f0f0f0')
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.str_trans_to_md5_button = Button(button_frame, text="开始运行",
                                            bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                            activebackground='#2980b9', activeforeground='white',
                                            relief='raised', borderwidth=2, padx=20, pady=5,
                                            command=lambda: MyThread(self.str_trans_to_md5))
        self.str_trans_to_md5_button.pack(side='left', padx=(0, 10))
        
        # 白名单按钮
        self.white_ip_button = Button(button_frame, text="添加IP白名单",
                                    bg='#2ecc71', fg='white', font=('Arial', 10),
                                    activebackground='#27ae60', activeforeground='white',
                                    relief='raised', borderwidth=2, padx=10, pady=5,
                                    command=self.add_white_ip)
        self.white_ip_button.pack(side='left')
        
        # 进度区域
        progress_frame = LabelFrame(main_frame, text="运行进度", font=('Arial', 10, 'bold'),
                                   bg='#f0f0f0', padx=10, pady=10)
        progress_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        
        self.progressbarOne = Progressbar(progress_frame, length=500, mode='determinate',
                                         style='Horizontal.TProgressbar')
        self.progressbarOne.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        self.progressbarOne['value'] = 0
        
        # 进度百分比标签
        self.progress_label = Label(progress_frame, text="0%", font=('Arial', 9), bg='#f0f0f0')
        self.progress_label.grid(row=0, column=1, padx=(10, 0))
        
        # 日志区域
        log_frame = LabelFrame(main_frame, text="运行日志", font=('Arial', 10, 'bold'),
                              bg='#f0f0f0', padx=10, pady=10)
        log_frame.grid(row=5, column=0, columnspan=2, sticky='nsew', pady=(0, 10))
        
        self.log_data_Text = Text(log_frame, width=70, height=12, font=('Consolas', 9),
                                 relief='solid', borderwidth=1)
        self.log_data_Text.grid(row=0, column=0, sticky='nsew')
        
        # 滚动条
        scrollbar = Scrollbar(log_frame, command=self.log_data_Text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.log_data_Text.config(yscrollcommand=scrollbar.set)
        
        # 配置网格权重
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # 初始日志
        self.log_data_Text.insert(END, '系统初始化完成，准备就绪...\n')
        
        # 设置样式
        try:
            from tkinter import ttk
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Horizontal.TProgressbar',
                          background='#3498db',
                          troughcolor='#ecf0f1',
                          borderwidth=0,
                          lightcolor='#3498db',
                          darkcolor='#3498db')
        except:
            pass
    #功能函数
    def str_trans_to_md5(self):
        share_url = self.init_data_Text.get(0.0, END).strip().replace("\n", "")
        print(f"DEBUG: 输入的分享链接: {share_url}")
        
        # 获取代理地址
        proxy_api_url = self.proxy_url_var.get().strip()
        if not proxy_api_url:
            self.write_log_to_Text("ERROR: 请输入代理地址")
            return
        
        # 获取运行次数
        try:
            run_count = int(self.run_count_var.get())
            if run_count <= 0 or run_count > 1000:
                self.write_log_to_Text("ERROR: 运行次数必须在1-1000之间")
                return
        except ValueError:
            self.write_log_to_Text("ERROR: 请输入有效的运行次数")
            return
        
        momo_url = 'https://www.maimemo.com'
        suc_num = 0
        
        if share_url[0:23] == momo_url:
            self.progressbarOne['value'] = 0
            self.progressbarOne['maximum'] = run_count
            self.progress_label.config(text="0%")
            self.write_log_to_Text(f"INFO: 开始运行任务，共{run_count}次...")
            self.write_log_to_Text(f"INFO: 使用代理地址: {proxy_api_url}")
            print(f"DEBUG: 分享链接验证通过，开始运行{run_count}次")
            
            # 禁用按钮防止重复点击
            self.str_trans_to_md5_button.config(state='disabled')
            self.white_ip_button.config(state='disabled')
            
            # 自动添加IP到白名单
            self.write_log_to_Text("INFO: 正在自动添加IP到白名单...")
            white_result = self.add_white_ip()
            if not white_result:
                self.write_log_to_Text("WARNING: IP白名单添加失败，可能不影响使用")
            
            try:
                for i in range(run_count):
                    current_percent = int((i / run_count) * 100)
                    print(f"DEBUG: 第 {i+1}/{run_count} 次循环 ({current_percent}%)")
                    
                    if i != 0:
                        sleep_time = random.randint(60, 120)
                        print(f"DEBUG: 等待 {sleep_time} 秒...")
                        self.write_log_to_Text(f"INFO: 等待{sleep_time}秒后继续...")
                        time.sleep(sleep_time)
                    
                    # 使用GUI输入的代理地址
                    print(f"DEBUG: 请求代理API: {proxy_api_url}")
                    
                    proxies = self.jl_api(proxy_api_url)
                    
                    if proxies is None:
                        self.write_log_to_Text(f"WARNING: 第{i+1}次 - 获取代理失败，跳过本次")
                        print(f"DEBUG: 第{i+1}次 - 代理获取失败")
                        self.progressbarOne['value'] += 1
                        current_percent = int(((i + 1) / run_count) * 100)
                        self.progress_label.config(text=f"{current_percent}%")
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
                    current_percent = int(((i + 1) / run_count) * 100)
                    self.progress_label.config(text=f"{current_percent}%")
                    self.init_window_name.update()
                    self.write_log_to_Text("INFO: 进度 {}/{} ({}%), 已成功{}次".format(i+1, run_count, current_percent, suc_num))
                    
                    if i == run_count - 1:
                        self.write_log_to_Text("SUCCESS: 任务完成，总共成功{}次".format(suc_num))
                        print("DEBUG: 任务完成")
                        
            except Exception as e:
                error_msg = f"ERROR: 运行过程中发生异常: {str(e)}"
                print(error_msg)
                self.write_log_to_Text(error_msg)
            finally:
                # 重新启用按钮
                self.str_trans_to_md5_button.config(state='normal')
                self.white_ip_button.config(state='normal')
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

    def get_local_ip(self):
        """获取本地公网IP地址"""
        try:
            # 使用多个IP检测服务提高可靠性
            ip_services = [
                'http://httpbin.org/ip',
                'https://api.ipify.org',
                'http://icanhazip.com'
            ]
            
            for service in ip_services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        ip = response.text.strip()
                        # 处理httpbin.org的JSON格式
                        if 'origin' in ip:
                            import json
                            ip = json.loads(ip)['origin']
                        return ip
                except:
                    continue
                    
            # 如果都失败，尝试获取本地IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            finally:
                s.close()
            return ip
            
        except Exception as e:
            print(f"ERROR: 获取IP地址失败: {str(e)}")
            return None

    def add_white_ip(self):
        """自动添加当前IP到白名单"""
        try:
            self.write_log_to_Text("INFO: 正在获取本地IP...")
            local_ip = self.get_local_ip()
            
            if not local_ip:
                self.write_log_to_Text("ERROR: 无法获取本地IP地址")
                return False
            
            self.write_log_to_Text(f"INFO: 检测到本地IP: {local_ip}")
            
            # 构建白名单API URL
            white_api = f"http://aapi.51daili.com/whiteIP-list?op=add&appkey=51代理网站获取&whiteip={local_ip}"
            print(f"DEBUG: 白名单API: {white_api}")
            
            response = requests.get(white_api, timeout=10)
            response.raise_for_status()
            
            result = response.text.strip()
            print(f"DEBUG: 白名单API返回: {result}")
            
            if "success" in result.lower() or "ok" in result.lower():
                self.write_log_to_Text(f"SUCCESS: IP白名单添加成功: {local_ip}")
                return True
            else:
                self.write_log_to_Text(f"WARNING: IP白名单添加结果: {result}")
                return False
                
        except requests.exceptions.Timeout:
            self.write_log_to_Text("ERROR: 添加白名单超时")
            return False
            
        except requests.exceptions.RequestException as e:
            self.write_log_to_Text(f"ERROR: 添加白名单请求失败: {str(e)}")
            return False
            
        except Exception as e:
            self.write_log_to_Text(f"ERROR: 添加白名单时发生错误: {str(e)}")
            return False

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
