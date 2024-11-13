# Nairaland Sentiment Analysis Pipeline

## Project Overview

Hello! 😊 Welcome to my **Nairaland Sentiment Analysis Pipeline** project! I'm a beginner in data engineering, and I created this project to dive into various skills needed in data engineering, from data scraping and processing to storage and visualization.

This pipeline gathers posts from [Nairaland](https://www.nairaland.com/), a popular Nigerian forum, processes the text data to analyze sentiments, and then stores and visualizes the results in an interactive dashboard. The project aims to provide insights into public opinions and sentiment trends within various forum sections, such as Politics, Business, and Education.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Modules Overview](#modules-overview)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Future Plans](#future-plans)
7. [Acknowledgments](#acknowledgments)

---

## Features

- **Web Scraping**: Collects data from different sections of Nairaland using an asynchronous scraper.
- **Text Processing**: Cleans and performs sentiment analysis on posts and comments.
- **Data Storage**: Saves processed data into MongoDB for easy retrieval.
- **Data Visualization**: Presents insights through a Streamlit dashboard with interactive charts.
- **Automated Workflow**: Uses GitHub Actions to run the pipeline automatically every 6 hours.

---

## Project Structure

This project is organized into modules to keep everything clear and modular. Here’s a quick overview:

```
nairaland-sentiment-pipeline/
├── scraper/                 # Data scraper module
├── processor/               # Text processing and sentiment analysis
├── database/                # MongoDB data management
├── visualization/           # Streamlit visualization app
├── config/                  # Configuration files
├── .github/                 # GitHub Actions for automation
├── requirements.txt         # Dependencies
└── main.py                  # Main pipeline orchestration script
```

---

## Modules Overview

### 1. **Scraper Module (scraper/scraper.py)**

This module contains a class that fetches posts from Nairaland asynchronously. The asynchronous approach allows efficient data retrieval, even for large volumes, without slowing down the pipeline.

### 2. **Processor Module (processor/text_processor.py)**

Here, posts are cleaned by removing URLs, special characters, and stopwords. It also performs **sentiment analysis** using TextBlob to classify each post as positive, negative, or neutral based on its polarity score.

### 3. **Database Module (database/mongo_handler.py)**

This module manages MongoDB operations, allowing storage and retrieval of posts based on sentiment. It also provides summary statistics for each section.

### 4. **Visualization Module (visualization/streamlit_app.py)**

The Streamlit app presents sentiment insights through an interactive dashboard. Users can see recent posts and sentiment distributions using charts and key metrics.

### 5. **GitHub Actions (.github/workflows/pipeline.yml)**

GitHub Actions automate the pipeline every 6 hours by:

- Checking out the repository
- Setting up Python and installing dependencies
- Running `main.py` to execute the pipeline steps

### 6. **Main Pipeline (main.py)**

This file brings together all modules to run the entire pipeline, including scraping, processing, and storing data. The pipeline is designed to handle errors gracefully, ensuring it runs smoothly without interruptions.

---

## Installation

To get started with this project on your local machine:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Akangbe/Nairaland-Sentiment-Analysis-Pipeline
   cd nairaland-sentiment-pipeline
   ```

2. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**: Ensure MongoDB is installed and running. Update the MongoDB connection settings in the `config/` directory.

---

## Usage

After installation, you can run the pipeline manually to scrape, process, and visualize data.

1. **Run the main pipeline**:

   ```bash
   python main.py
   ```

2. **Launch the Streamlit app**:
   ```bash
   streamlit run visualization/streamlit_app.py
   ```

This will open a local web app where you can explore sentiment insights and recent posts.

---

## Future Plans

- Add NLP enhancements for better sentiment accuracy.
- Integrate more sections from Nairaland for a broader analysis.
- Create historical sentiment trends over time.
- Improve the Streamlit dashboard for even richer data insights.

---

## Acknowledgments

A big thanks to the **Nairaland community** for the data and everyone who has shared their knowledge in data engineering online! 🌟
