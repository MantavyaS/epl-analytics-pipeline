# Prem Analytics Platform | AWS • Terraform • Docker • PostgreSQL • CI/CD

A production-style cloud analytics platform that ingests live Premier League data, transforms it through an automated ETL pipeline, stores it in Amazon RDS PostgreSQL, and exposes advanced football analytics through a Flask REST API.

This project was built to demonstrate practical Cloud Engineering, DevOps, Infrastructure as Code, Data Engineering, Backend Development, and AWS Architecture skills through the design and deployment of a complete end-to-end platform.

---

## Project Highlights

* Provisioned an entire AWS environment using Terraform
* Designed secure VPC networking with public and private subnets
* Deployed Dockerized services on AWS EC2
* Built an automated ETL pipeline for football analytics data
* Implemented GitHub Actions CI/CD deployments
* Secured infrastructure using IAM Roles and AWS Secrets Manager
* Configured CloudWatch monitoring and alerting
* Designed PostgreSQL schemas optimized for analytical workloads
* Implemented a private database architecture with zero public exposure

**Tech Stack:** AWS • Terraform • Docker • Python • Flask • PostgreSQL • GitHub Actions • CloudWatch

---

## Architecture Overview

The platform follows a secure two-tier AWS architecture.

The application layer runs inside Docker containers hosted on an EC2 instance within a public subnet. One container serves the Flask REST API while the second container executes the ETL pipeline.

The data layer is isolated inside private subnets using Amazon RDS PostgreSQL. Database access is restricted exclusively to the EC2 instance through tightly controlled security group rules.

The result is a production-style deployment architecture that separates application and database concerns while enforcing strong security boundaries.

![High Level Architecture](images/high_level_architecture.png)

---

## End-to-End Data Flow

1. The ETL container requests data from the Football-Data.org API.
2. Raw JSON responses are downloaded and validated.
3. Nested API data is transformed into relational structures.
4. Processed records are loaded into Amazon RDS PostgreSQL.
5. The Flask API executes analytical SQL queries against the database.
6. Results are returned through REST endpoints.
7. CloudWatch continuously monitors infrastructure health and performance.

---

## AWS Infrastructure

All AWS resources are provisioned through Terraform. No infrastructure components were created manually through the AWS Console.

The infrastructure can be recreated at any time using a single Terraform deployment.

### Infrastructure Components

| Resource         | Purpose                      |
| ---------------- | ---------------------------- |
| VPC              | Isolated network environment |
| Public Subnets   | Application hosting layer    |
| Private Subnets  | Database layer               |
| Internet Gateway | Internet connectivity        |
| Route Tables     | Traffic routing              |
| Security Groups  | Network access control       |
| EC2 Instance     | Docker application host      |
| RDS PostgreSQL   | Managed relational database  |
| IAM Role         | Secure AWS access            |
| Secrets Manager  | Credential management        |
| CloudWatch       | Monitoring and alerting      |

### Infrastructure Diagram

![Low Level Architecture](images/low_level_architecture.png)

---

## Security Design

Security was treated as a primary design objective throughout the project.

### Private Database Architecture

Amazon RDS is deployed inside private subnets and is not publicly accessible.

Only the EC2 security group is permitted to establish database connections on port 5432. There is no direct path from the public internet to the database.

### IAM-Based Access Control

The EC2 instance uses an IAM role rather than static AWS credentials.

This enables secure interaction with AWS services while eliminating credential management risks.

### Secrets Management

Database credentials are stored using AWS Secrets Manager rather than environment files or source code.

### Encryption

* RDS storage encrypted at rest
* EBS storage encrypted at rest
* Secrets encrypted within Secrets Manager

---

## Data Engineering Pipeline

The ETL pipeline runs as an independent Docker container and is responsible for acquiring, transforming, and loading football data into PostgreSQL.

### Data Sources

Data is retrieved from the Football-Data.org API.

### Data Processed

* Premier League standings
* Historical matchday standings
* Team statistics
* Top scorer information
* Goals scored
* Assists
* Appearances

### Database Design

The database schema is optimized for analytical workloads rather than simple data storage.

This enables efficient querying of:

* Position movement over time
* Points accumulation
* Attacking performance
* Defensive performance
* Player efficiency metrics

### Database Schema

#### Rolling Standings

![Rolling Standings Schema](images/rolling_standings_schema.png)

#### Top Scorers

![Top Scorers Schema](images/topscorers_schema.png)

#### PostgreSQL Tables

![Postgres Tables](images/postgres_tables.png)

---

## REST API

The platform exposes analytical insights through a Flask-based REST API.

The API connects directly to Amazon RDS PostgreSQL using Psycopg2 and serves pre-computed analytics.

### Available Endpoints

| Endpoint                | Description                             |
| ----------------------- | --------------------------------------- |
| `/`                     | Health check                            |
| `/best-attack`          | Teams ranked by goals scored per game   |
| `/best-defence`         | Teams ranked by goals conceded per game |
| `/points-gained`        | Points gained across matchdays          |
| `/topscorer-efficiency` | Goal contributions per match            |

