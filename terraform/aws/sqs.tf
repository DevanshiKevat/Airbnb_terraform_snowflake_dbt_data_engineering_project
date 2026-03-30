resource "aws_sqs_queue" "airbnb_s3_events_queue" {
  name = "airbnb-s3-events-queue"

  visibility_timeout_seconds = 300
  message_retention_seconds  = 86400
}

resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.airbnb_s3_events_queue.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid = "AllowS3SendMessage",   # ✅ add SID
        Effect = "Allow",
        Principal = {
          Service = "s3.amazonaws.com"
        },
        Action = "SQS:SendMessage",
        Resource = aws_sqs_queue.airbnb_s3_events_queue.arn,
        Condition = {
          ArnEquals = {   # ✅ CHANGE THIS
            "aws:SourceArn" = aws_s3_bucket.airbnb_bucket.arn
          }
        }
      }
    ]
  })
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.airbnb_bucket.id

  queue {
    queue_arn = "arn:aws:sqs:us-east-1:507325772253:airbnb-s3-events-queue"
    events    = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_sqs_queue_policy.allow_s3   
  ]
}
