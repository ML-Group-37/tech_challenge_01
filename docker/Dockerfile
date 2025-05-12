# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./src/ .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "tech_challenge.main:app", "--host", "0.0.0.0", "--port", "8000"]
