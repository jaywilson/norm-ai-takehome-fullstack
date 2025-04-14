## Law Server

The server implements a simple API to query laws from GoT.

First build the docker image:

`docker build --build-arg OPENAI_API_KEY=$OPENAI_API_KEY --build-arg LLAMA_CLOUD_API_KEY=$LLAMA_CLOUD_API_KEY -t law_server:latest .`

The run the server:

`docker run -p 9001:80 law_server:latest`

## Query UI

Start the frontend server:

`npm run dev`

Navigate to https://localhost:3000/
