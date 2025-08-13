# encoding:utf-8
import asyncio
import logging
import random
from typing import List, Set
import aiohttp
from aiohttp import ClientSession, ClientTimeout, TCPConnector
import re
from config import Config
from proxy_validator import ProxyValidator

logger = logging.getLogger(__name__)

class ProxyCollector:
    """代理收集器"""
    
    def __init__(self):
        self.proxies: Set[str] = set()
        self.validator = ProxyValidator()
        
    def get_random_headers(self) -> dict:
        """获取随机请求头"""
        return {'User-Agent': random.choice(Config.USER_AGENTS)}
    
    async def fetch_page(self, session: ClientSession, url: str, mod: int = 0) -> None:
        """获取页面内容"""
        try:
            timeout = ClientTimeout(total=Config.PROXY_TIMEOUT)
            headers = self.get_random_headers()
            
            async with session.get(url, headers=headers, timeout=timeout) as response:
                if response.status == 200:
                    content = await response.text()
                    await self.parse_content(content, mod)
                else:
                    logger.warning(f"Failed to fetch {url}: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
    
    async def parse_content(self, content: str, mod: int) -> None:
        """解析页面内容提取代理"""
        try:
            if mod == 0:  # 通用解析
                ips = re.findall(r'<td>[\s]*?(\d+\.\d+\.\d+\.\d+)[\s]*?</td>', content)
                ports = re.findall(r'<td>[\s]*?(\d{1,5})[\s]*?</td>', content)
                for ip, port in zip(ips, ports):
                    self.proxies.add(f"http://{ip}:{port}")
                    
            elif mod == -1:  # 文本格式
                for line in content.strip().split('\n'):
                    if line.strip():
                        self.proxies.add(f"http://{line.strip()}")
                        
            elif mod == 2:  # 快代理
                ips = re.findall(r'<td\s.*?="IP">(\d+\.\d+\.\d+\.\d+)</td>', content)
                ports = re.findall(r'<td\s.*?="PORT">(\d{1,5})</td>', content)
                for ip, port in zip(ips, ports):
                    self.proxies.add(f"http://{ip}:{port}")
                    
            elif mod == 3:  # proxy-list
                for proxy in content.strip().split('\r\n')[:-1]:
                    self.proxies.add(f"http://{proxy}")
                    
            elif mod == 8:  # 89ip.cn
                match = re.search(r'<div\sstyle="padding-left:20px;">[\s]?(.*?)[\s]?</div>', content, re.DOTALL)
                if match:
                    proxies = match.group(1).strip().split('<br>')[:-2]
                    for proxy in proxies:
                        self.proxies.add(f"http://{proxy.strip()}")
                        
        except Exception as e:
            logger.error(f"Error parsing content with mod {mod}: {e}")
    
    async def collect_proxies(self) -> List[str]:
        """收集代理"""
        logger.info("Starting proxy collection...")
        
        connector = TCPConnector(ssl=False, limit=100)
        timeout = ClientTimeout(total=30)
        
        async with ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []
            for source in Config.PROXY_SOURCES:
                task = asyncio.create_task(
                    self.fetch_page(session, source['url'], source['mod'])
                )
                tasks.append(task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"Collected {len(self.proxies)} unique proxies")
        
        # 验证代理
        proxy_list = list(self.proxies)
        valid_proxies = await self.validator.validate_proxies(proxy_list)
        
        logger.info(f"Found {len(valid_proxies)} valid proxies")
        return valid_proxies

def collect_valid_proxies() -> List[str]:
    """收集有效代理的入口函数"""
    collector = ProxyCollector()
    return asyncio.run(collector.collect_proxies())