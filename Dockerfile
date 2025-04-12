# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Copy the content of the local src directory to the working directory
COPY ./app /norm-fullstack/app
COPY ./docs /norm-fullstack/docs

# Set the working directory inside the container
WORKDIR /norm-fullstack/app

# Install any dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install uvicorn

ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Use the secret during runtime setup (need to debug)
# RUN --mount=type=secret,id=openai_key \
#    echo "OPENAI_API_KEY=$(cat /run/secrets/openai_key)" >> .env

# Command to run on container start
CMD ["uvicorn", "main:app", "--port", "80"]