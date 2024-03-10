# LLM -- OpenAI GPT Applications
Sample Python Project To Show LLM Capability

### Keycloak Authentication 
 - src/auth_service

### Interactive Chat Application -- src/chat_service
 - Company Name with simple prompt engineering
 - Document Summarizer
 - Video to Audio
 - You Tube Video Summarizer

### Non-Interactive Applications -- src/llm_service
 - Interactive chat interface using LLMs


### How to Run:
 - Navigate to src/ folder and open terminal
 - Create a .env file and fill in the config values mentioned in .env.sample
 - Feel free to remove the mysql service from docker-compose file if you already have a mysql instance running. In that case, create the username and database appropriately. If you are using the mysql service, then you do not have worry about changing anything.
 - Run docker-compose down; docker-compose up -d
 - You should be able to open these 4 links in any browser:
   - https://localhost:8443/auth/
   - https://localhost/auth_service/docs
   - https://localhost/chat_service/docs
   - https://localhost/llm_service/docs

### Requirements:
 - Docker

### Frameworks used
 - Docker 
 - Envoy 
 - Python (fastapi, mysql.connector, openai, etc)
 - SQL (MySQL)
 - Keycloak

### Concepts / Technologies
 - LLM
 - REST APIs
 - RDBMS
 - Proxy (Rate Limiting)
 - Authentication (OIDC)
 - Micro Services
