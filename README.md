# MCP-ChatBot

A versatile chatbot application that uses MCP (Modular Capability Protocol) to interact with multiple service backends.

![MCP Chatbot](https://img.shields.io/badge/MCP-Chatbot-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10-blue)
![Docker](https://img.shields.io/badge/docker-compatible-blue)

## Overview

MCP-ChatBot is a containerized application that demonstrates the use of Modular Capability Protocol (MCP) to enable LLM interactions with external services. This implementation includes a weather service backend and a Streamlit-based frontend that allows users to query for weather information through natural language.

## Features

- **Containerized Architecture**: Separate containers for the MCP server and client application
- **Weather Service Integration**: Real-time weather data using WeatherAPI
- **Streamlit UI**: Clean, responsive user interface for interacting with the chatbot
- **Extensible Design**: Ready to add more MCP servers for additional capabilities
- **GPT-4o Integration**: Powered by OpenAI's GPT-4o model for natural language understanding

## Architecture

The application consists of two main components:

1. **MCP Server**: A FastMCP-based service that handles weather data retrieval
2. **Streamlit Client**: A web-based UI for interacting with the chatbot

## Getting Started

### Prerequisites

- Docker and Docker Compose
- WeatherAPI Key (sign up at [WeatherAPI](https://www.weatherapi.com/))
- OpenAI API Key (sign up at [OpenAI](https://platform.openai.com/))

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/MCP-ChatBot.git
cd MCP-ChatBot
```

2. Create an `.env` file based on the example:

```bash
cp .env.example .env
```

3. Edit the `.env` file and add your API keys:

```
PYTHONUNBUFFERED=1
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

4. Launch the application using Docker Compose:

```bash
docker-compose up --build
```

5. Access the Streamlit UI at: `http://localhost:8501`

## Usage

Once the application is running, you can interact with the chatbot through the Streamlit interface:

1. Type natural language queries about weather in the text input
2. Examples:
   - "What's the weather like in New York?"
   - "How hot is it in Tokyo right now?"
   - "Tell me about the weather in London"

## Extending the Application

### Adding New MCP Servers

1. Create a new server file in the `servers` directory
2. Add the new service to the `docker-compose.yml` file
3. Update the client.py to include the new server in the agent configuration

Example of adding a new server in client.py:

```python
server_1 = MCPServerHTTP(url="http://mcp_server:8001/sse")
server_2 = MCPServerHTTP(url="http://new_server:8002/sse")  # New server

return Agent("openai:gpt-4o", mcp_servers=[server_1, server_2])
```

## Development

### Project Structure

```
MCP-ChatBot/
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── client.py                # Streamlit client application
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile.client        # Dockerfile for Streamlit client
├── Dockerfile.server        # Dockerfile for MCP server
├── LICENSE                  # MIT license
├── README.md                # Project documentation
└── servers/                 # MCP server implementations
    └── server.py            # Weather service implementation
```

### Technology Stack

- **FastMCP**: Framework for creating MCP servers
- **Streamlit**: Web framework for the UI
- **Pydantic-AI**: Agent system for LLM interactions
- **Docker**: Containerization platform
- **OpenAI GPT-4o**: LLM for natural language processing

## Troubleshooting

### Common Issues

1. **Connection Failed**: Ensure that all services are up and running. The client has a retry mechanism, but if it fails, restart the application.

2. **API Key Errors**: Verify that you've added valid API keys to the `.env` file.

3. **Docker Network Issues**: If containers can't communicate, check the Docker network configuration and ensure the service names match in the code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastMCP](https://github.com/Significant-Gravitas/fastmcp) for the MCP server implementation
- [Streamlit](https://streamlit.io/) for the frontend framework
- [WeatherAPI](https://www.weatherapi.com/) for weather data

---

Created by [Murali Anand](https://github.com/yourusername) © 2025