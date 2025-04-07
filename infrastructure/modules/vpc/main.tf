resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = var.vpc_name
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

resource "aws_subnet" "backend_inet" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = var.availability_zone
  tags = {
    Name = "backend-inet"
  }
}

resource "aws_route_table" "backend_inet_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = var.vpc_cidr
    gateway_id = "local"
  }
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "Public RT for backend-inet"
  }
}

resource "aws_route_table_association" "app_inet_association" {
  subnet_id      = aws_subnet.backend_inet.id
  route_table_id = aws_route_table.backend_inet_rt.id
}