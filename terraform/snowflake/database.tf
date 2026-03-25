resource "snowflake_database" "airbnb_db" {
  name = "AIRBNB_DB"
}

resource "snowflake_schema" "raw_schema" {
  name     = "RAW"
  database = snowflake_database.airbnb_db.name
}