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

variable "db_password" {
  description = "Password for the RDS PostgreSQL admin user"
  type        = string
  sensitive   = true
}

variable "football_api_key" {
  description = "API Key for raw data"
  type        = string
  sensitive   = true
}