resource "aws_iam_role" "snowflake_role" {
    name  = "snowflake_s3_access_role_airbnb"

    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
        Effect = "Allow",
        Principal = {
          AWS = "arn:aws:iam::014974079828:user/bl2h1000-s"
        },
        Action = "sts:AssumeRole",
        Condition = {
          StringEquals = {
            "sts:ExternalId" = "TSB40704_SFCRole=6_M/nPKz8Ub6wFTH/aL8y3omqvOQo="
          }
        }
      }
        ] 
    })
  
}

resource "aws_iam_policy" "s3_policy" {
    name = "snowflake_s3_policy"

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Action = [
                    "s3:ListBucket"
                ],
                Resource = [
                    "arn:aws:s3:::airbnb-raw-data-26"
                ]
            },
            {
                Effect = "Allow",
                Action = [
                "s3:GetObject"
                ],
                Resource = [
                "arn:aws:s3:::airbnb-raw-data-26/*"
                ]
            }
        ]
    })
  
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role = aws_iam_role.snowflake_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_airflow_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_sqs_policy" {
  name = "lambda-sqs-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.airbnb_s3_events_queue.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.airbnb_s3_events_queue.arn
  function_name    = aws_lambda_function.trigger_airflow.arn
  batch_size       = 1
}