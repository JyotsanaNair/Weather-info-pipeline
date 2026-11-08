# Air Quality Data Pipeline
 
A Python ETL pipeline that pulls current air quality readings (PM2.5, PM10, ozone, NO2, SO2, CO, US AQI, UV index) from the [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api) every 30 minutes and stores them in PostgreSQL.
 
## How it works
1. **Extract**: `fetch_air_quality` calls the API for each location in `LOCATIONS`. Failed calls are logged and skipped.
2. **Transform**: `transform_reading` converts the response into a row with a UTC timestamp.
3. **Load**: rows are inserted with `ON CONFLICT (location, recorded_at) DO NOTHING`, so duplicate readings are skipped.
4. **Schedule**: APScheduler runs the job on start and then every 30 minutes.
## Setup
1. Create a database called `air_quality_db` and run `air_quality_readings.sql`.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your database password (and optionally `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`):
   - macOS/Linux: `export DB_PASSWORD=your_password`
   - Windows PowerShell: `$env:DB_PASSWORD="your_password"`
4. Run: `python pipeline.py`
## Future steps
- More locations
- Charts of readings over time
- Simple forecasting model
