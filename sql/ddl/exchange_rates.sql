CREATE EXTERNAL TABLE IF NOT EXISTS raw_api.exchange_rates (
  currency_code STRING,
  exchange_rate FLOAT,
  date STRING
)
PARTITIONED BY (
  source_name STRING,
  date_partition STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://dev-s3-bucket/api/exchange_rates/';