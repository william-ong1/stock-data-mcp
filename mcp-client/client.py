# Part 2 - MCP Client

import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from ollama import AsyncClient

class MCPClient:
  def __init__(self, model_name="llama3.2"):
    # Initialize session and client objects
    self.session: Optional[ClientSession] = None
    self.exit_stack = AsyncExitStack()
    self.model_name = model_name
    self.ollama_client = AsyncClient()


  async def connect_to_server(self, server_script_path: str):
    """ Connect to an MCP server
    
    Args:
      server_script_path: Path to the server script (.py or .js)
    """

    is_python = server_script_path.endswith('.py')
    is_js = server_script_path.endswith('.js')
    if not (is_python or is_js):
      raise ValueError("Server script must be a .py or .js file")
        
    command = "python" if is_python else "node"
    server_params = StdioServerParameters(
      command=command,
      args=[server_script_path],
      env=None
    )
      
    stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
    self.stdio, self.write = stdio_transport
    self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
    
    await self.session.initialize()
    
    # List available tools
    response = await self.session.list_tools()
    tools = response.tools
    print("\nConnected to server with tools:", [tool.name for tool in tools])


  async def process_query(self, query: str) -> str:
    """ Process a query using Ollama and available tools """

    # Stock-related query keywords
    stock_keywords = ['stock', 'price', 'market', 'share', 'ticker', 'trading', '$', 
                      'nasdaq', 'nyse', 'dow', 'sp500', 's&p', 'investment']
    
    # Common stock symbols
    common_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'AMD']
    
    # Check if query contains stock symbols or keywords
    query_upper = query.upper()
    has_stock_symbol = any(symbol in query_upper for symbol in common_symbols)
    has_stock_keyword = any(keyword.lower() in query.lower() for keyword in stock_keywords)
    
    if not (has_stock_symbol or has_stock_keyword):
      # For non-stock queries, just use Ollama for conversation
      response = await self.ollama_client.chat(
        model=self.model_name,
        messages=[
          {
            "role": "system",
            "content": "You are a helpful AI assistant. Provide informative and friendly responses."
          },
          {
            "role": "user",
            "content": query
          }
        ],
        stream=False
      )
      return response.message.content

    # Use tools for stock query
    response = await self.session.list_tools()
    available_tools = [{ 
      "name": tool.name,
      "description": tool.description,
      "input_schema": tool.inputSchema
    } for tool in response.tools]

    tools_description = "\n".join([
      f"Tool: {tool['name']}\nDescription: {tool['description']}\nSchema: {tool['input_schema']}"
      for tool in available_tools
    ])
    
    system_prompt = f"""You are a helpful AI assistant with access to stock market tools. Here are the available tools:
      {tools_description}

      To use a tool, respond with a JSON object in this exact format:
      For single stock: {{"name": "get_stock_price", "input": {{"symbol": "AAPL"}}}}
      For multiple stocks: {{"name": "get_multiple_stocks", "input": {{"symbols": "AAPL,MSFT,GOOGL"}}}}

      If the user's query is about stocks, respond with the appropriate JSON object.
      If the query isn't specifically asking for stock data, respond with "GENERAL_QUERY" instead.
      Always use uppercase for stock symbols."""

    try:
      # Make async call to Ollama
      response = await self.ollama_client.chat(
        model=self.model_name,
        messages=[
          {
            "role": "system",
            "content": system_prompt
          },
          {
            "role": "user",
            "content": query
          }
        ],
        stream=False
      )

      response_text = response.message.content
          
      # If the model indicates this is a general query
      if response_text.strip() == "GENERAL_QUERY":
        response = await self.ollama_client.chat(
          model=self.model_name,
          messages=[
            {
              "role": "system",
              "content": "You are a helpful AI assistant. Provide informative and friendly responses."
            },
            {
              "role": "user",
              "content": query
            }
          ],
          stream=False
        )
        return response.message.content
          
      # Try to parse the response as JSON for stock queries
      try:
        import json
        tool_call = json.loads(response_text)
        
        if isinstance(tool_call, dict) and 'name' in tool_call and 'input' in tool_call:
          tool_name = tool_call['name']
          tool_args = tool_call['input']
          
          # Execute tool call
          result = await self.session.call_tool(tool_name, tool_args)
          
          # Get a human-readable response about the stock data
          response = await self.ollama_client.chat(
            model=self.model_name,
            messages=[
              {
                "role": "system",
                "content": "You are a helpful financial advisor. Analyze this stock data and provide insights about the stock prices, market trends, and notable changes. Be concise but informative."
              },
              {
                "role": "user",
                "content": f"Please analyze this stock market data and provide insights:\n{result.content}"
              }
            ],
            stream=False
          )
                  
          return f"Raw Data:\n{result.content}\n\nAnalysis:\n{response.message.content}"
        else:
          return "I couldn't understand how to use the stock tools for your request. Please ask about specific stock symbols (e.g., 'What's the price of AAPL?' or 'Show me AAPL, MSFT, and GOOGL')"
                  
      except json.JSONDecodeError:
        return "I wasn't able to properly format the tool request. Please specify which stocks you want to look up."
              
    except Exception as e:
      return f"An error occurred while processing your request: {str(e)}"


  async def chat_loop(self):
    """ Run an interactive chat loop """

    print("\nMCP Client Started!")
    print(f"Using Ollama model: {self.model_name}")
    print("Type your queries or 'quit' to exit.")

    while True:
      try:
        query = input("\nQuery: ").strip()
          
        if query.lower() == 'quit':
          break
            
        response = await self.process_query(query)
        print("\n" + response)
                
      except Exception as e:
        print(f"\nError: {str(e)}")
  

  async def cleanup(self):
    """ Clean up """
    await self.exit_stack.aclose()


async def main():
  if len(sys.argv) < 2:
    print("Usage: python client.py <path_to_server_script>")
    sys.exit(1)
      
  client = MCPClient(model_name="llama3.2")

  # Connects to server
  try:
    await client.connect_to_server(sys.argv[1])
    await client.chat_loop()
  finally:
    await client.cleanup()


if __name__ == "__main__":
  import sys
  asyncio.run(main())