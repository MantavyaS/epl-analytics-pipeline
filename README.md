# Prem Analytics Platform

A Dockerized data engineering and analytics platform that ingests Premier League data from the Football-Data API, stores it in PostgreSQL, and exposes advanced team and player analytics through a Flask REST API.

## Tech Stack

### Backend

* Python
* Flask
* PostgreSQL
* Psycopg2

### Data Engineering

* Football-Data.org API
* JSON Transformation Pipeline
* ETL Workflow

### DevOps

* Docker
* Docker Compose

## Architecture Diagram

```text
Football-Data.org API
          │
          ▼
      Fetchers
          │
          ▼
   Transformers
          │
          ▼
     PostgreSQL
          │
          ▼
  Analytics Layer
          │
          ▼
      Flask API
          │
          ▼
       Client
```

## Key Features

- Built an end-to-end ETL pipeline using Python
- Transformed nested JSON API responses into a relational PostgreSQL schema
- Developed analytical queries for team movement, attacking performance, defensive performance, and player efficiency
- Exposed analytics through a Flask REST API
- Containerized the entire platform using Docker and Docker Compose

### Data Pipeline

* Fetches Premier League standings and top scorer data from Football-Data.org
* Retrieves historical standings for multiple matchdays
* Cleans and transforms nested JSON responses
* Loads structured data into PostgreSQL

### Analytics

* Biggest Position Movers
* Points Gained Over Time
* Best Attack Rankings
* Best Defence Rankings
* Top Scorer Efficiency

### API Endpoints

| Endpoint                | Description                            |
| ----------------------- | -------------------------------------- |
| `/`                     | API status                             |
| `/best-attack`          | Teams ranked by goals per game         |
| `/best-defence`         | Teams ranked by defensive performance  |
| `/movement`             | Team position changes across matchdays |
| `/points-gained`        | Points gained over selected matchdays  |
| `/topscorer-efficiency` | Goal contributions per match           |

## Project Structure

```text
Project1/

├── app/
│   ├── __init__.py
│   └── routes.py
│
├── analytics/
│   ├── best_attack.py
│   ├── best_defence.py
│   ├── movement.py
│   ├── points_gained.py
│   └── topscorer_efficiency.py
│
├── database/
│   ├── db.py
│   ├── create_tables.py
│   └── insert_data.py
│
├── fetchers/
├── transformers/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Running the Project

### Clone Repository

```bash
git clone <repository-url>
cd Project1
```

### Configure Environment Variables

Create a `.env` file:

```env
API_KEY=your_api_key

DB_NAME=prem_analytics
DB_USER=admin
DB_PASSWORD=password
DB_HOST=postgres_container
DB_PORT=5432

BASE_URL=https://api.football-data.org/v4
```

### Start Services

```bash
docker compose up --build
```

### Access API

```text
http://localhost:5000
```

Example:

```text
http://localhost:5000/best-attack
```
