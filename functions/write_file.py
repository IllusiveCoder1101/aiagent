import os
from pathlib import Path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
    
        abs_path = os.path.abspath(working_directory)
            
        #if not Path(abs_path).is_dir():
        #    return f'Error: "{working_directory}" is not a directory'
            
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
                        
        valid_target_dir = os.path.commonpath([abs_path, target_path]) == abs_path
        
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        file_dir = "/".join(target_path.split("/")[0:-1])
        os.makedirs(file_dir,exist_ok=True)
        
        with open(file=target_path, mode='w') as f:
            f.write(content)
            
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"   


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write contents to file, requires user to specify the current working directory, path to the file and content to write to the file.",
        "parameters": {
            "type": "object",
            "properties": {
                
                "file_path": {
                    "type": "string",
                    "description": "Path to the specific file to read content from relative to the working directory no default value for this parameter.",
                },
                "content": {
                    "type":'string',
                    "description": "Content to write to the file."
                }
            },
        },
    },
}