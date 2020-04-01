FROM python:3.8.2-alpine3.11

# Create app directory
RUN mkdir -p /usr/app/watchlist

# Set Work directory
WORKDIR /usr/app/watchlist

# Copy all project files
COPY . ./

# Install requirements
RUN pip install -r requirements.txt

# Cleanup 
RUN rm Dockerfile

# Run the application
CMD ["/bin/sh", "-c", "python watchlist.py"]