### API Demonstration

#### Health Endpoint

![Health](images/flask_api_health.png)

#### Best Attack

![Best Attack](images/flask_api_best_attack.png)

#### Best Defence

![Best Defence](images/flask_api_best_defence.png)

#### Points Gained

![Points Gained](images/flask_api_points_gained.png)

#### Top Scorer Efficiency

![Top Scorer Efficiency](images/flask_api_topscorer_efficiency.png)

---

## Docker Deployment

The platform is fully containerized.

Two Docker containers run on the EC2 instance:

### Flask API Container

Responsible for serving REST endpoints and handling database interactions.

### ETL Container

Responsible for fetching, transforming, and loading football data.

### Docker Runtime

![Docker PS](images/docker_ps.png)

---

## CI/CD Pipeline

Deployment is fully automated using GitHub Actions.

Whenever code is pushed to the main branch:

1. GitHub Actions executes the deployment workflow.
2. The workflow connects to EC2 via SSH.
3. The latest repository changes are pulled.
4. Docker containers are rebuilt and restarted.
5. The updated platform becomes live.

No manual deployment steps are required.

### GitHub Actions Workflow

![GitHub Actions](images/github_actions_success.png)

---

## Monitoring & Observability

AWS CloudWatch is configured to monitor both the application host and the database layer.

Alarms provide visibility into infrastructure health and help detect issues before they impact users.

### Metrics Monitored

* EC2 CPU Utilization
* EC2 Status Checks
* RDS CPU Utilization
* RDS Free Storage
* Database Health

### CloudWatch Monitoring

![CloudWatch Alarms](images/cloudwatch_alarm.png)

![CloudWatch RDS Alarms](images/cloudwatch_rds_alarms.png)

---

## Infrastructure Screenshots

### VPC & Networking

![VPC](images/vpc.png)

![VPC Resource Map](images/vpc_resourceMap1.png)

![VPC Resource Map Detail](images/vpc_resourceMap2.png)

### EC2

![EC2 Instance Console](images/ec2_instance_console.png)

![EC2 Network](images/ec2_network.png)

![EC2 Status Checks](images/ec2_status_checks.png)

### Security Groups

![Security Groups](images/security_groups.png)

#### EC2 Inbound Rules

![EC2 SG Inbound](images/ec2_sg_in.png)

#### EC2 Outbound Rules

![EC2 SG Outbound](images/ec2_sg_e.png)

#### RDS Inbound Rules

![RDS SG Inbound](images/rds_sg_in.png)

#### RDS Outbound Rules

![RDS SG Outbound](images/rds_sg_e.png)

### IAM & Secrets Manager

![IAM EC2 Role](images/iam_ec2Role.png)

![Secrets Manager](images/secrets_manager.png)

### RDS PostgreSQL

![RDS Database](images/rds_db.png)

![RDS Connectivity](images/rds_connection.png)

---

## Project Metrics

* 100% Infrastructure Provisioned Through Terraform
* 2 Dockerized Services
* 5 Analytics API Endpoints
* Multi-Tier AWS Architecture
* Private RDS Deployment
* Automated CI/CD Pipeline
* CloudWatch Monitoring & Alerting
* Infrastructure Fully Reproducible From Code

---

## Technology Stack

| Category               | Technologies                                                   |
| ---------------------- | -------------------------------------------------------------- |
| Cloud                  | AWS EC2, RDS PostgreSQL, VPC, IAM, Secrets Manager, CloudWatch |
| Infrastructure as Code | Terraform                                                      |
| Backend                | Python, Flask, Psycopg2                                        |
| Database               | PostgreSQL                                                     |
| Data Engineering       | ETL Pipelines, JSON Transformation                             |
| Containerization       | Docker, Docker Compose                                         |
| CI/CD                  | GitHub Actions                                                 |
| Source Control         | Git & GitHub                                                   |

---

## Project Structure

```text
Project1/
├── analytics/
│   ├── best_attack.py
│   ├── best_defence.py
│   ├── points_gained.py
│   └── topscorer_efficiency.py
├── app/
│   ├── __init__.py
│   └── routes.py
├── database/
│   ├── db.py
│   └── insert_data.py
├── fetchers/
├── transformers/
├── infrastructure/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── scripts/
│           └── bootstrap.sh
├── Dockerfile
├── docker-compose.yml
├── aws-compose.yaml
└── requirements.txt
```

---

## What This Project Demonstrates

This project demonstrates the ability to design, provision, deploy, secure, monitor, and operate a production-style cloud application from scratch.

Key concepts explored include:

* AWS Infrastructure Design
* Infrastructure as Code
* Network Security
* Docker Containerization
* Data Engineering
* PostgreSQL Database Design
* CI/CD Automation
* Monitoring & Observability
* Backend API Development
* Cloud Architecture Best Practices

The objective was not simply to build an application, but to gain practical experience with the tools and patterns commonly used by Cloud Engineers, DevOps Engineers, Site Reliability Engineers, and Infrastructure Engineers in production environments.
