# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Copy the content of the local src directory to the working directory
COPY ./app /norm-fullstack/app
COPY ./docs /norm-fullstack/docs

# Set the working directory inside the container
WORKDIR /norm-fullstack/app

# Install any dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

ARG LLAMA_CLOUD_API_KEY
ENV LLAMA_CLOUD_API_KEY=$LLAMA_CLOUD_API_KEY

# Command to run on container start
CMD ["uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]