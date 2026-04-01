resource "aws_lambda_function" "trigger_airflow" {
  function_name = "trigger-airflow-dag"

  filename         = "${path.module}/lambda/lambda.zip"
  handler          = "lambda_trigger.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_role.arn

  source_code_hash = filebase64sha256("${path.module}/lambda/lambda.zip")

  environment {
    variables = {
      AIRFLOW_URL      = "http://<your-ip>:8080"
      AIRFLOW_USERNAME = "admin"
      AIRFLOW_PASSWORD = "admin"
    }
  }
}