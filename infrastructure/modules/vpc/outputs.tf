output "vpc_id" {
  value = aws_vpc.main.id
}

output "vpc_name" {
  value = var.vpc_name
}

output "igw_id" {
  value = aws_internet_gateway.igw.id
}

output "backend_inet_id" {
  value = aws_subnet.backend_inet.id
}
