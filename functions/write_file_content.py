import os
from google import genai
from google.genai import types

schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Writes provided data into file which is part of the working directory structure.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to which data is written, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The data to write into the file_path file.",
            ),
        },
    ),
)

def write_file_content(working_directory, file_path, content):

    try:

        if (working_directory == None):
            errorString = f'Error: "{working_directory}" is not a directory'
            return errorString

        working_directory_abs = os.path.abspath(working_directory)

        file_path_norm = os.path.normpath(os.path.join(working_directory_abs, file_path))

        print(f"file_path_norm: {file_path_norm}")

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, file_path_norm]) == working_directory_abs
        print(f"valid_target_dir: {valid_target_dir}")
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        #os.path.isdir for determining if it is a file, and hence, can't be dumped to.
        if (os.path.isdir(file_path_norm)):
            errorString = f'Error: is a directory and not a regular file: "{file_path}"' 
            return errorString

        #check for and create any directories/subdirs required.

        if not (os.path.isdir(os.path.dirname(file_path_norm))):
            os.makedirs(os.path.dirname(file_path_norm), exist_ok=True)

        #now that they are there...
        with open(file_path_norm, "w") as f:
            f.write(content)

    except Exception as e: 
        return f"Error: error in write file: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
