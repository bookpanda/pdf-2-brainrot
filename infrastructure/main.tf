resource "random_id" "bucket_suffix" {
  byte_length = 8
}

module "s3" {
  source      = "./modules/s3"
  bucket_name = "${var.bucket_name}-${random_id.bucket_suffix.hex}"
}

module "iam" {
  source        = "./modules/iam"
  bucket_name   = "${var.bucket_name}-${random_id.bucket_suffix.hex}"
  s3_policy_arn = module.s3.s3_policy_arn
}
