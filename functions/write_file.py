from pathlib import Path

def write_file(working_directory, file_path, content):
    working_directory_path = Path(working_directory).resolve()
    target_file_path = working_directory_path / file_path
    target_file_path = target_file_path.resolve()

    if not target_file_path.is_relative_to(working_directory_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not target_file_path.exists():
        target_file_path.touch()

    with open(target_file_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'