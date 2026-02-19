import os
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads data from a specific file path, up to a maximum of 10000 characters, and returns that as a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path from which data is read, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):

    get_file_content = ""

    try:
    # wonder if this can be refactored  later...
        if (working_directory == None):
            errorString = f'Error: "{working_directory}" is not a directory'
            return errorString


        working_directory_abs = os.path.abspath(working_directory)

        file_path_norm = os.path.normpath(os.path.join(working_directory_abs, file_path))

        #os.path.isdir for determining if it really is
        if not (os.path.isfile(file_path_norm)):
            errorString = f'Error: File not found or is not a regular file: "{file_path}"' 
            return errorString
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, file_path_norm]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'



        MAX_CHARS = 10000

        with open(file_path_norm, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            get_file_content += file_content_string

        # After reading the first MAX_CHARS...
            if f.read(1):
                get_file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return get_file_content

    except Exception as e:
        return f"Error: error reading file: {e}"
