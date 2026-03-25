resource "snowflake_file_format" "csv_format" {
  name     = "AIRBNB_CSV_FORMAT"
  database = snowflake_database.airbnb_db.name
  schema   = snowflake_schema.raw_schema.name
  format_type = "CSV"

    field_delimiter = ","
    parse_header    = true

    field_optionally_enclosed_by = "\""
    trim_space = true
    error_on_column_count_mismatch = false
    

}

