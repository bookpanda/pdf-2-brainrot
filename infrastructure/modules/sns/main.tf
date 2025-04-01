resource "aws_sns_topic" "s3_uploads" {
  name = "s3-uploads-topic"
}

resource "aws_sns_topic_policy" "s3_sns_policy" {
  arn = aws_sns_topic.s3_uploads.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "SNS:Publish"
        Resource  = aws_sns_topic.s3_uploads.arn
        Condition = {
          ArnLike = {
            "aws:SourceArn" = "arn:aws:s3:::${var.bucket_name}"
          }
        }
      }
    ]
  })
}

resource "aws_s3_bucket_notification" "s3_to_sns" {
  bucket = var.bucket_id

  topic {
    topic_arn = aws_sns_topic.s3_uploads.arn
    events    = ["s3:ObjectCreated:*"]
  }
}

resource "aws_sns_topic_subscription" "sns_to_backend" {
  topic_arn = aws_sns_topic.s3_uploads.arn
  protocol  = "https"
  endpoint  = var.sns_topic_endpoint
}
