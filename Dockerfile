# Base image
FROM --platform=linux/amd64  python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install project dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable

# Set the command to run when the container starts
CMD ["python3", "app.py"]
