provider "aws" {
  region = "us-east-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  owners = ["099720109477"]
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "prem_analytics_vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.102.0/24", "10.0.103.0/24", "10.0.104.0/24"]

  enable_nat_gateway      = false
  single_nat_gateway      = false
  map_public_ip_on_launch = true

  tags = {
    Project     = "Prem_Analytics"
    Terraform   = "true"
    Environment = "dev"
    Owner       = "Mantavya"
  }
}

resource "aws_key_pair" "prem_analytics" {
  key_name = "prem_analytics_key"

  public_key = file("~/.ssh/id_ed25519.pub")
}

resource "aws_security_group" "prem_analytics_sg" {
  name        = "prem-analytics-sg"
  description = "security group for the prem analytics platform"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name        = "prem_analytics_sg"
    Project     = "Prem_Analytics"
    Environment = "dev"
    Owner       = "Mantavya"
  }
}

resource "aws_security_group_rule" "ssh_ingress" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  security_group_id = aws_security_group.prem_analytics_sg.id
  cidr_blocks       = ["142.189.201.143/32"]
}

resource "aws_security_group_rule" "flask_ingress" {
  type              = "ingress"
  from_port         = 5000
  to_port           = 5000
  protocol          = "tcp"
  security_group_id = aws_security_group.prem_analytics_sg.id
  cidr_blocks       = ["142.189.201.143/32"]
}

resource "aws_security_group_rule" "all_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.prem_analytics_sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_instance" "prem_analytics_server" {
  ami = data.aws_ami.ubuntu.id

  instance_type = var.instance_type

  vpc_security_group_ids = [
    aws_security_group.prem_analytics_sg.id
  ]

  subnet_id = module.vpc.public_subnets[0]

  associate_public_ip_address = true

  key_name = aws_key_pair.prem_analytics.key_name

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  user_data = file("${path.module}/scripts/bootstrap.sh")

  tags = {
    Project     = "Prem_Analytics"
    Environment = "dev"
    Owner       = "Mantavya"
    Terraform   = "true"
    Name        = var.instance_name
  }
}