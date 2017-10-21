# Use an official Python runtime as a base image
FROM python:3.6-wheezy

# Set the working directory to /app
WORKDIR /Platypus

# Copy the current directory contents into the container at /app
ADD . /Platypus

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "src/Tornado.py"]