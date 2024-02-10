import openai

def query_openai_chat_model(prompt):
    openai.api_key = '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'

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the appropriate engine for your task
        prompt=prompt,
        max_tokens=150  # Adjust as needed
    )

    return response.choices[0].text.strip()

# ... rest of your code
