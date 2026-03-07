#Base Image
FROM python:3.13-slim

# working dir in the container
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

EXPOSE 5001

CMD ["python", "app.py"]

