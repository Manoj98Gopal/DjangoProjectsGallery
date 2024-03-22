# Use an official Python 3.8 image as the base image
FROM python:3.8

# Set environment variables to configure Python's behavior
ENV PYTHONUNBUFFERED 1         # Ensure Python prints output to the terminal immediately
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing bytecode files

# Install dependencies for PostgreSQL client
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory for your application inside the container
WORKDIR /app

# Copy the project's dependencies file (requirements.txt) into the container
COPY requirements.txt /app/

# Install gunicorn and other project dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . /app/

# Specify the command to run when the container starts
CMD ["gunicorn", "storefront.wsgi:application", "--bind", "0.0.0.0:8000"]
