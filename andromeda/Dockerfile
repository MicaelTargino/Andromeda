# Dockerfile for Django
FROM python:3.8-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start Django server
CMD ["gunicorn", "andromeda.wsgi:application", "--bind", "0.0.0.0:8000"]