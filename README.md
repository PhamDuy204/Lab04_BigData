# Lab04_BigData

## Host A (Data Sender)

Step 1: Install Docker.  
Download and install Docker from the official website: https://www.docker.com

Step 2: Start Docker Compose.  
Run the following command to build and start the containers in detached mode:  
`docker-compose up --build -d`

Step 3: Install required Python packages.  
Run: `pip install -r requirements.txt`

Step 4: Run the data sending script.  
Execute: `python send_data.py`

---

## Host B (Data Processor)

Step 1: Install required Python packages.  
Run: `pip install -r requirements.txt`

Step 2: Map port host A to B.  
Run: `ssh -L 9092:localhost:9092 -N ip_host_A`

Step 3: Run the main processing script.  
Execute: `python3 main.py`

