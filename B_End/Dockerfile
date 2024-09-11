FROM python:3.10.12

WORKDIR /app

# Copy only the requirements file to my working dir
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the backend port
EXPOSE 8080

# Run the backend application
CMD ["python3", "app.py"]
