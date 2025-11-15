# USAGE.md

This guide explains how to run and interact with the **Agentic AI Editor**, a lightweight agentic coding assistant powered by Google's Gemini API.

The agent operates entirely through a command-line interface and uses tools to read, modify, and execute code inside a sandboxed working directory (`./calculator`).

---

# 🚀 1. Prerequisites

Before running the agent, make sure you have:

* **Python 3.10+** installed
* **uv** package manager (for running and installing Python packages)
* A **Gemini API key** stored in a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

Install project dependencies:

```
uv sync
```

---

# ▶️ 2. Running the Agent

The core interface is:

```
uv run main.py "<your prompt here>"
```

Examples:

```
uv run main.py "list all files"
uv run main.py "read tests.py"
uv run main.py "what does this project do?"
```

To enable verbose mode (shows tool calls):

```
uv run main.py "read tests.py" --verbose
```

---

# 📂 3. Working Directory

The agent only operates inside the sandboxed directory:

```
./calculator/
```

Tools cannot read or write outside this directory. Any attempt to escape it (e.g., `../secret.txt`) will return a safe error.

---

# 🧠 4. What the Agent Can Do

The agent supports the following capabilities:

### **✔️ List files in the working directory**

```
uv run main.py "list files"
```

### **✔️ Read any file**

```
uv run main.py "read tests.py"
```

### **✔️ Modify or create files**

```
uv run main.py "add comments to main.py"
```

### **✔️ Run Python files**

```
uv run main.py "run tests.py"
```

### **✔️ Debug code with iterative tool calls**

```
uv run main.py "fix my calculator app"
```

The agent determines which tool to use by reasoning about your prompt.

---

# 💻 5. Example Sessions

Below are real screenshots captured while using the agent.

### 📸 Listing Files

![List Files](screenshots/get_files_info.png)

### 📸 Exploring the Project

![Explore](screenshots/explore.png)

### 📸 Reading a File

![Read File](screenshots/read_file.png)

### 📸 Fixing Bugs

![Fix Bug](screenshots/fix_bug.png)

---

# 🛠️ 6. Supported Prompts

You can ask the agent to:

* "Summarize tests.py"
* "Improve the calculator logic"
* "Run the calculator on '5 * 12'"
* "Fix division"
* "Add a new feature: exponentiation"
* "Refactor this project"
* "Explain how this code works"

The model will:

1. Analyze your request
2. Choose the right tools
3. Perform actions
4. Return results or iterate further

---

# 🔒 7. Error Cases

The sandbox prevents unsafe actions. Examples:

### ❌ Attempting to read outside sandbox

```
uv run main.py "read ../etc/passwd"
```

→ Returns: *Error: Cannot read file outside permitted directory*

### ❌ Running non-Python files

```
uv run main.py "run lorem.txt"
```

→ Returns: *Error: not a Python file*

### ❌ Writing outside sandbox

```
uv run main.py "write ../hack.py: print(1)"
```

→ Returns: *Error: Cannot write outside working directory*

---

# 🧭 8. Understanding the Flow

A typical multi-step request:

```
uv run main.py "fix my calculator app"
```

**Step-by-step:**

1. Model lists files
2. Model reads relevant files
3. Model analyzes code
4. Model writes new code
5. Agent executes tests
6. Model decides if more fixes are needed
7. Final summary returned

---

# 📘 9. Notes

* All file paths must be relative to `./calculator`
* The agent loop runs up to 20 iterations
* File reads are capped at 10k characters
* Python execution uses `subprocess.run`

---

This document gives you everything you need to use the agent effectively.

If you'd like to dive deeper, see:

* **README.md** for a general overview
* **ARCHITECTURE.md** for an internal explanation of the system
* **FUNCTIONS.md** (optional) for detailed tool documentation
