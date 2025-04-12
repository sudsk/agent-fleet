FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=5000
ENV AGENTFLEET_ENVIRONMENT=${AGENTFLEET_ENVIRONMENT:-DEVELOPMENT}

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
