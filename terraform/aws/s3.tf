provider "aws" {
    region = "us-east-1"  
}

resource "aws_s3_bucket" "airbnb_bucket" {
  bucket = "airbnb-raw-data-26"

  tags = {
    Name = "Airbnb Raw Data"
    Environment = "Dev"
  }
}

