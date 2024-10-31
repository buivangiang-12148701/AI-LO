import asyncio
import aiohttp
from typing import List, Dict
import logging
from bs4 import BeautifulSoup
from app.core.exceptions import CrawlerError

class AsyncCrawler:
    def __init__(self, max_concurrency=5):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.logger = logging.getLogger(__name__)
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        
    async def fetch_page(self, url: str) -> str:
        """Fetch single page with semaphore"""
        async with self.semaphore:
            try:
                async with self.session.get(url) as response:
                    return await response.text()
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {str(e)}")
                raise CrawlerError(f"Failed to fetch {url}")
                
    async def crawl_recipes(self, urls: List[str]) -> List[Dict]:
        """Crawl multiple recipes concurrently"""
        tasks = [self.fetch_recipe(url) for url in urls]
        return await asyncio.gather(*tasks)
        
    async def fetch_recipe(self, url: str) -> Dict:
        """Fetch and parse single recipe"""
        html = await self.fetch_page(url)
        return self.parse_recipe(html)
        
    def parse_recipe(self, html: str) -> Dict:
        """Parse recipe HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # Parse logic here...
            return {
                'name': soup.find('h1').text,
                'ingredients': self.parse_ingredients(soup),
                'steps': self.parse_steps(soup)
            }
        except Exception as e:
            self.logger.error(f"Error parsing recipe: {str(e)}")
            raise CrawlerError("Failed to parse recipe") 