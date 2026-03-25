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