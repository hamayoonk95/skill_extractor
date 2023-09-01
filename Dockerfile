# Use Python 3.8 slim image as the base image
FROM python:3.11-slim

# Set the working directory in the Docker image
WORKDIR /app

# Install Chrome Browser (Selenium needs it for scraping)
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Copy the requirments file
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Run the application
CMD ["python", "main.py"]


# Command to run docker container from the image with HOST_IP for mysql_host and a database name for database in -it interactive mode

# docker run --rm -e MYSQL_HOST=100.65.220.94 -e DATABASE_NAME=dummy_dock -it --name skill_extractor_container skill_extractor