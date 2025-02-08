-- Aggregate negative sentiment from 6.6M Dow Jones articles
-- Simulates quarterly sentiment shock index for airline analytics

CREATE OR REPLACE TABLE `your_project.airline_analysis.quarterly_sentiment_summary` AS
WITH base AS (
  SELECT
    PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', publish_date) AS timestamp,
    sentiment_score,
    CASE WHEN sentiment_score < -0.2 THEN 1 ELSE 0 END AS is_negative
  FROM
    `your_project.raw_dowjones.articles`
  WHERE
    LENGTH(article_body) > 300 -- filter out noise
    AND sector = 'aviation'
),
quarterly AS (
  SELECT
    EXTRACT(YEAR FROM timestamp) AS year,
    EXTRACT(QUARTER FROM timestamp) AS quarter,
    COUNT(*) AS total_articles,
    SUM(is_negative) AS negative_articles,
    SAFE_DIVIDE(SUM(is_negative), COUNT(*)) AS negative_ratio,
    AVG(sentiment_score) AS avg_sentiment
  FROM base
  GROUP BY year, quarter
),
with_shocks AS (
  SELECT *,
    CASE
      WHEN negative_ratio > (
        SELECT APPROX_QUANTILES(negative_ratio, 4)[OFFSET(3)]
        FROM quarterly
      ) THEN 1
      ELSE 0
    END AS sentiment_shock
  FROM quarterly
)
SELECT * FROM with_shocks;
