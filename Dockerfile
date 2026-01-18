#parent image
FROM python:3.13.7-alpine3.21

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure stdout and stderr are unbuffered
ENV PYTHONUNBUFFERED 1

# Set the working dir inside the container
WORKDIR /blog_it

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base bash git openssh-client \
    && rm -rf /var/cache/apk/*


# Copy the requirements file and install dependencies
COPY requirements.txt /blog_it/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /blog_it

#Expose the port on which the Django server will run
EXPOSE 8000