output "backend_ip" {
  value = aws_eip.backend_inet_eip.public_ip
}