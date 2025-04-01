resource "aws_iam_user" "user" {
  name = "pdf2br-user"
}

# resource "aws_iam_policy" "s3_user_policy" {
#   name        = "s3-access-policy-${var.bucket_name}"
#   description = "Policy to allow access to the S3 bucket"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = [
#           "s3:GetObject",
#           "s3:PutObject",
#           "s3:ListBucket"
#         ]
#         Effect = "Allow"
#         Resource = [
#           "arn:aws:s3:::${aws_s3_bucket.uploads.bucket}",
#           "arn:aws:s3:::${aws_s3_bucket.uploads.bucket}/*"
#         ]
#       }
#     ]
#   })
# }

resource "aws_iam_policy_attachment" "user_policy_attachment" {
  name       = "pdf2br-user-policy-attachment"
  policy_arn = var.s3_policy_arn
  users      = [aws_iam_user.user.name]
}

resource "aws_iam_access_key" "user_access_key" {
  user = aws_iam_user.user.name
}
