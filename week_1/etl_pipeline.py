import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import os

# Context-specific logging: avoids "print" for better production tracking
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DataIngestionEngine:
    """
    Automates the Extraction, Transformation, and Loading (ETL) of web data.
    Designed for the ICP-IX8D2E-2026 internship requirements.
    """
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.output_file = "scraped_data_week1.csv"

    def run_extraction(self) -> str:
        # Using a timeout and status check to prevent pipeline hanging
        logger.info(f"Initiating extraction from {self.target_url}")
        response = requests.get(self.target_url, timeout=15)
        response.raise_for_status()
        return response.text

    def run_transformation(self, raw_html: str) -> pd.DataFrame:
        # Enforcing 'Format Consistency' as requested in the Task ID: ICP-IX8D2E-2026
        logger.info("Transforming raw HTML into structured schema...")
        soup = BeautifulSoup(raw_html, 'lxml')
        staging_area = []

        for container in soup.find_all('div', class_='quote'):
            # Cleaning logic: stripping non-standard quotes and whitespace
            text_data = container.find('span', class_='text').get_text(strip=True)
            author_data = container.find('small', class_='author').get_text(strip=True)
            
            staging_area.append({
                "raw_text": text_data.replace('“', '').replace('”', ''),
                "author_name": author_data,
                "ingestion_timestamp": datetime.now().isoformat(),
                "batch_id": "WEEK_01_SCRAPE"
            })
        
        return pd.DataFrame(staging_area)

    def run_loading(self, data_frame: pd.DataFrame):
        # Loading phase: Persists data to the local repository filesystem
        if not data_frame.empty:
            data_frame.to_csv(self.output_file, index=False)
            logger.info(f"ETL Load successful: Saved to {self.output_file}")
        else:
            logger.error("No data found to load.")

if __name__ == "__main__":
    # Target source defined for the Week 1 Project
    engine = DataIngestionEngine("https://quotes.toscrape.com/")
    
    try:
        html_payload = engine.run_extraction()
        structured_df = engine.run_transformation(html_payload)
        engine.run_loading(structured_df)
    except Exception as e:
        logger.critical(f"Pipeline crashed: {str(e)}")
