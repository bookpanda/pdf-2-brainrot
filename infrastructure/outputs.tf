output "bucket_name" {
  value = "${var.bucket_name}-${random_id.bucket_suffix.hex}"
}
