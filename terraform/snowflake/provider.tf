terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.98"   # or latest stable
    }
  }
}

provider "snowflake" {
  organization_name = "KFMMUTT"
  account_name = "QAB84166"
  user = "DevanshiKevat"
  password = "Omnamahshivay@9122"
  role     = "ACCOUNTADMIN"
}