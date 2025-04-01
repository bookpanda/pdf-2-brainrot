output "s3_policy_arn" {
  value = aws_iam_policy.s3_policy.arn
}

output "bucket_id" {
  value = aws_s3_bucket.uploads.id
}
