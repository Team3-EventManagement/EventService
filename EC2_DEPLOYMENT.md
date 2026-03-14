# Testing on Amazon EC2

This guide assumes you have launched an Amazon EC2 instance (e.g., Ubuntu 22.04 LTS), have SSH access, and want to quickly deploy the API using Docker for testing purposes.

## 1. Prepare your EC2 Instance

First, SSH into your EC2 instance:
```bash
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
```

Update the system and install Docker and Docker Compose:
```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
# Add your user to the docker group so you don't need sudo for every docker command
sudo usermod -aG docker ubuntu
# You will need to log out and log back in for the group change to take effect!
```

## 2. Transfer Files to EC2

You need to copy your project folder (`EventService`) from your local machine to the EC2 instance. You can do this using `scp` from your local machine terminal:

```bash
scp -i /path/to/your-key.pem -r c:\Users\307410\Desktop\EventService ubuntu@your-ec2-public-ip:~/
```
*(Alternatively, you can commit this project to a private GitHub repository and `git clone` it onto your EC2 instance).*

## 3. Update docker-compose.yaml for Production

Currently, your `docker-compose.yaml` only runs the PostgreSQL database. We need to update it to run the FastAPI app as well. 

Create a `.env` file on your EC2 instance with real secrets:
```bash
cd ~/EventService
cp .env.example .env
nano .env  # Edit your secrets! Change POSTGRES_PASSWORD and SECRET_KEY
```

Now, update `docker-compose.yaml` on your EC2 instance (or locally before you copy it) to look like this:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: event_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-event_pass}
      POSTGRES_DB: event_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    restart: always
    ports:
      - "80:8000"
    environment:
      - DATABASE_URL=postgresql://event_user:${POSTGRES_PASSWORD:-event_pass}@db:5432/event_db
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

volumes:
  postgres_data:
```

## 4. Open EC2 Security Group Ports

By default, an EC2 instance only allows inbound traffic on port 22 (SSH). You need to allow inbound HTTP traffic.
1. Go to your AWS EC2 Console.
2. Select your instance -> Go to the **Security** tab.
3. Click on the attached Security Group.
4. Click **Edit inbound rules**.
5. Add a rule: Type **HTTP**, Port **80**, Source **Anywhere-IPv4 (0.0.0.0/0)**.
6. Save rules.

## 5. Run the Application

On your EC2 instance, inside the `EventService` directory:
```bash
docker-compose up -d --build
```

This will:
1. Start the PostgreSQL database
2. Build your FastAPI Docker image using the `Dockerfile`.
3. Start the API container, linking it to the database, and map port 8000 inside the container to port 80 (standard HTTP port) on the EC2 host.

## 6. Test the API

You can now test the API from anywhere in the world! 

Open your web browser and navigate to:
**`http://YOUR_EC2_PUBLIC_IP/docs`**

You should see the FastAPI Swagger UI and be able to create users, login, and create events just like you did locally.
