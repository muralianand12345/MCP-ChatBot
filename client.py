import time
import asyncio
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP  # , MCPServerStdio


# Configure MCP servers
@st.cache_resource
def setup_agent():
    # Add retry mechanism to handle connection issues during container startup
    retries = 5
    for attempt in range(retries):
        try:
            # Using the Docker service name from docker-compose.yml
            server_1 = MCPServerHTTP(url="http://mcp_server:8001/sse")
            # server_2 = MCPServerHTTP(url="http://mcp_server:8002/sse") # Add more servers if needed
            # server_3 = MCPServerStdio()  # For local npx mcp server

            return Agent(
                "openai:gpt-4o", mcp_servers=[server_1]
            )  # , server_2, server_3])
        except ConnectionError as e:
            if attempt < retries - 1:
                st.warning(
                    f"Connection attempt {attempt+1} failed. Retrying in 3 seconds..."
                )
                time.sleep(3)
            else:
                st.error(
                    f"Failed to connect to MCP server after {retries} attempts: {str(e)}"
                )
                raise
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            raise


# Initialize agent with a try-except to handle startup issues
try:
    agent = setup_agent()
    connection_error = None
except Exception as e:
    agent = None
    connection_error = str(e)

# Simple title
st.title("MCP Chatbot")

# Display area
response_area = st.empty()

# Show error if connection failed
if connection_error:
    st.error(f"Failed to initialize the chatbot: {connection_error}")
    st.info("Please check if the MCP server is running and restart the application.")


# Function to process user query
async def process_query(query):
    if agent is None:
        return "System initialization failed. Please restart the application."

    try:
        async with agent.run_mcp_servers():
            result = await agent.run(query)
        return result.data
    except Exception as e:
        # More detailed error handling
        import traceback

        error_details = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_details)  # Log the full error
        return f"An error occurred: {str(e)}"


# Input box
user_input = st.text_input("Ask something:", key="input")

if user_input:
    with st.spinner("Processing..."):
        try:
            # Run the async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(process_query(user_input))
            finally:
                loop.close()  # Ensure the loop is properly closed

            if isinstance(response, str):
                # Check if it's an image URL
                if any(
                    ext in response.lower() for ext in [".jpg", ".jpeg", ".png", ".gif"]
                ) and response.startswith("http"):
                    response_area.image(response)
                # For HTML content, use markdown to render it properly
                elif "<img" in response or "<ul" in response or "<li" in response:
                    response_area.markdown(response, unsafe_allow_html=True)
                else:
                    response_area.markdown(response)
            else:
                response_area.write(response)

        except Exception as e:
            import traceback

            st.error(f"Error: {str(e)}")
            st.code(traceback.format_exc(), language="python")
