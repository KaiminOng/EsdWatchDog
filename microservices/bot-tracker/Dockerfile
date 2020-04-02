FROM python:3.8.2-alpine3.11

# Create app directory
RUN mkdir -p /usr/app/bot-tracker

# Set Work directory
WORKDIR /usr/app/bot-tracker

# Copy all project files
COPY . ./

# Install requirements
RUN pip install -r requirements.txt

# Cleanup 
RUN rm Dockerfile

# Run the application
CMD ["/bin/sh", "-c", "python webhook.py"]