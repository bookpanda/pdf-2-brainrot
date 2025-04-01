
output "access_key_id" {
  value = module.iam.access_key_id
}

output "secret_access_key" {
  value     = module.iam.secret_access_key
  sensitive = true
}

output "region" {
  value = var.region
}

output "bucket_name" {
  value = local.bucket_name
}
