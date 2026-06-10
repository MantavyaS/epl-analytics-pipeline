variable "instance_type" {
  description = "type of ec2 instance"
  type        = string
  default     = "t3.micro"
}

variable "instance_name" {
  description = "name of the ec2 instance"
  type        = string
  default     = "prem_analytics_server"
}