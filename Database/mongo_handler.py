# # database/mongo_handler.py
# from pymongo import MongoClient
# from typing import List, Dict
# import logging
# from datetime import datetime

# class MongoHandler:
#     def __init__(self, connection_string: str, database_name: str):
#         self.client = MongoClient("collection1")
#         self.db = self.client["my_database1"]
        
#     def insert_posts(self, posts: List[Dict], section: str):
#         """Insert processed posts into MongoDB"""
#         try:
#             collection = self.db[section]
            
#             # Add timestamp for tracking
#             for post in posts:
#                 post['inserted_at'] = datetime.now()
                
#             # Insert posts
#             result = collection.insert_many(posts)
#             logging.info(f"Inserted {len(result.inserted_ids)} posts into {section} collection")
            
#             return result.inserted_ids
            
#         except Exception as e:
#             logging.error(f"Error inserting posts into MongoDB: {str(e)}")
#             raise

#     def get_posts_by_sentiment(self, section: str, sentiment: str) -> List[Dict]:
#         """Retrieve posts by sentiment category"""
#         collection = self.db[section]
#         return list(collection.find({'sentiment_category': sentiment}))

#     def get_section_stats(self, section: str) -> Dict:
#         """Get statistics for a section"""
#         collection = self.db[section]
        
#         stats = {
#             'total_posts': collection.count_documents({}),
#             'sentiment_distribution': {
#                 'positive': collection.count_documents({'sentiment_category': 'positive'}),
#                 'negative': collection.count_documents({'sentiment_category': 'negative'}),
#                 'neutral': collection.count_documents({'sentiment_category': 'neutral'})
#             }
#         }
        
#         return stats








# from pymongo import MongoClient
# from typing import List, Dict
# import logging
# from datetime import datetime

# class MongoHandler:
#     def __init__(self, connection_string: str):
#         self.client = MongoClient(connection_string)
#         self.db = self.client["my_database1"]  # Use your actual database name here
        
#     def insert_posts(self, posts: List[Dict]):
#         """Insert processed posts into MongoDB"""
#         try:
#             collection = self.db["collection1"]  # Use your actual collection name
            
#             # Add timestamp for tracking
#             for post in posts:
#                 post['inserted_at'] = datetime.now()
                
#             # Insert posts
#             result = collection.insert_many(posts)
#             logging.info(f"Inserted {len(result.inserted_ids)} posts into collection1")
            
#             return result.inserted_ids
            
#         except Exception as e:
#             logging.error(f"Error inserting posts into MongoDB: {str(e)}")
#             raise

#     def get_posts_by_sentiment(self, sentiment: str) -> List[Dict]:
#         """Retrieve posts by sentiment category"""
#         collection = self.db["collection1"]
#         return list(collection.find({'sentiment_category': sentiment}))

#     def get_section_stats(self) -> Dict:
#         """Get statistics for a section"""
#         collection = self.db["collection1"]
        
#         stats = {
#             'total_posts': collection.count_documents({}),
#             'sentiment_distribution': {
#                 'positive': collection.count_documents({'sentiment_category': 'positive'}),
#                 'negative': collection.count_documents({'sentiment_category': 'negative'}),
#                 'neutral': collection.count_documents({'sentiment_category': 'neutral'})
#             }
#         }
        
#         return stats



















from pymongo import MongoClient
from typing import List, Dict
import logging
from datetime import datetime

class MongoHandler:
    def __init__(self, connection_string: str, database_name: str):
        # Initialize MongoDB connection with provided URI and database name
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        
    def insert_posts(self, posts: List[Dict], section: str):
        """Insert processed posts into MongoDB"""
        try:
            collection = self.db[section]
            
            # Add timestamp for tracking
            for post in posts:
                post['inserted_at'] = datetime.now()
                
            # Insert posts
            result = collection.insert_many(posts)
            logging.info(f"Inserted {len(result.inserted_ids)} posts into {section} collection")
            
            return result.inserted_ids
            
        except Exception as e:
            logging.error(f"Error inserting posts into MongoDB: {str(e)}")
            raise

    def get_posts_by_sentiment(self, section: str, sentiment: str) -> List[Dict]:
        """Retrieve posts by sentiment category"""
        collection = self.db[section]
        return list(collection.find({'sentiment_category': sentiment}))

    def get_section_stats(self, section: str) -> Dict:
        """Get statistics for a section"""
        collection = self.db[section]
        
        stats = {
            'total_posts': collection.count_documents({}),
            'sentiment_distribution': {
                'positive': collection.count_documents({'sentiment_category': 'positive'}),
                'negative': collection.count_documents({'sentiment_category': 'negative'}),
                'neutral': collection.count_documents({'sentiment_category': 'neutral'})
            }
        }
        
        return stats
