CREATE EXTERNAL TABLE IF NOT EXISTS raw_api.customer_data (
  customer_id INT,
  customer_name STRING,
  age INT,
  gender STRING,
  location STRING,
  date_joined STRING
)
PARTITIONED BY (
  source_name STRING,
  date_partition STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://dev-s3-bucket/api/customer_data/';