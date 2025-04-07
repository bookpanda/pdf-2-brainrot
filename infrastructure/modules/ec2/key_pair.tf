resource "tls_private_key" "generated_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key_pair" {
  key_name   = "${var.vpc_name}-key"
  public_key = tls_private_key.generated_key.public_key_openssh
}

resource "local_file" "private_key" {
  filename = "${path.root}/${var.vpc_name}-key.pem"
  content  = tls_private_key.generated_key.private_key_pem
}
