import os
from pathlib import Path



def get_file_content(working_directory: str, file_path: str) -> str:
    try:

        abs_path = os.path.abspath(working_directory)
        
        if not Path(abs_path).is_dir():
            return f'Error: "{working_directory}" is not a directory'
        
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
                    
        valid_target_dir = os.path.commonpath([abs_path, target_path]) == abs_path
        
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not Path(target_path).is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(file=target_path) as f:
            content = f.read(10000)
        
            if f.read(1):
                content+=  f'[...File "{file_path}" truncated at {10000} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"    

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read file content upto 10000 characters, the file_path should be relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the specific file to read content from relative to the working directory no default value for this parameter.",
                },
            },
        },
    },
}

