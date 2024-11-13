# processor/text_processor.py
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import re
from typing import Dict, List, Union

class TextProcessor:
    def __init__(self):
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    def get_sentiment(self, text: str) -> Dict[str, Union[float, str]]:
        """Analyze sentiment of text using TextBlob"""
        blob = TextBlob(text)
        
        # Get polarity score (-1 to 1)
        polarity = blob.sentiment.polarity
        
        # Get subjectivity score (0 to 1)
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment category
        if polarity > 0:
            category = 'positive'
        elif polarity < 0:
            category = 'negative'
        else:
            category = 'neutral'
            
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'category': category
        }

    def process_post(self, post: Dict) -> Dict:
        """Process a single post including its comments"""
        processed_post = post.copy()
        
        # Clean and analyze main post
        cleaned_text = self.clean_text(post['main_post'])
        sentiment = self.get_sentiment(cleaned_text)
        
        processed_post.update({
            'cleaned_text': cleaned_text,
            'sentiment_polarity': sentiment['polarity'],
            'sentiment_subjectivity': sentiment['subjectivity'],
            'sentiment_category': sentiment['category']
        })
        
        # Process comments
        if isinstance(post['comments'], list):
            processed_comments = []
            for comment in post['comments']:
                if isinstance(comment, dict) and 'text' in comment:
                    cleaned_comment = self.clean_text(comment['text'])
                    comment_sentiment = self.get_sentiment(cleaned_comment)
                    processed_comment = {
                        **comment,
                        'cleaned_text': cleaned_comment,
                        'sentiment_polarity': comment_sentiment['polarity'],
                        'sentiment_subjectivity': comment_sentiment['subjectivity'],
                        'sentiment_category': comment_sentiment['category']
                    }
                    processed_comments.append(processed_comment)
            
            processed_post['processed_comments'] = processed_comments
            
        return processed_post
