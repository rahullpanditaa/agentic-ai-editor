import subprocess
from pathlib import Path

def run_python_file(working_directory, file_path, args=[]):
    working_directory_path = Path(working_directory).resolve()
    target_python_file_path = working_directory_path / file_path
    target_python_file_path = target_python_file_path.resolve()

    if not target_python_file_path.is_relative_to(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not target_python_file_path.exists():
        return f'Error: File "{file_path}" not found.'
    
    if target_python_file_path.suffix != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    
    process = subprocess.run(["python3", file_path, *args], capture_output=True, cwd=working_directory_path, timeout=30.0, text=True)
    out = process.stdout
    err = process.stderr
    code = process.returncode

    output = out if out else "No output produced."
    
    return f"STDOUT:\n{output}\nSTDERR:\n{err}"

