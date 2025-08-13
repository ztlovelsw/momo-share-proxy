# encoding:utf-8
import os
from typing import Dict, Any

class Config:
    """配置管理类"""
    
    # 代理配置
    MAX_PROXY_COUNT = int(os.getenv('MAX_PROXY_COUNT', 50))
    PROXY_TIMEOUT = 10
    CONCURRENT_REQUESTS = 5
    
    # 目标配置
    MOMO_LINK = os.getenv('MOMO_LINK', '')
    
    # 调试配置
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    # 用户代理列表
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
    ]
    
    # 代理源配置
    PROXY_SOURCES = [
        {'url': 'http://www.kxdaili.com/dailiip.html', 'mod': 0},
        {'url': 'https://proxy.seofangfa.com/', 'mod': 0},
        {'url': 'http://www.66ip.cn', 'mod': 0},
        {'url': 'https://www.kuaidaili.com/free', 'mod': 2},
        {'url': 'https://www.89ip.cn', 'mod': 8},
        {'url': 'https://cdn.jsdelivr.net/gh/parserpp/ip_ports@master/proxyinfo.txt', 'mod': -1},
        {'url': 'https://fastly.jsdelivr.net/gh/parserpp/ip_ports@main/proxyinfo.txt', 'mod': -1},
        {'url': 'https://www.proxy-list.download/api/v1/get?type=http', 'mod': 3},
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """验证配置"""
        if not cls.MOMO_LINK:
            raise ValueError("MOMO_LINK environment variable is required")
        return True