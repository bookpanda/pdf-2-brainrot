variable "region" {
  description = "The region in which the VPC will be created"
  type        = string
}

variable "availability_zone" {
  description = "The availability zone in which the VPC will be created"
  type        = string
}

variable "bucket_prefix" {
  description = "The prefix of the name of the S3 bucket"
  type        = string
}

variable "sns_topic_endpoint" {
  description = "The endpoint for the SNS topic to send notifications to"
  type        = string
}

variable "ami" {
  description = "AMI of backend EC2"
  type = string
}