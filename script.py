import time
from openai import OpenAI
import os
import sys

# Read content of the diff file provided as argument
diff_file = sys.argv[1]
with open(diff_file, "r") as file:
    content = file.read()

client = OpenAI(api_key="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")
ASSISTANT_ID = "asst_Fy3sB2IFeExmT3vsH9zRQ6sK"

# Get the content from the changes in the event
if os.getenv('GITHUB_EVENT_NAME') == 'push':
    # Get the commit messages from the push event
    for commit in os.getenv('COMMIT_MESSAGES').split('\n'):
        content += commit + '\n'
elif os.getenv('GITHUB_EVENT_NAME') == 'pull_request':
    # Get the pull request body
    content = os.getenv('PULL_REQUEST_BODY')

# Create a thread with the retrieved content.
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": content,
        }
    ]
)

# Submit the thread to the assistant (as a new run).
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

# Wait for run to complete.
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    time.sleep(1)

# Get the latest message from the thread.
message_response = client.beta.threads.messages.list(thread_id=thread.id)
messages = message_response.data

# Print the latest message.
latest_message = messages[0]
print(f"💬 code review: {latest_message.content[0].text.value}")
