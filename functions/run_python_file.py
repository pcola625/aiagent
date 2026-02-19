import os.path
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required= ["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to python file to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the python file",
                items= types.Schema(
                    type=types.Type.STRING,
                    description="Argument among arguments to pass to the python file",
                )
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try: 
        if (working_directory == None):
            errorString = f'Error: "{working_directory}" is not a directory'
            return errorString

        working_directory_abs = os.path.abspath(working_directory)

        file_path_norm = os.path.normpath(os.path.join(working_directory_abs, file_path))

        print(f"file_path_norm: {file_path_norm}")

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, file_path_norm]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        #os.path.isdir for determining if it is a file, and hence, can't be dumped to.
        if (os.path.isdir(file_path_norm)):
            errorString = f'Error: is a directory and not a regular file: "{file_path}"'
            return errorString

        if not (os.path.exists(file_path_norm)):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        print(f"{file_path[-3:]}")
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_norm]


        """
        if any additional args were provided, add them to the command list. You can use the .extend() method to do this.
        """
        if args != None:
            command.extend(args)


        """
        Use the subprocess.run() function to run the command that you built. This will return a CompletedProcess object, which you'll want to assign to a variable. Also, when calling subprocess.run(), make sure to provide the necessary arguments to:
            Set the working directory properly.
            Capture output (i.e., stdout and stderr).
            Decode the output to strings, rather than bytes; this is done by setting text=True.
            Set a timeout of 30 seconds to prevent infinite execution.

        """
        command_result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=working_directory_abs, timeout=30)

        #Build an output string based on the CompletedProcess object:
        output_string = ""

        #   If the process exited with a non-zero returncode, include "Process exited with code X".
        if command_result.returncode != 0:
            output_string += f"Process existed with code {command_result.stderr}\n"
        if command_result.stdout is None and command_result.stderr is None:
            output_string += f"No output produced\n"
        #   If no output was produced in stdout or stderr (both of which are attributes of CompletedProcess), add "No output produced".
        else:
        #   Otherwise, include any text in stdout prefixed with STDOUT:, and any text in stderr prefixed with STDERR:.
            output_string += f"STDOUT: {command_result.stdout}\n"
            output_string += f"STDERR: {command_result.stderr}\n"

        #Return the output string.
        return output_string
    except Exception as e:
        return f"Error: when doing something at run_python_file: {e}"


