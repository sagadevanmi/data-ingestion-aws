CREATE EXTERNAL TABLE IF NOT EXISTS raw_sql.transactions (
  transaction_id INT,
  customer_id INT,
  product_id INT,
  quantity INT,
  transaction_date STRING,
  total_amount FLOAT
)
PARTITIONED BY (
  source_name STRING,
  date_partition STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '"'
)
STORED AS TEXTFILE
LOCATION 's3://dev-s3-bucket/sql/transactions/';