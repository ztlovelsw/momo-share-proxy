# encoding:utf-8
import asyncio
import logging
from typing import List, Tuple
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from config import Config

logger = logging.getLogger(__name__)

class ProxyValidator:
    """代理验证器"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = ClientTimeout(total=timeout)
        self.test_url = "http://httpbin.org/ip"
        
    async def validate_proxy(self, proxy: str) -> Tuple[str, bool]:
        """验证单个代理"""
        try:
            async with ClientSession(timeout=self.timeout) as session:
                async with session.get(self.test_url, proxy=proxy) as response:
                    if response.status == 200:
                        return proxy, True
        except Exception as e:
            logger.debug(f"Proxy {proxy} validation failed: {e}")
        return proxy, False
    
    async def validate_proxies(self, proxies: List[str]) -> List[str]:
        """批量验证代理"""
        if not proxies:
            return []
            
        semaphore = asyncio.Semaphore(Config.CONCURRENT_REQUESTS)
        
        async def validate_with_semaphore(proxy):
            async with semaphore:
                return await self.validate_proxy(proxy)
        
        tasks = [validate_with_semaphore(proxy) for proxy in proxies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_proxies = []
        for result in results:
            if isinstance(result, tuple) and result[1]:
                valid_proxies.append(result[0])
        
        logger.info(f"Validated {len(valid_proxies)} out of {len(proxies)} proxies")
        return valid_proxies[:Config.MAX_PROXY_COUNT]