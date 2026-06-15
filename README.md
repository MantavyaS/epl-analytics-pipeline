# Prem Analytics Platform

A cloud-native Premier League analytics platform that ingests football data from the Football-Data.org API, transforms and stores it in PostgreSQL, and exposes advanced analytics through a Flask REST API.

The platform is fully containerized using Docker and deployed to AWS using Terraform infrastructure-as-code.

---

# Project Overview

This project was built to demonstrate practical skills in:

* Cloud Infrastructure Engineering
* DevOps & Infrastructure as Code
* Data Engineering
* Backend API Development
* Database Design
* AWS Architecture

The application automatically retrieves Premier League data, processes it through an ETL pipeline, loads it into PostgreSQL, and exposes analytical insights through REST endpoints.

---

# Tech Stack

## Cloud & Infrastructure

* AWS EC2
* AWS RDS PostgreSQL
* AWS VPC
* AWS IAM
* AWS Secrets Manager (In Progress)
* Terraform

## Backend

* Python
* Flask
* Psycopg2

## Data Engineering

* Football-Data.org API
* ETL Pipeline
* JSON Data Transformation

## Database

* PostgreSQL

## DevOps

* Docker
* Docker Compose
* GitHub

---

# Architecture

```text
                          Football-Data.org API
                                      │
                                      ▼
                              ETL Container
                                      │
                                      ▼
                          Amazon RDS PostgreSQL
                                      │
                                      ▼
                             Flask API Container
                                      │
                                      ▼
                                 AWS EC2
                                      │
                                      ▼
                                   Client
```

## AWS Infrastructure

```text
Internet
    │
    ▼
Public Subnet
    │
    ▼
EC2 Instance
├── Flask API Container
└── ETL Container
    │
    ▼
Private Subnets
    │
    ▼
Amazon RDS PostgreSQL
```

Infrastructure is provisioned entirely using Terraform.

Resources include:

* Custom VPC
* Public Subnets
* Private Subnets
* Internet Gateway
* Security Groups
* EC2 Instance
* RDS PostgreSQL
* IAM Roles

---

# Key Features

## Cloud Infrastructure

* Infrastructure deployed using Terraform
* Custom AWS VPC with public and private subnets
* EC2-hosted containerized application
* PostgreSQL migrated to Amazon RDS
* Security groups implementing least-privilege access
* IAM roles for secure AWS service access

## Data Engineering

* Automated ETL pipeline
* Historical standings ingestion
* Top scorer ingestion
* JSON transformation and normalization
* Relational PostgreSQL schema

## Analytics

* Team Position Movement
* Points Gained Analysis
* Best Attack Rankings
* Best Defence Rankings
* Top Scorer Efficiency

## API

REST API exposing analytical insights through Flask endpoints.

---

# API Endpoints

| Endpoint              | Description                             |
| --------------------- | --------------------------------------- |
| /                     | API Status                              |
| /best-attack          | Teams ranked by goals per game          |
| /best-defence         | Teams ranked by defensive performance   |
| /points-gained        | Points gained across selected matchdays |
| /topscorer-efficiency | Goal contributions per match            |

---

# Project Structure

```text
Project1/

├── analytics/
│   ├── best_attack.py
│   ├── best_defence.py
│   ├── points_gained.py
│   └── topscorer_efficiency.py
│
├── app/
│   ├── __init__.py
│   └── routes.py
│
├── database/
│   ├── db.py
│   └── insert_data.py
│
├── fetchers/
├── transformers/
│
├── infrastructure/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── scripts/
│           └── bootstrap.sh
│
├── Dockerfile
├── docker-compose.yml
├── aws-compose.yaml
├── requirements.txt
└── README.md
```

---

# Infrastructure Highlights

## Networking

* Custom VPC (10.0.0.0/16)
* Public Subnets for application hosting
* Private Subnets for database isolation

## Security

* EC2 Security Group
* Dedicated RDS Security Group
* PostgreSQL accessible only from EC2
* Encrypted EBS storage
* Encrypted RDS storage

## Automation

Terraform provisions:

* VPC
* Subnets
* Route Tables
* Security Groups
* EC2 Instance
* RDS Database
* IAM Roles

EC2 bootstrap automation installs:

* Docker
* Docker Compose
* Git

using cloud-init user data scripts.

---

# Future Improvements

* AWS Secrets Manager integration
* CloudWatch monitoring and alerting
* S3 data lake storage
* GitHub Actions CI/CD pipeline
* Application Load Balancer
* HTTPS with ACM
* Auto-scaling infrastructure

---

# Learning Outcomes

This project provided hands-on experience with:

* Terraform Infrastructure as Code
* AWS Networking
* Security Groups
* Amazon RDS
* Dockerized Deployments
* Data Engineering Pipelines
* PostgreSQL Administration
* REST API Design
* Cloud Architecture Design

```
```
