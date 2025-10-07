# Use the official Python 3.9 slim version as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code from the host to the container's /app directory
COPY . .

# Command to run the application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]