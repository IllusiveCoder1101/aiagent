import os
from pathlib import Path
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
    
        abs_path = os.path.abspath(working_directory)
            
        if not Path(abs_path).is_dir():
            return f'Error: "{working_directory}" is not a directory'
            
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
                        
        valid_target_dir = os.path.commonpath([abs_path, target_path]) == abs_path
            
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        if not Path(target_path).is_file():
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ['python', target_path] + (args or [])
  

        process_run = subprocess.run(command,text=True, timeout=30, capture_output=True)

        print(process_run)
        if process_run.returncode != 0:
            return f"Process exited with code {process_run.returncode}"

        if not process_run.stdout and not process_run.stderr:
            return "No output produced"
        out = ""

        if process_run.stdout:
            out += f"STDOUT: {process_run.stdout}"
        if process_run.stderr:
            out += f"STDERR: {process_run.stderr}"
        return out

    except Exception as e:
        return f"Error: executing python file: {e}"   


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute python code depending on the specified working directory, path to the python file (relatve to working directory) and args which is a list of string to run the required python file.",
        "parameters": {
            "type": "object",
            "properties": {
                
                "file_path": {
                    "type": "string",
                    "description": "Path to the specific python file to execute  from relative to the working directory no default value for this parameter.",
                },
                "args": {
                    "type":'List[string]',
                    "description": "Arguments required to run the python file."
                }
            },
        },
    },
}