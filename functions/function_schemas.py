from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
            )
        }
    )
)

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the contents of the specified file path, contained within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file whose contents are to be read and returned. A maximum of 10,000 characters to be read."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the specified .py file. If optional arguments given, use them as command-line arguments. The .py file ahs to be within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The .py file which is to be executed."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The optional command-line arguments to be used when executing the .py file. Default value is an empty list"
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the given file path the given content as argument. The file has to be within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write the contents to. If given file path does not already exist, a new file will be created with the exact same file path."
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="The contents which are to be written to the specified file path."
            )
        }
    )
)