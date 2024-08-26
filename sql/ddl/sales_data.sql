CREATE EXTERNAL TABLE IF NOT EXISTS raw_files.sales_data (
  transaction_id INT,
  product_id INT,
  quantity INT,
  price FLOAT,
  transaction_date STRING
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
LOCATION 's3://dev-s3-bucket/files/sales_data/';