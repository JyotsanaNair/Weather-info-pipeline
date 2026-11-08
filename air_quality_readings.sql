CREATE TABLE IF NOT EXISTS public.air_quality_readings (
	id SERIAL PRIMARY KEY,
	location varchar(100) not null,
	latitude float,
	longitude float,
	recorded_at timestamptz not null,
	pm2_5 float,
	pm10 float,
	ozone float,
	nitrogen_dioxide float,
	sulphur_dioxide float,
	carbon_monoxide float,
	us_aqi int,
	uv_index float,
	inserted_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_air_quality_location_time
	ON public.air_quality_readings (location, recorded_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS idx_air_quality_unique_reading
	ON public.air_quality_readings (location, recorded_at);

SELECT * FROM air_quality_readings;