# ARCHITECTURE.md

This document describes the internal architecture of the **Agentic AI Editor**, a toy implementation of agentic coding assistants like Cursor, Claude Code, and OpenCode. It explains how the agent loop works, how tools are invoked, how files are safely manipulated, and how the system remains sandboxed.

---

# 🧩 1. High-Level Overview

The system combines:

* A **function-calling LLM** (Google Gemini)
* A set of **safe Python tools** (file read/write, directory listing, Python execution)
* An **agent loop** that feeds tool responses back to the model
* A **sandboxed working directory** (`./calculator`)

The LLM uses tools to inspect, understand, and modify files on disk until it produces a final answer.

At a high level, the architecture looks like this:

```
User Prompt → Agent Loop → LLM → Tool Call → Python Tool
                  ↑                           ↓
                  └────────── Tool Response ───┘
```

---

# 🔄 2. The Agent Loop

The core engine is a loop that runs up to 20 iterations:

1. Send current `messages` (conversation history) to the LLM
2. Receive:

   * Natural language text **or**
   * A list of one or more **FunctionCall** objects
3. If **FunctionCall** (i.e. if LLM wants to call one of the available tools):

   * Execute the function(s) in Python
   * Convert outputs into `function_response` objects
   * Append them to the conversation
4. If **text** (i.e. if the LLM sends back plain text in the response, not a list[FunctionCall]):

   * Print and exit
5. Repeat

This is the same control flow used by agentic editors.

---

# 🧠 3. Message Structure

Every LLM call includes:

## **User messages:**

Contain prompts or tool results.

## **Model messages:**

Contain model-generated text or function call requests.

Each message is a `types.Content` object containing one or more `parts`.

### Example sequence:

```
User: "Fix my calculator"
Model: FunctionCall(get_files_info)
Tool: directory listing
Model: FunctionCall(get_file_content)
Tool: file contents
Model: natural language answer (final)
```

---

# 🧰 4. Tools and Schemas

The system exposes four tools to the LLM:

### 1. **get_files_info**

Lists files in a directory.

### 2. **get_file_content**

Reads a file (safe, truncated to 10,000 characters).

### 3. **write_file**

Writes content to a file (creates if missing).

### 4. **run_python_file**

Executes a Python script inside the sandboxed working directory.

Each tool has a **FunctionDeclaration schema**, which tells Gemini:

* The tool’s name
* Its description
* The names, types, and required fields of its parameters

This ensures the LLM generates valid function calls.

---

# 🔒 5. Sandboxing and Safety

The agent enforces a strict working directory:

```
./calculator/
```

Every tool validates paths like this:

1. Resolve the working directory path
2. Resolve the target path
3. Use `is_relative_to()` to ensure the path is inside the sandbox

If a path escapes the directory (e.g., `"../secret.txt"`), the tool returns an error instead of executing.

This prevents:

* Modifying system files
* Reading sensitive data
* Breaking out of project boundaries

---

# ⚙️ 6. Function Dispatcher

`call_function.py` is responsible for:

1. Accepting a **list of FunctionCall objects**
2. Mapping LLM function names to Python functions
3. Passing arguments into the Python functions
4. Wrapping their results into `function_response` parts
5. Returning a list of `Content` objects to the agent loop

This layer ensures that:

* Tools are consistently invoked
* Errors return structured responses
* The LLM always receives well-formed results

---

# 🧪 7. Execution Flow Example

User prompt:

```
"Fix my calculator app"
```

The agent might execute:

1. `get_files_info` → list project files
2. `get_file_content(main.py)` → read implementation
3. `get_file_content(tests.py)` → read tests
4. LLM analyzes differences
5. LLM suggests code fix
6. `write_file(main.py, new_code)` → patched file
7. `run_python_file(tests.py)` → verify fix
8. LLM determines if more fixes are needed
9. Final natural language response

Each iteration is guided entirely by model reasoning.

---

# 🗂️ 8. Repository Layout

```
agentic-ai-editor/
├── README.md          ← main overview for humans
├── ARCHITECTURE.md    ← deep technical explanation
├── screenshots/       ← images referenced in README
├── main.py            ← agent loop
├── call_function.py   ← function dispatcher
├── functions/         ← all tool implementations + schemas
├── calculator/        ← sandboxed working directory (agent operates here)
└── utils.py           ← helper functions

```

---

# 🎯 9. Key Design Goals

* **Safety:** no filesystem escape
* **Clarity:** readable, modular structure
* **Reproducibility:** deterministic tool responses
* **Learning value:** demonstrates real agentic tooling
* **Expandability:** new tools can be added easily

---

# 🧱 10. Limitations

* Only supports Python execution
* No diff-based file editing (full overwrite only)
* No long-term memory or plan-chaining
* Multi-file reasoning is LLM-dependent
* Does not detect infinite loops (bounded by iteration count)

---

# 📌 11. Future Extensions

* Recursively listing files
* File searching / grep tool
* JSON-aware editing tools
* Python AST-based fix suggestions
* Git integration
* Planning to use a different, much larger project as the sandbox

---

# 📘 Summary

This project demonstrates a **complete working example of an agentic coding editor**, using:

* a sandboxed filesystem
* a predictable tool interface
* a clean agent loop
* structured function-calling

It captures the core principles behind real-world tools like Cursor and Claude Code in a lightweight, fully transparent implementation.

---
