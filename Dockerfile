FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Just add basic dependencies for Postgres wait script if needed (uncomment if necessary)
# RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5005

CMD ["python", "app.py"]
