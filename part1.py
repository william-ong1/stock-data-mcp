# Part 1 - Setup and Exploration
# 
# Observations:
#
# Llama 3.2 can perform simple math operations, reason through a simple reasoning problem, and provide accurate information regarding capitals and cities.
# It can also paraphrase a sentence, generate text based on a prompt, and generate a Python function for the n-th Fibonacci number.
# However, the model failed at describing an MCP in the context of LLMs. Its response differed each trial, with none of them being "Model Context Protocol".
# Some of its answers were "Mean Conditional Probability", "Mean Collision Per Second", and "Mean Cumulative Perplexity", yet it was very confident in each answer with a thorough explanation.
# In addition, the model failed at describing real-time data, in which it was unable to answer the current date, weather, or stock prices, citing that it does not have real-time access to the data needed.
# The model was also unable to answer my prompt on whether I should buy or sell a stock, citing that it couldn't provide any financial or investment advice.
# As a result, overall, LLama 3.2 is strong at math operations, reasoning, text generation, and historical information retrieval, but struggles with real-time data and financial advice.


import ollama

ollama.pull("llama3.2")

prompts = [
  "What's the square root of 144, then divided by 2?",
  "What's MCP in the context of LLMs?",
  "If I have 4 apples, sold 3, then bought 2, how many do I have?",
  "Paraphrase this: In my free time, I enjoy playing basketball, working out, and trying new restaurants.",
  "Write me a short answer for when someone asks me how's my day.",
  "Write me a Python function to calculate the n-th Fibonacci number.",
  "What's the capital of Japan?",
  "What's the capital of Tokyo?",
  "What's the date today?",
  "What's the weather in Seattle, WA tonight?",
  "What's the current stock price for Microsoft?",
  "I have some AAPL stock worth $1000, how many shares do I roughly have?",
  "Should I buy or sell NVDA right now?"]

for i in range(len(prompts)):
  response = ollama.generate(model="llama3.2", prompt=prompts[i]).response
  print(f"Prompt {i+1}: \"{prompts[i]}\" \nLlama 3.2 says:", response, "\n")
  print("------------------------------------- \n")