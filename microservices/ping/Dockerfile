FROM python:3.8

# Create app directory
RUN mkdir -p /usr/app/ping

# Set Work directory
WORKDIR /usr/app/ping

# Copy all project files
COPY . ./

# Install requirements
RUN pip install -r requirements.txt

# Cleanup folder
RUN rm Dockerfile

# Run the application
CMD ["/bin/sh", "-c", "python ping.py"]

