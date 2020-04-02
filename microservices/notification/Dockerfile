FROM python:3.8.2-alpine3.11

# Create app directory
RUN mkdir -p /usr/app/notification

# Set Work directory
WORKDIR /usr/app/notification

# Copy all project files
COPY . ./

# Change permission for run script
RUN chmod 755 start.sh

# Install requirements
RUN pip install -r requirements.txt

# Cleanup folder
RUN rm Dockerfile

# Run the application
CMD ["/bin/sh", "-c", "python /usr/app/notification/notification.py"]

