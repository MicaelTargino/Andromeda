FROM python:3.8-slim

WORKDIR /app

ENV PYTHONUBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Execute Python script
CMD ["python", "index_data.py"]