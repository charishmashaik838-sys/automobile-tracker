# Automobile Manufacturing Unit - Two Tier Application

This is a two-tier Python application designed to track materials and production metrics for an automobile manufacturing unit.

## Architecture
- **Tier 1 (Application Tier):** Flask application running on an AWS EC2 instance (handles both frontend and backend).
- **Tier 2 (Data Tier):** Managed database running on AWS RDS (MySQL or PostgreSQL) in a private subnet.

## Key Features
- **Material Tracking:** Log materials built, assembled, and delivered.
- **Metrics Dashboard:** Real-time summary of total and daily production.
- **Inventory Analysis:** Breakdown of materials by type.
- **Status Management:** Quickly update the status of a material as it moves through the production pipeline.

## Deployment Guide

### 1. AWS RDS Setup (Data Tier)
1. **Create RDS Instance:**
   - Select **MySQL** or **PostgreSQL**.
   - Choose the **Free Tier** template.
   - **Network:** Place the instance in a **Private Subnet**.
   - **Security Group:** Allow inbound traffic on the database port (3306 for MySQL, 5432 for PostgreSQL) ONLY from the EC2 Security Group.
2. **Create Database:**
   - Create a database named `automobile_db`.

### 2. AWS EC2 Setup (Application Tier)
1. **Launch EC2 Instance:**
   - Select **Ubuntu 22.04 LTS**.
   - Assign a Security Group allowing:
     - SSH (Port 22) from your IP.
     - HTTP (Port 80 or 5000) from anywhere.
2. **Configure SSH Access:**
   - Connect to your instance: `ssh -i your-key.pem ubuntu@your-ec2-ip`
3. **Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv -y
   git clone <your-repo-url>
   cd automobile_app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 3. Application Configuration
Set the following environment variables on the EC2 instance to connect to the RDS instance:

```bash
export DB_USER='your_rds_username'
export DB_PASSWORD='your_rds_password'
export DB_HOST='your-rds-endpoint.aws.com'
export DB_NAME='automobile_db'
export DB_TYPE='postgresql' # or 'mysql'
export SECRET_KEY='a-very-secure-random-string'
```

### 4. Running the Application
```bash
python app.py
```
The application will be available at `http://<EC2-Public-IP>:5000`.

## Project Structure
- `app.py`: Flask application routes and logic.
- `models.py`: SQLAlchemy database models.
- `templates/index.html`: Single-page dashboard interface.
- `requirements.txt`: Python package dependencies.
