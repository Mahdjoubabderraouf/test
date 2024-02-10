#!/usr/bin/env python3
import os
import sys
import openai
import string
import re
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# set OPENAI_API_KEY= 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
FILENAME_VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
GIT_DIFF_FILENAME_REGEX_PATTERN = r"\+\+\+ b/(.*)"
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo-0125"
DEFAULT_STYLE = "concise"
DEFAULT_PERSONA = "kent_beck"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 4096

OPENAI_ERROR_NO_RESPONSE = "No response from OpenAI. Error:\n"
OPENAI_ERROR_FAILED = "OpenAI failed to generate a review. Error:\n"

API_KEYS = {
    "openai": "OPENAI_API_KEY",
}

REQUEST = "Code Review Checklist\
Code Readability\
- Code readability is satisfactory.\
- Consider improving variable and function names for better clarity.\
\
Proper Indentation and Formatting\
- Inconsistent indentation observed.\
- Ensure uniformity in indentation for better readability.\
\
Efficient Use of Variables\
- Unused variables present.\
- Evaluate variable scoping for optimization.\
\
Clear and Concise Comments\
- Some parts lack comments.\
- Ensure comments accurately reflect the code and provide clarity.\
\
Adherence to Coding Standards\
- Coding standards not consistently followed.\
- Address violations and align with project standards.\
\
Proper Error Handling\
- Error handling could be more robust.\
- Consider adding explicit error messages for better debugging.\
\
Function and Variable Naming Conventions\
- Naming conventions not consistently followed.\
- Align with project naming standards for consistency.\
\
---\
\
Overall Assessment:\
The code meets the following criteria: List of criteria met.\
The code needs improvement in the following areas: List of criteria not met.\
\
Feel free to address the mentioned points and provide updates or explanations where necessary. \
at the end i need a full rapport contains more review info about the code  \
\n"

STYLES = {
"zen": "the review must be in markdown file format"
}

PERSONAS = {
    "developer": "You are an experienced software developer in a variety of programming languages and methodologies. You create efficient, scalable" ,
    "kent_beck": "You are Kent Beck. You are known for software design patterns, test-driven development (TDD), and agile methodologies",
}

class BaseLLM:
    """
    Base class for language learning models.
    """
    def __init__(self, model: str):
        self.model = model

    def prepare_kwargs(self, prompt: str, max_tokens: int, temperature: float) -> dict:
        """
        Prepares the keyword arguments for an LLM API call.
        To be implemented by subclasses.
        """
        raise NotImplementedError

    def call_api(self, kwargs: dict) -> str:
        """
        Calls the LLM API using the provided kwargs.
        To be implemented by subclasses.
        """
        raise NotImplementedError

class OpenAI_LLM(BaseLLM):
    """
    OpenAI LLM implementation.
    """
    def prepare_kwargs(self, prompt: str, max_tokens: int, temperature: float) -> dict:
        kwargs = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": prompt}],
        }
        return kwargs

    def call_api(self, kwargs: dict) -> str:
        try:
            response = openai.ChatCompletion.create(**kwargs)
            
            if response.choices:
                if "text" in response.choices[0]:
                    return response.choices[0].text.strip()
                else:
                    return response.choices[0].message.content.strip()
            else:
                return OPENAI_ERROR_NO_RESPONSE + response.text
        except Exception as e:
            print(f"OpenAI API call failed with parameters {kwargs}. Error: {e}")
            raise Exception(f"OpenAI API call failed with parameters {kwargs}. Error: {e}")

def main():
    # Get environment variables
    api_to_use = os.environ.get("API_TO_USE", "openai")  # Default to OpenAI if not specified
    persona = PERSONAS.get(os.environ.get("PERSONA", DEFAULT_PERSONA))
    style = STYLES.get(os.environ.get("STYLE", DEFAULT_STYLE))
    api_key_env_var = API_KEYS.get(api_to_use)

    # Make sure the necessary environment variable is set
    if api_key_env_var is None or api_key_env_var not in os.environ:
        print(f"The {api_key_env_var} environment variable is not set.")
        sys.exit(1)

    # Read in the diff
    diff = sys.stdin.read()
    """

    # Generate the prompt
    prompt = f"{persona}.{style}.{REQUEST}\n{diff}"

    # Instantiate the OpenAI LLM class (Assuming it's defined elsewhere)
    llm = OpenAI_LLM(DEFAULT_OPEN


    
    """

    # Generate the prompt
    prompt = f"{persona}.{style}.{REQUEST}\n{diff}"

    # Instantiate the OpenAI LLM class
    llm = OpenAI_LLM(DEFAULT_OPENAI_MODEL)
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the API key for OpenAI

    # Prepare kwargs for the API call
    kwargs = llm.prepare_kwargs(prompt, LLM_MAX_TOKENS, LLM_TEMPERATURE)
    
    # Call the API and print the review text
    review_text = llm.call_api(kwargs)

    print(f"{review_text}")

if __name__ == "__main__":
    main()
