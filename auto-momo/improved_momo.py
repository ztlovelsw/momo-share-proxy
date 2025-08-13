# encoding:utf-8
import asyncio
import logging
import os
from typing import List
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from config import Config
from improved_ip import collect_valid_proxies

logger = logging.getLogger(__name__)

class MomoShare:
    """墨墨分享器"""
    
    def __init__(self):
        self.success_count = 0
        self.config = Config
        
    def get_random_headers(self) -> dict:
        """获取随机请求头"""
        return {'User-Agent': random.choice(self.config.USER_AGENTS)}
    
    async def visit_with_proxy(self, session: ClientSession, url: str, proxy: str) -> bool:
        """使用代理访问URL"""
        try:
            timeout = ClientTimeout(total=self.config.PROXY_TIMEOUT)
            headers = self.get_random_headers()
            
            async with session.get(
                url, 
                headers=headers, 
                proxy=proxy, 
                timeout=timeout
            ) as response:
                if response.status == 200:
                    content = await response.text()
                    return "学习天数" in content
                    
        except Exception as e:
            if self.config.DEBUG_MODE:
                logger.debug(f"Failed to visit with proxy {proxy}: {e}")
                
        return False
    
    async def visit_with_semaphore(self, semaphore: asyncio.Semaphore, session: ClientSession, url: str, proxy: str) -> None:
        """带并发限制的访问"""
        async with semaphore:
            success = await self.visit_with_proxy(session, url, proxy)
            if success:
                self.success_count += 1
                logger.info(f"Successfully visited with proxy {proxy}")
    
    async def share_momo(self, proxies: List[str]) -> int:
        """执行墨墨分享"""
        if not self.config.MOMO_LINK:
            raise ValueError("MOMO_LINK is not configured")
            
        logger.info(f"Starting momo share with {len(proxies)} proxies")
        
        semaphore = asyncio.Semaphore(self.config.CONCURRENT_REQUESTS)
        timeout = ClientTimeout(total=30)
        
        async with ClientSession(timeout=timeout) as session:
            tasks = [
                self.visit_with_semaphore(semaphore, session, self.config.MOMO_LINK, proxy)
                for proxy in proxies
            ]
            
            await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"Momo share completed: {self.success_count} successful visits")
        return self.success_count

def main():
    """主函数"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # 收集有效代理
        proxies = collect_valid_proxies()
        if not proxies:
            logger.error("No valid proxies found")
            return
        
        # 执行分享
        share = MomoShare()
        success_count = asyncio.run(share.share_momo(proxies))
        
        print(f"墨墨分享链接访问成功{success_count}次。")
        
    except Exception as e:
        logger.error(f"Failed to execute momo share: {e}")
        raise

if __name__ == '__main__':
    main()