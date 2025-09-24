import os
from pathlib import Path

def get_files_info(boundary_directory, directory="."):
    # directory is relative path within the working directory

    boundary_path = Path(boundary_directory)
    boundary_path = boundary_path.resolve()
    target_path = boundary_path / directory

    # check whether target path inside working path
    if not target_path.resolve().is_relative_to(boundary_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not target_path.is_dir():
        return f'Error: "{directory}" is not a directory'
    
    directory_contents = ""
    for p in target_path.iterdir():
        directory_contents += f"- {p.name}: file_size={p.stat().st_size} bytes, is_dir={p.is_dir()}\n"
    
    return directory_contents.rstrip()

    

    
    

    
    