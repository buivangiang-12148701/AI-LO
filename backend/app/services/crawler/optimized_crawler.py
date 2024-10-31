import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from urllib.parse import urljoin
import time

class OptimizedCrawler:
    def __init__(self, max_concurrency: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.results = []
        self.seen_urls = set()
        
    async def crawl_with_retry(self, url: str, retries: int = 3) -> str:
        """Crawl với retry mechanism"""
        for attempt in range(retries):
            try:
                async with self.semaphore:
                    async with self.session.get(url) as response:
                        return await response.text()
            except Exception as e:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    async def process_url(self, url: str):
        """Xử lý một URL"""
        if url in self.seen_urls:
            return
            
        self.seen_urls.add(url)
        html = await self.crawl_with_retry(url)
        data = self.parse_html(html)
        
        if data:
            self.results.append(data)
            
            # Find new URLs to crawl
            new_urls = self.extract_urls(html)
            tasks = [self.process_url(url) for url in new_urls]
            await asyncio.gather(*tasks)

    def parse_html(self, html: str) -> Dict:
        """Parse HTML content"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # Implement parsing logic
            pass
        except Exception as e:
            logging.error(f"Parse error: {str(e)}")
            return None 