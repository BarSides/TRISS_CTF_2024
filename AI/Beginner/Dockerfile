# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY . .

RUN mkdir static

# Set the environment variable for the CTF flag
ENV CTF_FLAG "BarSides{t0rch3d_by_p1ckl3s}"

# Expose the port the app will run on
EXPOSE 8893

# Run the Flask application
CMD ["python", "app.py"]