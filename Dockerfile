# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdk-pixbuf2.0-dev \
    libgtk-3-dev \
    libasound2 \
    libdbus-glib-1-2 \
    libxt6 \
    libxtst6 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy the rest of the application's code into the container
COPY . .

# Command to run the application
CMD ["python", "amorfo.py"]
