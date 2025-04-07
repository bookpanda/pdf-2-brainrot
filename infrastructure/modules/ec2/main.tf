resource "aws_network_interface" "eni_backend_inet" {
  subnet_id       = var.backend_inet_id
  private_ips     = ["10.0.1.100"] # static private IP, must be within the backend_inet subnet CIDR range
  security_groups = [aws_security_group.sg_backend_inet.id]
  tags = {
    Name = "${var.vpc_name}-backend-inet-eni"
  }
}

resource "aws_eip" "backend_inet_eip" {
  tags = {
    Name = "${var.vpc_name}-backend-inet-eip"
  }
}

resource "aws_eip_association" "backend_inet_eip_assoc" {
  allocation_id        = aws_eip.backend_inet_eip.id
  network_interface_id = aws_network_interface.eni_backend_inet.id
}

resource "aws_instance" "backend" {
  ami           = var.ami
  instance_type = "t2.micro"

  network_interface {
    network_interface_id = aws_network_interface.eni_backend_inet.id
    device_index         = 0
  }

  iam_instance_profile = var.s3_instance_profile_name
  key_name = aws_key_pair.generated_key_pair.key_name
  user_data = data.template_file.user_data.rendered

  tags = {
    Name = "${var.vpc_name}-backend"
  }
}

data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")
  vars = {
    APP_NAME        = "${var.app_name}"
    PORT            = "${var.app_port}"
    AWS_REGION      = "${var.region}"
    AWS_BUCKET_NAME = "${var.bucket_name}"
    GITHUB_REPO     = "${var.github_repo}"
  }
}

resource "aws_security_group" "sg_backend_inet" {
  name        = "sg_backend_inet"
  description = "Security group for backend_inet subnet and EC2 instances"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}
