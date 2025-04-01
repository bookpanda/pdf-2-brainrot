provider "aws" {
  region = "pdf-to-brainrot-${random_id.bucket_suffix.hex}"
}
