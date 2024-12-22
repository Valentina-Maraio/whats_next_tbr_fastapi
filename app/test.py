import openai

# Set your API key
openai.api_key = "your-api-key"

try:
    # Fetch available models
    response = openai.ChatCompletion.list()
    print("Available models:", response)
except Exception as e:
    print("An error occurred:", e)