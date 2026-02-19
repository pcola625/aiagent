import os
from google import genai
from google.genai import types 

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):

    get_files_info = ""

    try:
        working_directory_abs = os.path.abspath(working_directory)
        if (working_directory == None):
            errorString = f'Error: "{working_directory}" is not a directory'
            return errorString
    

        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        print(f"target dir: {target_dir}")

        #os.path.isdir for determining if it really is
        if not (os.path.isdir(target_dir)):
            errorString = f'Error: "{target_dir}" is not a directory'
            return errorString
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
    
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        for thesefiles in os.listdir(target_dir):
        
            """
            ... for each of the files in it... 

            - README.md: file_size=1032 bytes, is_dir=False
            - src: file_size=128 bytes, is_dir=True
            - package.json: file_size=1234 bytes, is_dir=False

            """
            new_line_to_print=""
            currfile_is_dir = os.path.isdir(os.path.join(target_dir,thesefiles))
            currfile_is_file = os.path.isfile(os.path.join(target_dir,thesefiles))
            currfile_name = thesefiles
            currfile_size = os.path.getsize(os.path.join(target_dir,thesefiles))

            new_line_to_print = f"    - {currfile_name}: file_size={currfile_size} bytes, is_dir={currfile_is_dir}\n"    

            get_files_info += new_line_to_print
        return get_files_info


    except Exception as e:
        return f"Error: error in listing the files: {e}"
