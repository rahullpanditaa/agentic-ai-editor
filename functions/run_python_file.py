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
    
    try:
        process = subprocess.run(["python3", file_path, *args], capture_output=True, cwd=working_directory_path, timeout=30.0, text=True)
        out = process.stdout
        err = process.stderr
        code = process.returncode
    except Exception as e:
        return f"Error: executing Python file: {e}"


    output = f"STDOUT:\n{out}\n" if out else ""
    error = f"STDERR:\n{err}\n" if err else ""
    exit_code = f"Process exited with code {code}" if code != 0 else ""

    
    return f"{output}{error}{exit_code}"

