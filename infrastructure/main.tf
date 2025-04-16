resource "random_id" "bucket_suffix" {
  byte_length = 8
}

locals {
  bucket_name = "${var.bucket_prefix}-${random_id.bucket_suffix.hex}"
}

module "s3" {
  source      = "./modules/s3"
  bucket_name = local.bucket_name
}

module "sns" {
  source             = "./modules/sns"
  bucket_name        = local.bucket_name
  bucket_id          = module.s3.bucket_id
  sns_topic_endpoint = "${var.sns_topic_endpoint}/sns/webhook"
}

module "iam" {
  source        = "./modules/iam"
  bucket_name   = local.bucket_name
  s3_policy_arn = module.s3.s3_policy_arn
}

# module "vpc" {
#   source            = "./modules/vpc"
#   availability_zone = var.availability_zone
# }

# module "ec2" {
#   source                   = "./modules/ec2"
#   ami                      = var.ami
#   region                   = var.region
#   app_name                 = var.app_name
#   app_port                 = var.app_port
#   bucket_name              = local.bucket_name
#   vpc_id                   = module.vpc.vpc_id
#   vpc_name                 = module.vpc.vpc_name
#   backend_inet_id          = module.vpc.backend_inet_id
#   s3_instance_profile_name = module.s3.s3_instance_profile_name
# }
