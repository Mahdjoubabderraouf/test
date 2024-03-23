import time
from openai import OpenAI
import os
import sys

# Read content of the diff file provided as argument
diff_file = sys.argv[1]
with open(diff_file, "r") as file:
    content = file.read()

client = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))
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
            "content": """
            # importing the cv2 library
import cv2

# loading the haar case algorithm file into alg variable
alg = "/content/haarcascade_frontalface_default.xml"
# passing the algorithm to OpenCV
haar_cascade = cv2.CascadeClassifier(alg)
# loading the image path into file_name variable - replace <INSERT YOUR IMAGE NAME HERE> with the path to your image
file_name = "/content/363563581_389519590091103_5883128900995827442_n.jpg"
# reading the image
img = cv2.imread(file_name, 0)
# creating a black and white version of the image
gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# detecting the faces
faces = haar_cascade.detectMultiScale(
    gray_img, scaleFactor=1.05, minNeighbors=3, minSize=(100, 100)
)

i = 0
# for each face detected
for x, y, w, h in faces:
    # crop the image to select only the face
    cropped_image = img[y : y + h, x : x + w]
    # loading the target image path into target_file_name variable  - replace <INSERT YOUR TARGET IMAGE NAME HERE> with the path to your target image
    target_file_name = 'stored-faces/' + str(i) + '.jpg'
    cv2.imwrite(
        target_file_name,
        cropped_image,
    )
    i = i + 1;""",
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
