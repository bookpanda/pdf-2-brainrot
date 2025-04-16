resource "aws_iam_policy" "textract_policy" {
  name        = "TextractPermissions"
  description = "Permissions to use AWS Textract for text detection"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "textract:StartDocumentTextDetection",
          "textract:GetDocumentTextDetection"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "polly_policy" {
  name        = "PollyPermissions"
  description = "Permissions to use AWS Polly for speech synthesis"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "polly:StartSpeechSynthesisTask",
          "polly:GetSpeechSynthesisTask",
          "polly:SynthesizeSpeech"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}
resource "aws_iam_policy_attachment" "textract_policy_attachment" {
  name       = "textract-policy-attachment"
  policy_arn = aws_iam_policy.textract_policy.arn
  users      = [aws_iam_user.user.name]
  depends_on = [aws_iam_user.user]
}

resource "aws_iam_policy_attachment" "polly_policy_attachment" {
  name       = "polly-policy-attachment"
  policy_arn = aws_iam_policy.polly_policy.arn
  users      = [aws_iam_user.user.name]
  depends_on = [aws_iam_user.user]
}
