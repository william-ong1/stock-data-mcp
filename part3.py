# Part 3 - Evaluation and Analysis

import ollama

ollama.pull("llama3.2")

prompts = [
  "What's the square root of 144?",
  "What's a MCP in the context of LLMs?",
  "If I have 4 apples, sold 3, then bought 2, how many do I have?",
  "If I have 4 apples, sold 3, then bought 2, how many do I have in stock?",
  "If an item is initially $100, then there is a 30 percent discount, what is the new price?"
  "Paraphrase this: In my free time, I enjoy playing basketball, working out, and trying new restaurants.",
  "Write me a short answer for when someone asks me how's my day.",
  "What's the date today?",
  "What's the weather in Seattle, WA tonight?",
  "What's the current stock price for Microsoft?",
  "I have some AAPL stock worth $1000, how many shares do I roughly have?",
  "Should I buy or sell NVDA right now?"]

for i in range(len(prompts)):
  response = ollama.generate(model="llama3.2", prompt=prompts[i]).response
  print(f"Prompt {i+1}: \"{prompts[i]}\"")
  print("Response without tool integration:")
  print(response, "\n")
  print("Response with tool integration:\n")
  print("------------------------------------- \n")


# Prompt 1: "What's the square root of 144?"
# Response without tool integration:
# The square root of 144 is 12. 

# √144 = 12 

# Response with tool integration:

# ------------------------------------- 



# Prompt 2: "What's a MCP in the context of LLMs?"
# Response without tool integration:
# In the context of Large Language Models (LLMs), "MCP" likely stands for "Masked CLS Prediction". 

# In the Masked Language Modeling (MLM) task, a subset of words in the input sequence are randomly replaced with a [MASK] token. The model is then trained to predict the original word that was replaced by the [MASK] token.

# CLS (Classifier Label) is a specific type of label used in some LLMs to indicate the classification or category of the input sequence. In this context, MCP likely refers to predicting the CLS label for a given input sequence.

# In practice, MCP often involves a binary classification task where the model needs to predict whether the input sequence falls into one of two categories (e.g., positive/negative sentiment, spam/ham, etc.). The predicted CLS label is then used as the output of the model. 

# Response with tool integration:

# ------------------------------------- 

# Prompt 3: "If I have 4 apples, sold 3, then bought 2, how many do I have?"
# Response without tool integration:
# To find out how many apples you have now, let's break it down step by step:

# 1. You started with 4 apples.
# 2. You sold 3 apples, so you were left with: 4 - 3 = 1 apple
# 3. Then, you bought 2 more apples, so now you have: 1 + 2 = 3 apples

# So, you currently have 3 apples. 

# Response with tool integration:

# ------------------------------------- 

# Prompt 4: "If I have 4 apples, sold 3, then bought 2, how many do I have in stock?"
# Response without tool integration:
# Let's break it down:

# You start with 4 apples.
# You sell 3, leaving you with: 4 - 3 = 1
# Then, you buy 2 more, so now you have: 1 + 2 = 3

# So, you have 3 apples in stock. 

# Response with tool integration:

# ------------------------------------- 

# Prompt 5: "If an item is initially $100, then there is a 30 percent discount, what is the new price?Paraphrase this: In my free time, I enjoy playing basketball, working out, and trying new restaurants."
# Response without tool integration:
# I see you've provided a completely unrelated passage about your personal interests.

# To answer your original question, if an item is initially $100 and there's a 30 percent discount, we need to calculate the discount amount first:

# Discount = 30% of $100
# = 0.3 x $100
# = $30

# Now, subtract the discount from the initial price:

# New Price = Initial Price - Discount
# = $100 - $30
# = $70 

# Response with tool integration:

# ------------------------------------- 

# Prompt 6: "Write me a short answer for when someone asks me how's my day."
# Response without tool integration:
# Here are a few options:

# * "It's going well, thanks! Just enjoying the moment."
# * "Good, just busy with [insert task or activity here]."
# * "Can't complain, got everything done I needed to today."
# * "It's been a good day so far, thanks for asking!"
# * "Just taking it one thing at a time, that's about it."

# Choose the one that best fits your mood and tone! 

# Response with tool integration:

# ------------------------------------- 

# Prompt 7: "What's the date today?"
# Response without tool integration:
# I'm not currently able to share the date in real-time. I can provide you with general information and answer questions about dates, but I don't have have access to your device's clock or current date. If you need to know the current date, I recommend checking your device's clock or searching online for the current date. 

# Response with tool integration:

# ------------------------------------- 

# Prompt 8: "What's the weather in Seattle, WA tonight?"
# Response without tool integration:
# I'm not capable of providing real-time weather information. However, I can suggest some ways for you to find out the current weather in Seattle, WA:

# 1. Check online weather websites: You can check websites like weather.com, accuweather.com, or wunderground.com for the latest weather forecast and conditions.
# 2. Use a mobile app: Download a weather app on your smartphone, such as Dark Sky or Weather Underground, to get real-time weather updates.
# 3. Tune into local news: Watch local news or check their website for the latest weather forecast and updates.

# If you'd like, I can also provide general information about Seattle's typical weather patterns during different times of the year. Just let me know! 

# Response with tool integration:

# ------------------------------------- 

# Prompt 9: "What's the current stock price for Microsoft?"
# Response without tool integration:
# I'm not able to provide real-time data or current prices. However, I can suggest some ways for you to find the current stock price of Microsoft:

# 1. Check online financial websites: You can check websites such as Yahoo Finance, Google Finance, or Microsoft's own investor relations website for the current stock price.
# 2. Use a stock market app: Download a stock market app on your mobile device, such as Robinhood, Fidelity, or Apple Finance, which provides real-time stock prices.
# 3. Visit a financial news website: Websites like Bloomberg, CNBC, or The New York Times often provide up-to-date stock prices.

# Please note that stock prices can fluctuate rapidly and may be different when you check. 

# Response with tool integration:

# ------------------------------------- 

# Prompt 10: "I have some AAPL stock worth $1000, how many shares do I roughly have?"
# Response without tool integration:
# To find out how many shares of AAPL you have, we need to know the current market price of one share. However, since my knowledge cutoff is December 2023, I can provide you with a rough estimate based on historical data.

# As of my knowledge cutoff in December 2023, the average market price of one Apple Inc. (AAPL) share was around $145.

# To calculate the number of shares you have, you can divide your total investment value ($1000) by the current market price per share ($145):

# $1000 ÷ $145 = approximately 6.89 shares

# Please note that this is an estimate based on historical data and may not reflect the current market price or the actual number of shares you own. For accurate information, I recommend checking the current stock price and consulting your broker or financial institution. 

# Response with tool integration:

# ------------------------------------- 

# Prompt 11: "Should I buy or sell NVDA right now?"
# Response without tool integration:
# I can't provide personalized financial or investment advice, but I can offer general information about NVIDIA Corporation. Would that help? 

# Response with tool integration:

# ------------------------------------- 