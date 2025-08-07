
import json
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os
from langsmith import traceable



load_dotenv()

# client = wrap_openai(OpenAI())
client = OpenAI(
    api_key=" ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(command):
    return os.popen(command).read().strip()  # ✅ returns actual output


def get_weather(city: str):
    # TODO!: Do an actual API Call
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"


avaiable_tools = {
   
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.
    (DONT give code in the terminal)

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    - Use only javascipt language for coding
    -DONT give code in the terminal
    - create FUll stack apps only in React , Nodejs , Express , PostgreSql

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - run_command: Takes a command as input to execute on system and returns ouput
    
    Example:
    User Query: create a simple todo app in js?
    Output: {{ "step": "plan", "content": "The user wants me to create a simple todo app using JavaScript . I need to break this down into smaller steps, including create a folder first in his directory and inside it create files for HTML, CSS, and JavaScript, and linking them together. Since user doesnt provide anything about folder , i will named it as todo_app, and inside it will give the code not on terminal" }}
    Output: {{ "step": "plan", "content": "The user wants me to create a simple todo app using JavaScript. To do that I will create a folder called 'todoapp', create the necessary files (index.html, style.css, script.js), and provide the code for each file using run_command function" }}
    Output: {{ "step": "action", "function": "run_command", "input": "mkdir" }}
    Output: {{ "step": "plan2", "content": "Now that the directory is created, I need to create a file inside it with the todo app code.  I'll create a simple todo app using Javascript and HTML in a file named index.html inside the todo_app directory. I can use 'echo' command to write to the file." }}
    Output: {{ "step": "action", "function": "run_command", "input": "echo" }}
    Output: {{ "step": "observe", "output": "index.js file.txt" }}
    Output: {{ "step": "output", "content": "Successfully created a folder named todo_app and an index.html file containing a simple todo app inside it" }}
"""

messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input('> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name, False) != False:
                output = avaiable_tools[tool_name].get("fn")(tool_input)
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                continue
        
        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break


    


