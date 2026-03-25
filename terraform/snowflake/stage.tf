resource "snowflake_stage" "airbnb_stage" {
  name     = "AIRBNB_STAGE"
  database = snowflake_database.airbnb_db.name
  schema   = snowflake_schema.raw_schema.name

  url                 = "s3://airbnb-raw-data-26/raw/"
  storage_integration = snowflake_storage_integration.s3_integration.name


}