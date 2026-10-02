import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from call_function import call_function
import json
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

prompt = args.user_prompt
verbose = args.verbose
available_functions = [
    schema_get_files_info,
    schema_run_python_file,
    schema_get_file_content,
    schema_write_file
]
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt},
]
response = {}

for _ in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    
    message = response.choices[0].message

    if message.tool_calls is None:
        break
    messages.append(message)
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call,verbose)
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)

if response.usage is not None:
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
else:
    raise RuntimeError("API Failure!")


print("Final response:")
print(response.choices[0].message.content)