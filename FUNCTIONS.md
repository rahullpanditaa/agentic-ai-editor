# FUNCTIONS.md

This document describes all tools (functions) used by the Agentic AI Editor. These tools are exposed to the LLM through **Google Gemini function-calling**, enabling the model to read, write, inspect, and execute code inside a sandboxed working directory.

Each tool has:

* A Python implementation (in `functions/`)
* A schema describing expected arguments and return values
* Safety checks to prevent directory escape

---

# 📂 Working Directory

All tools operate strictly inside:

```
./calculator/
```

Paths outside this directory are rejected.

---

# 🧰 1. get_files_info

### **Purpose**

List all files and directories inside a given relative path of the working directory.

### **Schema Name**

```
get_files_info
```

### **Python File**

`functions/get_files_info.py`

### **Parameters**

| Name      | Type   | Required | Description                                           |
| --------- | ------ | -------- | ----------------------------------------------------- |
| directory | string | No       | Path relative to the working directory (default: ".") |

### **Behavior**

* Ensures path stays inside sandbox
* Lists each file with:

  * name
  * size in bytes
  * whether it’s a directory

### **Example Output**

```
- tests.py: file_size=1342 bytes, is_dir=False
- pkg: file_size=4096 bytes, is_dir=True
- main.py: file_size=729 bytes, is_dir=False
```

---

# 📄 2. get_file_content

### **Purpose**

Read up to the first 10,000 characters of a file.

### **Schema Name**

```
get_file_content
```

### **Python File**

`functions/get_files_content.py`

### **Parameters**

| Name      | Type   | Required | Description                                |
| --------- | ------ | -------- | ------------------------------------------ |
| file_path | string | Yes      | Path to file relative to working directory |

### **Behavior**

* Ensures file is inside sandbox
* Ensures file exists
* Reads up to 10k characters
* Appends truncate message if too long

### **Example Output**

```
import json
from pkg.calculator import Calculator
# ...
```

### **Potential Errors**

* "File not found"
* "File outside permitted directory"

---

# 📝 3. write_file

### **Purpose**

Create or overwrite a file with new content.

### **Schema Name**

```
write_file
```

### **Python File**

`functions/write_file.py`

### **Parameters**

| Name      | Type   | Required | Description                |
| --------- | ------ | -------- | -------------------------- |
| file_path | string | Yes      | Path to file               |
| content   | string | Yes      | Full file content to write |

### **Behavior**

* Ensures path is inside sandbox
* Creates the file if it does not exist
* Overwrites entire file content
* Returns success message with character count

### **Example Output**

```
Successfully wrote to "main.py" (823 characters written)
```

### **Potential Errors**

* "Cannot write outside permitted directory"

---

# 🐍 4. run_python_file

### **Purpose**

Execute a Python script inside the working directory and return its output.

### **Schema Name**

```
run_python_file
```

### **Python File**

`functions/run_python_file.py`

### **Parameters**

| Name      | Type   | Required | Description                |
| --------- | ------ | -------- | -------------------------- |
| file_path | string | Yes      | Python file to execute     |
| args      | array  | No       | Optional list of arguments |

### **Behavior**

* Ensures script is inside sandbox
* Ensures file exists and is a `.py` file
* Executes with:

```
subprocess.run(["python3", file_path, *args], ...)
```

* Captures stdout, stderr, and exit code
* Returns combined output

### **Example Output**

```
STDOUT:
{
  "expression": "5 + 7",
  "result": 12
}

Process exited with code 0
```

### **Potential Errors**

* "File not found"
* "Not a Python file"
* Python runtime exceptions
* Timeout exceptions

---

# 🧠 5. Function Dispatcher (`call_function.py`)

This component:

1. Accepts a list of `FunctionCall` objects produced by Gemini
2. Looks up their corresponding Python functions
3. Injects the `working_directory` argument automatically
4. Executes each function safely
5. Wraps the results into `types.Content` objects
6. Returns these to the agent loop

All tool responses follow the Gemini function-call JSON schema format.

---

# 📘 Summary

The five tools allow the model to:

* Inspect the project
* Read code
* Modify files
* Execute Python modules

Together they support multi-step, agentic behavior inside a safe, controlled environment.

This API layer (set of callable tools available to LLM) defines the core functionality that the model uses to operate as a coding assistant.
