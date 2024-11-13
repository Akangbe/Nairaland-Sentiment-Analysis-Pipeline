import aiohttp
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict, Optional
import backoff
 


#  sCRAPING NAIRALAND

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


SECTIONS_CONFIG = {
    "Politics": "https://www.nairaland.com/politics",
    "Crime": "https://www.nairaland.com/crime",
    "Romance": "https://www.nairaland.com/romance",
    "Jobs/Vacancies": "https://www.nairaland.com/jobs",
    "Career": "https://www.nairaland.com/career",
    "Business": "https://www.nairaland.com/business",
    "Investment": "https://www.nairaland.com/investment",
    "NYSC": "https://www.nairaland.com/nysc",
    "Education": "https://www.nairaland.com/education",
    "Health": "https://www.nairaland.com/health",
    "Travel": "https://www.nairaland.com/travel",
    "Family": "https://www.nairaland.com/family",
    "Culture": "https://www.nairaland.com/culture",
    "Religion": "https://www.nairaland.com/religion",
    "Food": "https://www.nairaland.com/food"
}

class NairalandScraper:
    def __init__(self, save_dir: str = "scraped_data"):
        self.ua = UserAgent()
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.sections = SECTIONS_CONFIG
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=50)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3
    )
    async def fetch_page(self, url: str) -> str:
        """Fetch a page with retry logic and error handling"""
        headers = {'User-Agent': self.ua.random}
        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url}: Status {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""

    async def get_posts_links(self, url: str) -> List[str]:
        """Extract post links from a section page"""
        try:
            html = await self.fetch_page(url)
            if not html:
                return []
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find posts table
            body = soup.find("div", class_="body")
            if not body:
                logger.warning(f"No body found for {url}")
                return []
                
            tables = body.find_all("table")
            posts_table = None
            for table in tables:
                if table.find("tr") and table.find("tr").find("th"):
                    posts_table = table
                    break
                    
            if not posts_table:
                logger.warning(f"No posts table found for {url}")
                return []
                
            # Extract links
            posts_info = posts_table.tr.th.find_all("td")
            links = [
                f"https://www.nairaland.com{i.find('b').a['href']}" 
                for i in posts_info 
                if i.find("b") and i.find("b").a
            ]
            logger.info(f"Found {len(links)} links in {url}")
            return links
            
        except Exception as e:
            logger.error(f"Error getting posts links from {url}: {str(e)}")
            return []

    async def get_post_content(self, url: str) -> Dict:
        """Extract content from a single post"""
        try:
            html = await self.fetch_page(url)
            if not html:
                return {}
                
            soup = BeautifulSoup(html, 'html.parser')
            
            body = soup.find("div", class_="body")
            if not body:
                return {}
                
            # Get main post and comments
            main_post = body.find("div", class_="narrow")
            posts_table = body.find("table", summary="posts")
            comment_posts = posts_table.find_all("td", class_="l w pd")[1:] if posts_table else []
            
            comments = [
                post.find("div", class_="narrow").text.strip() 
                for post in comment_posts 
                if post.find("div", class_="narrow")
            ]
            
            post_data = {
                'url': url,
                'title': soup.title.text if soup.title else '',
                'main_post': main_post.text.strip() if main_post else '',
                'comments': comments,
                'num_comments': len(comments),
                'scraped_at': datetime.now().isoformat()
            }
            
            logger.info(f"Successfully scraped post: {url}")
            return post_data
            
        except Exception as e:
            logger.error(f"Error getting post content from {url}: {str(e)}")
            return {}

    def get_section_urls(self, section: str, num_pages: int) -> List[str]:
        """Generate URLs for all pages in a section"""
        base_url = self.sections.get(section)
        if not base_url:
            logger.error(f"Section {section} not found in config")
            return []
        return [f"{base_url}/{page}" for page in range(num_pages)]

    async def scrape_section(self, section: str, num_pages: int, batch_size: int = 5):
        """Scrape an entire section"""
        logger.info(f"Starting scrape of section: {section}")
        
        # Get all page URLs for the section
        section_urls = self.get_section_urls(section, num_pages)
        
        all_posts = []
        total_posts = 0
        
        # Process URLs in batches
        for i in range(0, len(section_urls), batch_size):
            batch_urls = section_urls[i:i + batch_size]
            
            # Get post links from section pages
            tasks = [self.get_posts_links(url) for url in batch_urls]
            batch_links = await asyncio.gather(*tasks)
            post_links = [link for sublist in batch_links for link in sublist]
            
            logger.info(f"Processing batch {i//batch_size + 1}, found {len(post_links)} links")
            
            # Get content from each post
            tasks = [self.get_post_content(url) for url in post_links]
            posts = await asyncio.gather(*tasks)
            valid_posts = [p for p in posts if p]  # Filter out empty results
            all_posts.extend(valid_posts)
            total_posts += len(valid_posts)
            
            # Save intermediate results
            if len(all_posts) >= 100:  # Reduced threshold for testing
                self.save_posts(section, all_posts)
                logger.info(f"Saved batch of {len(all_posts)} posts for {section}")
                all_posts = []
                
            await asyncio.sleep(3)  # Reduced delay for testing
            
        # Save any remaining posts
        if all_posts:
            self.save_posts(section, all_posts)
            
        logger.info(f"Completed scrape of section: {section}. Total posts: {total_posts}")

    def save_posts(self, section: str, posts: List[Dict]):
        """Save posts to CSV file"""
        df = pd.DataFrame(posts)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.save_dir / f"{section}_{timestamp}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Saved {len(posts)} posts to {filename}")

# async def main():
#     # Start with a smaller test run
#     sections_to_scrape = ["Politics"]  # We'll start with just one section
    
#     async with NairalandScraper() as scraper:
#         for section in sections_to_scrape:
#             await scraper.scrape_section(section, num_pages=5)  # Reduced pages for testing




async def main():
    sections_to_scrape = ["Politics", "Business", "Crime", "NYSC","Education", "Food", "Romance"] 
    
    async with NairalandScraper() as scraper:
        for section in sections_to_scrape:
            await scraper.scrape_section(section, num_pages=10) 

if __name__ == "__main__":
    asyncio.run(main())

