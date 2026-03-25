resource "snowflake_warehouse" "airbnb_wh" {
  name           = "AIRBNB_WH"
  warehouse_size = "XSMALL"
  auto_suspend   = 60
  auto_resume    = true
}