# main.py

import asyncio
import logging
from Scraper.scraper import NairalandScraper
from processor.text_processor import TextProcessor
from Database.mongo_handler import MongoHandler
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def main():
    # Initialize components
    scraper = NairalandScraper()
    processor = TextProcessor()
    mongo_handler = MongoHandler(
        os.getenv("MONGO_URI"),  # Access MONGO_URI from .env
        'nairaland_db'
    )
    
    sections = ["Politics", "Business", "Crime", "NYSC", "Education", "Food", "Romance"]
    
    try:
        async with scraper:
            for section in sections:
                # Scrape posts
                posts = await scraper.scrape_section(section, num_pages=10)
                
                # Process posts
                processed_posts = [processor.process_post(post) for post in posts]
                
                # Store in MongoDB
                mongo_handler.insert_posts(processed_posts, section)
                
                logging.info(f"Completed processing for section: {section}")
                
    except Exception as e:
        logging.error(f"Pipeline error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())


















# import asyncio
# import logging
# from Scraper.scraper import NairalandScraper
# from processor.text_processor import TextProcessor
# from Database.mongo_handler import MongoHandler
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# async def main():
#     # Initialize components
#     scraper = NairalandScraper()
#     processor = TextProcessor()
#     mongo_handler = MongoHandler(
#         os.getenv("MONGO_URI"),  # Access MONGO_URI from .env
#         'nairaland_db'
#     )
    
#     sections = ["Politics", "Business", "Crime", "NYSC", "Education", "Food"]
    
#     try:
#         async with scraper:
#             for section in sections:
#                 # Scrape posts
#                 posts = await scraper.scrape_section(section, num_pages=10)
                
#                 if posts is None:
#                     logging.warning(f"No posts found for section: {section}")
#                     continue  # Skip to the next section if no posts are found
                
#                 # Process posts
#                 processed_posts = [processor.process_post(post) for post in posts]
                
#                 # Store in MongoDB
#                 mongo_handler.insert_posts(processed_posts, section)
                
#                 logging.info(f"Completed processing for section: {section}")
                
#     except Exception as e:
#         logging.error(f"Pipeline error: {str(e)}")

# if __name__ == "__main__":
#     asyncio.run(main())
