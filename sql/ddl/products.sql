CREATE EXTERNAL TABLE IF NOT EXISTS raw_sql.products (
  product_id INT,
  product_name STRING,
  category STRING,
  price FLOAT,
  stock_available INT
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
LOCATION 's3://dev-s3-bucket/sql/products/';