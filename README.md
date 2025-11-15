# Agentic AI Editor (Toy Claude Code)

<p align="center">
  <img src="screenshots/demo.gif" width="650">
</p>


A lightweight, CLI-based code-editing agent inspired by tools like Cursor, OpenCode, and Claude Code. This project demonstrates how to build an **agentic coding assistant** using Google's free Gemini API.

The agent can:

* Inspect files in a sandboxed working directory (LLM can only access files inside that directory)
* Read file contents
* Write or modify files
* Execute Python files and return stdout/stderr
* Use iterative reasoning to solve coding tasks

It works by combining a **function-calling LLM** with a colection of tools (functions that are available for the LLM to call).

---

## 🚀 Features

* **Directory Inspection** — List files and folders along with size and type
* **Safe File Reading** — Read up to 10,000 characters of any file inside the working directory
* **Safe File Writing** — Modify or create files (sandboxed within the working directory)
* **Python File Execution** — Run Python scripts with arguments
* **Agent Loop** — LLM iteratively calls tools until task is complete
* **Working Directory Sandbox** — Prevents escaping the project directory
* **Verbose Mode** — View detailed tool-calls for debugging

---

## 📂 How It Works

At a high level, the agent follows this loop:

1. User provides a prompt
2. LLM examines the prompt and decides whether to:

   * produce text **or**
   * call one of the available tools
3. If the model requests a tool call, Python executes it
4. The tool’s result is appended to the conversation
5. The LLM reasons again using the result
6. Loop continues until the model provides a final answer

This mirrors how real agentic editors (Cursor, Claude Code) operate.

---

## 📁 Project Structure

```
agentic-ai-editor/
├── main.py
├── call_function.py
├── functions/
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   |── write_file.py
|   |__function_schemas.py (schemas for each tool)
│    
├── calculator/            # Sandboxed working directory (Example code for this project)
│   ├── main.py
│   ├── tests.py
│   ├── README.md
│   └── lorem.txt
└── utils/
    └── setup + constants
```

---

## 🛠️ Installation

Make sure you have:

* Python 3.10+
* `uv` package manager
* A `.env` file containing:

```
GEMINI_API_KEY=your_api_key_here
```

Install dependencies:

```
uv install
```

---

## ▶️ Usage

Run the agent with a natural language command:

```
uv run main.py "list all files"
```

```
uv run main.py "read tests.py"
```

```
uv run main.py "fix my calculator app"
```

You can also enable verbose logging:

```
uv run main.py "read main.py" --verbose
```

---

## 🖼️ Screenshots

### Reading a file
![Reading a file](screenshots/read_file.png)

### List all files
![List all files](screenshots/get_files_info.png)

### Explore functionality
![Explore functionality](screenshots/explore.png)

### Fix a bug
![Fix a bug](screenshots/fix_bug.png)

## 🧠 Example Outputs

### Listing files:

```
- Calling function: get_files_info
- main.py (729 bytes)
- tests.py (1342 bytes)
- README.md (12 bytes)
```

### Reading a file:

```
- Calling function: get_file_content
Okay, I have read the content of `tests.py`...
```

### Running the calculator directly:

```
uv run calculator/main.py "5 + 7"
{
  "expression": "5 + 7",
  "result": 12
}
```

---

## 🔒 Safety

All tools are restricted to the `./calculator` working directory. Attempts to read or write outside this directory return safe error messages.

---

## 🧱 Limitations

* Only supports Python file execution
* File reads are capped at 10,000 characters
* LLM occasionally reflects or plans instead of immediately calling a tool
* No rollback or diff-based file editing

---

## 🎯 Learning Goals

This project demonstrates:

* How function-calling LLMs work
* Agent loop design
* Safe tool invocation
* Multi-file Python project structuring
* Building real developer tools powered by LLMs

---

## Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [USAGE.md](USAGE.md)
- [FUNCTIONS.md](FUNCTIONS.md)
