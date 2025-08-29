FROM python:3.11-slim

# Set work directory inside container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
