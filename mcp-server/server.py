# Part 2 - MCP Server 
# FastMCP server that uses yfinance to fetch stock information from Yahoo! Finance's API.
# yfinance documentation: https://yfinance-python.org and https://github.com/ranaroussi/yfinance 

from typing import Any, Dict
import yfinance as yf
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("server")

def get_stock_info(ticker: str) -> Dict[str, Any] | None:
  """ Get stock information with proper error handling. """
  try:
    stock = yf.Ticker(ticker)
    return stock.info
  except Exception:
    return None


def format_stock_info(info: Dict[str, Any]) -> str:
  """ Format stock information into a readable string. """
  return f"""
    Symbol: {info.get('symbol', 'Unknown')}
    Current Price: ${info.get('regularMarketPrice', 'Unknown')}
    Previous Close: ${info.get('regularMarketPreviousClose', 'Unknown')}
    Open: ${info.get('regularMarketOpen', 'Unknown')}
    Day's Range: ${info.get('regularMarketDayLow', 'Unknown')} - ${info.get('regularMarketDayHigh', 'Unknown')}
    52 Week Range: ${info.get('fiftyTwoWeekLow', 'Unknown')} - ${info.get('fiftyTwoWeekHigh', 'Unknown')}
    Market Cap: ${info.get('marketCap', 'Unknown'):,.2f}
    Volume: {info.get('volume', 'Unknown'):,}
    """


@mcp.tool()
async def get_stock_price(symbol: str) -> str:
  """ Get current stock price and basic information.

  Args:
      symbol: Stock ticker symbol (e.g., AAPL, MSFT)
  """

  info = get_stock_info(symbol)
  
  if not info:
    return f"Unable to fetch data for {symbol}"
  
  return format_stock_info(info)


@mcp.tool()
async def get_multiple_stocks(symbols: str) -> str:
  """ Get current prices for multiple stocks.

  Args:
      symbols: Comma-separated list of stock symbols (e.g., AAPL,MSFT,GOOGL)
  """

  symbols_list = [s.strip() for s in symbols.split(',')]
  results = []
  
  for symbol in symbols_list:
    info = get_stock_info(symbol)
    if info:
      price = info.get('regularMarketPrice', 'Unknown')
      change = info.get('regularMarketChange', 0)
      change_percent = info.get('regularMarketChangePercent', 0)
      results.append(f"{symbol}: ${price} ({change:+.2f} / {change_percent:+.2f}%)")
    else:
      results.append(f"{symbol}: Unable to fetch data")
  
  return "\n".join(results)


if __name__ == "__main__":
  mcp.run(transport='stdio')