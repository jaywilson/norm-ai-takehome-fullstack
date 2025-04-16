## Law Server

The server implements a simple API to query laws from GoT.

First build the docker image:

`docker build --build-arg OPENAI_API_KEY=$OPENAI_API_KEY --build-arg LLAMA_CLOUD_API_KEY=$LLAMA_CLOUD_API_KEY -t law_server:latest .`

Then run the server:

`docker run -p 9001:80 law_server:latest`

## Query UI

Start the frontend server:

`npm run dev`

Navigate to https://localhost:3000/

## Reflection Response

Q: What unique challenges do you foresee in developing and integrating AI regulatory agents for legal
compliance from a full-stack perspective? How would you address these challenges to make the system
robust and user-friendly?

Accuracy: each compliance decision needs to be correct and auditable. I would make sure to have robust
observability for the agent processes: be able to audit the context the agent had and re-evaluate its decisions.

Completeness: can the system answer all the customer's compliance questions? I would invest in making sure
parsing and structuring of new regulations is as robust as possible, and especially identify situations
where it seems likely human understanding will be needed for the foreseeable future and figure out how to
develop tools to assist the people working on it.

Automation: would the user trust the system to make a compliance decision without human intervention? I would
try to build a system that clearly articulates its decisions to the user and presents them with actions it is
ready to take, so that the user only needs to approve them. Over time, hopefully the system's accuracy will be
high enough that the user will feel comfortable auto-accepting high-condidence suggestions. 
