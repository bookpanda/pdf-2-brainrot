output "bucket_name" {
  value = "${var.bucket_name}-${random_id.bucket_suffix.hex}"
}

output "access_key_id" {
  value = module.iam.access_key_id
}

output "secret_access_key" {
  value     = module.iam.secret_access_key
  sensitive = true
}
