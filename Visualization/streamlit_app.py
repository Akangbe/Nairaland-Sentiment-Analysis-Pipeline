# visualization/streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objects as go
from typing import Dict

class DashboardApp:
    def __init__(self, mongo_handler):
        self.mongo_handler = mongo_handler
        st.set_page_config(page_title="Nairaland Analysis", layout="wide")

    def run(self):
        st.title("Nairaland Data Analysis Dashboard")
        
        # Sidebar for filtering
        st.sidebar.title("Filters")
        sections = ["Politics", "Business", "Crime", "NYSC", "Education", "Food", "Romance"]
        selected_section = st.sidebar.selectbox("Select Section", sections)
        
        # Get statistics for selected section
        stats = self.mongo_handler.get_section_stats(selected_section)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Posts", stats['total_posts'])
        with col2:
            st.metric("Positive Posts", stats['sentiment_distribution']['positive'])
        with col3:
            st.metric("Negative Posts", stats['sentiment_distribution']['negative'])
        
        # Sentiment Distribution Plot
        sentiment_data = pd.DataFrame({
            'Sentiment': ['Positive', 'Negative', 'Neutral'],
            'Count': [
                stats['sentiment_distribution']['positive'],
                stats['sentiment_distribution']['negative'],
                stats['sentiment_distribution']['neutral']
            ]
        })
        
        fig = px.pie(
            sentiment_data, 
            values='Count', 
            names='Sentiment',
            title=f'Sentiment Distribution - {selected_section}'
        )
        st.plotly_chart(fig)
        
        # Display recent posts
        st.subheader("Recent Posts")
        recent_posts = list(self.mongo_handler.db[selected_section]
                          .find()
                          .sort('inserted_at', -1)
                          .limit(5))
        
        for post in recent_posts:
            with st.expander(f"{post['title'][:100]}..."):
                st.write(f"Sentiment: {post['sentiment_category']}")
                st.write(f"Polarity: {post['sentiment_polarity']:.2f}")
                st.write(f"Content: {post['cleaned_text'][:200]}...")