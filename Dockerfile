FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

#Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Start the application
CMD ["flask", "run","--host=0.0.0.0", "--port=5000"]

# Expose the port that the application will run on
EXPOSE 5000
