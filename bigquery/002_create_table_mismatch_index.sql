CREATE OR REPLACE TABLE `aviation-analysis.aviation_data_2010_2024.mismatch_index_table` AS
SELECT
  YEAR,
  QUARTER,
  ROUTE_KEY,
  CARRIER,
  ORIGIN,
  DEST,
  REGION,
  DISTANCE_GROUP,
  T100_SEATS,
  DB1B_PASSENGERS,
  SAFE_DIVIDE(T100_SEATS, DB1B_PASSENGERS * 10) AS mismatch_index,
  SAFE_DIVIDE(DB1B_PASSENGERS, T100_SEATS) AS load_factor_proxy,
  CASE
    WHEN SAFE_DIVIDE(T100_SEATS, DB1B_PASSENGERS * 10) < 0.5 THEN 'Undersupplied'
    WHEN SAFE_DIVIDE(T100_SEATS, DB1B_PASSENGERS * 10) > 1.5 THEN 'Oversupplied'
    ELSE 'Balanced'
  END AS mismatch_bucket
FROM `aviation-analysis.aviation_data_2010_2024.raw_data`
WHERE 
  CLASS IN ('A', 'C', 'E', 'F')         -- Keep only scheduled passenger flights
  AND AIRCRAFT_CONFIG = 1              -- Only passenger-configured aircraft
  AND T100_SEATS > 0                   -- Valid denominator
  AND DB1B_PASSENGERS IS NOT NULL      -- Must have demand signal
