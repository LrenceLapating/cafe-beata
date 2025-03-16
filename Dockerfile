FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p uploads/avatars

# Expose the port the app runs on
EXPOSE $PORT

# Command to run the application
CMD cd backend && uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000} 