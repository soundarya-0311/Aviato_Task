# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install -r requirements.txt

# Run FastAPI with Uvicorn
CMD  uvicorn main:app --port 8000 --host=0.0.0.0

ENV GOOGLE_APPLICATION_CREDENTIALS="phrasal-chiller-443513-u1-1eb39beb218a.json"
