# Use an official Python runtime as a base image
FROM python:slim

# Set the working directory to /aor
WORKDIR /aor

# Copy the current directory contents into the container at /aor
ADD . /aor

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["python", "aor.py"]