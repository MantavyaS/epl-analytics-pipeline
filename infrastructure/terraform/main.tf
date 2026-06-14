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

// ec2 instance

resource "aws_instance" "prem_analytics_server" {
  ami = data.aws_ami.ubuntu.id

  instance_type = var.instance_type

  vpc_security_group_ids = [
    aws_security_group.prem_analytics_sg.id
  ]

  subnet_id = module.vpc.public_subnets[0]

  associate_public_ip_address = true

  key_name = aws_key_pair.prem_analytics.key_name

  iam_instance_profile = aws_iam_instance_profile.prem_analytics_instance_profile.name

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

// RDS Instance

resource "aws_db_subnet_group" "prem_analytics_db_subnet" {
  name       = "prem_analytics_db_subnet"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Project     = "Prem_Analytics"
    Terraform   = "true"
    Environment = "dev"
    Owner       = "Mantavya"
  }
}

resource "aws_db_instance" "prem-analytics-db" {
  identifier = "prem-analytics-db"

  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.t3.micro"

  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = "prem_analytics"
  username = "premadmin"
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.prem_analytics_db_subnet.name
  vpc_security_group_ids = [aws_security_group.prem_analytics_rds_sg.id]

  publicly_accessible = false
  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Project     = "Prem_Analytics"
    Terraform   = "true"
    Environment = "dev"
    Owner       = "Mantavya"
  }
}

resource "aws_security_group" "prem_analytics_rds_sg" {
  name        = "prem_analytics_rds_sg"
  description = "Security group for the RDS database"

  vpc_id = module.vpc.vpc_id

  tags = {
    Name        = "prem_analytics_rds_sg"
    Project     = "Prem_Analytics"
    Environment = "dev"
    Owner       = "Mantavya"
  }
}

resource "aws_security_group_rule" "rds_ingress_from_ec2" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.prem_analytics_rds_sg.id
  source_security_group_id = aws_security_group.prem_analytics_sg.id
}

resource "aws_security_group_rule" "rds_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.prem_analytics_rds_sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}

// iam role

resource "aws_iam_role" "prem_analytics_ec2_role" {
  name = "prem_analytics_ec2_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name        = "prem_analytics_ec2-role"
    Project     = "Prem_Analytics"
    Environment = "dev"
    Owner       = "Mantavya"
  }
}

resource "aws_iam_role_policy" "prem_analytics_secrets_policy" {
  name = "prem-analytics-secrets-read-policy"
  role = aws_iam_role.prem_analytics_ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Effect   = "Allow"
        Resource = aws_secretsmanager_secret.prem_analytics_db.arn
      },
    ]
  })

}

resource "aws_iam_instance_profile" "prem_analytics_instance_profile" {
  name = "prem_analytics_instance_profile"
  role = aws_iam_role.prem_analytics_ec2_role.name
}

// secrets - decided against using but keeping for reference purposes

resource "aws_secretsmanager_secret" "prem_analytics_db" {
  name = "prem-analytics/database"

  tags = {
    Project     = "Prem_Analytics"
    Environment = "dev"
    Owner       = "Mantavya"
  }
}

resource "aws_secretsmanager_secret_version" "prem_analytics_db_version" {
  secret_id = aws_secretsmanager_secret.prem_analytics_db.id

  secret_string = jsonencode({
    API_KEY     = var.football_api_key
    BASE_URL    = "https://api.football-data.org/v4"
    DB_NAME     = "prem_analytics"
    DB_USER     = "premadmin"
    DB_PASSWORD = var.db_password
    DB_HOST     = aws_db_instance.prem-analytics-db.address
    DB_PORT     = 5432
  })
}

// monitoring - alarms

resource "aws_sns_topic" "prem_analytics_alerts" {
  name = "prem-analytics-alerts"
}

resource "aws_cloudwatch_metric_alarm" "ec2_high_cpu" {
  alarm_name          = "prem-analytics-ec2-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80

  dimensions = {
    InstanceId = aws_instance.prem_analytics_server.id
  }

  alarm_actions = [aws_sns_topic.prem_analytics_alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "rds-high-cpu" {
  alarm_name          = "prem-analytics-rds-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.prem-analytics-db.id
  }

  alarm_actions = [aws_sns_topic.prem_analytics_alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "rds_low_storage" {
  alarm_name          = "prem-analytics-rds-low-storage"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 5000000000

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.prem-analytics-db.id
  }

  alarm_actions = [aws_sns_topic.prem_analytics_alerts.arn]
}