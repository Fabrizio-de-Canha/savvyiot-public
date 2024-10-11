# Stage 1: Build the application
FROM python:3.10 as BUILD_IMAGE

# Set working directory
WORKDIR /home/savvyiot/frontend-api

# Create a virtual environment
RUN python -m venv venv

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/home/savvyiot/frontend-api/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM python:3.10-slim as final

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/savvyiot/frontend-api

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/home/savvyiot/frontend-api/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the virtual environment and application code from the build stage
COPY --from=BUILD_IMAGE /home/savvyiot/frontend-api/venv /home/savvyiot/frontend-api/venv
COPY ./api /home/savvyiot/frontend-api/

# Start the application
CMD ["uvicorn", "main:app", "--port", "5000", "--host", "0.0.0.0"]
