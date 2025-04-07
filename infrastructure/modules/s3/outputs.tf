output "s3_policy_arn" {
  value = aws_iam_policy.s3_policy.arn
}

output "bucket_id" {
  value = aws_s3_bucket.uploads.id
}

output "s3_instance_profile_name" {
  value = aws_iam_instance_profile.s3_instance_profile.name
}
