resource "snowflake_storage_integration" "s3_integration" {
  name                      = "AIRBNB_S3_INT"
  storage_provider          = "S3"
  enabled                   = true
  storage_aws_role_arn      = "arn:aws:iam::507325772253:role/snowflake_s3_access_role_airbnb"
  storage_allowed_locations = ["s3://airbnb-raw-data-26/raw/"]
}