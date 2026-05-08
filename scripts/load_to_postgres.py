import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

def load_data():
    # 1. Load the cleaned dataset
    csv_path = r'c:\Users\Pranav\OneDrive\PROJECT AND PRESENTATIONS\PROJECTS AND PRESENTATIONS\Athlete Training Analysis\datasets\cleaned_athlete_data.csv'
    df = pd.read_csv(csv_path)

    # 2. Clean column names for SQL compatibility
    df.columns = [col.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_per_') for col in df.columns]

    # 3. Database connection parameters
    # Replace these with your actual PostgreSQL credentials
    DB_USER = "postgres"
    DB_PASSWORD = "Pranav2004"
    DB_HOST = "localhost"
    DB_PORT =  "5522"
    DB_NAME = "Athlete"

    try:
        # 4. Create SQLAlchemy engine
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        # 5. Load data into PostgreSQL
        print(f"Loading data into table 'athlete_training' in database '{DB_NAME}'...")
        df.to_sql('athlete_training', engine, if_exists='replace', index=False)
        print("Data loaded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    load_data()
