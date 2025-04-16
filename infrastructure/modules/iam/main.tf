resource "aws_iam_user" "user" {
  name = "pdf2br-user"
}

resource "aws_iam_policy_attachment" "s3_policy_attachment" {
  name       = "pdf2br-user-policy-attachment"
  policy_arn = var.s3_policy_arn
  users      = [aws_iam_user.user.name]
}

resource "aws_iam_access_key" "user_access_key" {
  user = aws_iam_user.user.name
}
