resource "random_id" "bucket_suffix" {
  byte_length = 8
}

module "s3" {
  source      = "./modules/s3"
  bucket_name = var.bucket_name
}
