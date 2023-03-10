FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the bot will listen on
EXPOSE 8080

# Set the environment variables for the PostgreSQL database
ENV POSTGRES_DB=telegrambot
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432

# Start the bot
CMD ["python", "bot.py"]