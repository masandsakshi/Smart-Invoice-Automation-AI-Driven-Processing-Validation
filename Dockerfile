# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# (Optional) upgrade pip first so it can pick up possible wheels 
# for other packages more reliably
RUN pip install --no-cache-dir --upgrade pip

# Copy the requirements file into the container
COPY ./requirements.txt ./

# Install any dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set the working directory
WORKDIR /code

# Copy the rest of the working directory contents into the container
COPY ./src  ./src

# Install bash
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y bash
