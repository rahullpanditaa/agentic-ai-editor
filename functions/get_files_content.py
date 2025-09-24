from pathlib import Path

def get_file_content(working_directory, file_path):
    working_directory_path = Path(working_directory).resolve()
    target_file_path = working_directory_path / file_path
    target_file_path = target_file_path.resolve()

    if not target_file_path.is_relative_to(working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not target_file_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with target_file_path.open() as f:
        file_contents = f.read(10000)

    if len(file_contents) > 10000:
        file_contents += f"\n[...File {file_path} truncated at 10000 characters]"
    return file_contents