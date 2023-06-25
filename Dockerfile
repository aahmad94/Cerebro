# Base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run when the container starts
CMD ["python3", "cerebro_bot.py"]
