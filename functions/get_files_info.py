import os
from pathlib import Path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    try:
        abs_path = os.path.abspath(working_directory)
        if not Path(abs_path).is_dir():
            return f'Error: "{directory}" is not a directory'
                
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
      
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            final_str = ""
            for i in Path(target_dir).iterdir():
                final_str += f"- {i.name}: file_size={i.stat().st_size} bytes, is_dir={i.is_dir()}\n"
            return final_str

    except Exception as e:
       return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}