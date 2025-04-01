resource "aws_s3_bucket" "uploads" {
  bucket        = var.bucket_name
  force_destroy = true
  tags = {
    Name = "pdf2br-uploads"
  }
}

resource "aws_s3_bucket_ownership_controls" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_public_access_block" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "uploads_acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.uploads,
    aws_s3_bucket_public_access_block.uploads,
  ]

  bucket = aws_s3_bucket.uploads.id
  acl    = "public-read"
}

resource "aws_iam_policy" "s3_policy" {
  name        = "pdf2br-s3-policy"
  description = "Policy to allow access to the S3 bucket"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect = "Allow"
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.uploads.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.uploads.bucket}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role" "s3_instance_role" {
  name = "${var.bucket_name}-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  policy_arn = aws_iam_policy.s3_policy.arn
  role       = aws_iam_role.s3_instance_role.name
}

resource "aws_iam_instance_profile" "s3_instance_profile" {
  name = "${var.bucket_name}-instance-profile"
  role = aws_iam_role.s3_instance_role.name
}
