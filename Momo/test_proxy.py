#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
代理功能测试脚本
用于测试新的代理API格式是否正常工作
"""

import requests
import sys
import os

# 添加当前目录到路径，以便导入momo_proxy_useful
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from momo_proxy_useful import MY_GUI
import tkinter as tk

def test_proxy_api():
    """测试代理API获取功能"""
    print("=" * 50)
    print("开始测试代理API...")
    
    # 创建GUI实例（不显示窗口）
    root = tk.Tk()
    gui = MY_GUI(root)
    
    # 测试新的代理API
    proxy_api_url = 'http://bapi.51daili.com/getapi2?linePoolIndex=-1&packid=2&time=1&qty=1&port=1&format=txt&dt=2&dtc=1&usertype=17&uid=59521'
    
    print(f"测试API: {proxy_api_url}")
    
    try:
        proxies = gui.jl_api(proxy_api_url)
        
        if proxies:
            print("✅ 代理获取成功!")
            print(f"代理配置: {proxies}")
            
            # 测试代理是否可用
            test_url = "http://httpbin.org/ip"
            print(f"\n测试代理可用性...")
            
            try:
                response = requests.get(test_url, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    print("✅ 代理可用!")
                    print(f"返回内容: {response.text}")
                else:
                    print(f"❌ 代理测试失败，状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ 代理测试出错: {str(e)}")
                
        else:
            print("❌ 代理获取失败")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_proxy_api()