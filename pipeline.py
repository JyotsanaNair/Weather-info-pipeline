import requests #to retrieve the data from the api
import os #to get the environment variables
from datetime import datetime, timezone # to transform the data
import psycopg2 #to load data into PostgreSQL
from apscheduler.schedulers.blocking import BlockingScheduler #to do the scheduling

from dotenv import load_dotenv
load_dotenv()

def fetch_air_quality(location):
    # fetch current air quality for one location
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude" : location["latitude"],
        "longitude" : location["longitude"],
        "current" : "pm2_5,pm10,ozone,nitrogen_dioxide,sulphur_dioxide,carbon_monoxide,us_aqi,uv_index"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data["current"]
    else:
        return None


def transform_reading(location, current):
    recorded_at = datetime.fromisoformat(current["time"]).replace(tzinfo=timezone.utc)

    return(
        location["name"],
        location["latitude"],
        location["longitude"],
        recorded_at,
        current["pm2_5"],
        current["pm10"],
        current["ozone"],
        current["nitrogen_dioxide"],
        current["sulphur_dioxide"],
        current["carbon_monoxide"],
        current["us_aqi"],
        current["uv_index"],
    )

DB_CONFIG = {
    "host" : os.environ.get("DB_HOST", "localhost"),
    "port" : os.environ.get("DB_PORT", "5432"),
    "dbname" : os.environ.get("DB_NAME", "air_quality_db"),
    "user" : os.environ.get("DB_USER", "postgres"),
    "password" : os.environ.get("DB_PASSWORD")
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()


insert_query = """
    INSERT INTO air_quality_readings 
        (location, latitude, longitude,recorded_at, pm2_5 ,
        pm10 ,ozone, nitrogen_dioxide, sulphur_dioxide, carbon_monoxide, us_aqi, uv_index )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

def run_pipeline():
    sydney = {"name": "Sydney", "latitude": -33.87, "longitude": 151.21}
    result = fetch_air_quality(sydney)
    row = transform_reading(sydney, result)

    try:
        cur.execute(insert_query, row)
        conn.commit()
        print("Inserted a reading.")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Reading already exists for this timestamp, skipping.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, "interval", minutes= 30, next_run_time = datetime.now(timezone.utc))
    scheduler.start()
