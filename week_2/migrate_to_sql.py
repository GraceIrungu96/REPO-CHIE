import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# This line finds your .env file and reads the password
load_dotenv()

def migrate_data():
    conn = None
    try:
        # Instead of the real password, we use os.getenv
        conn = psycopg2.connect(
            dbname="icp_internship_db",
            user="postgres", 
            password=os.getenv("DB_PASSWORD"), 
            host="127.0.0.1",
            port="5432"
        )
        cursor = conn.cursor()

        csv_path = os.path.expanduser("~/REPO-CHIE/week_1/scraped_data_week1.csv")
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            insert_query = "INSERT INTO quotes (author, text) VALUES (%s, %s)"
            cursor.execute(insert_query, (row['author_name'], row['raw_text']))

        conn.commit()
        print("✅ Success! Data is migrated and your password is safe.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    migrate_data()