# 🤖 MIKE AI: Local God-Mode Agentic Assistant

> **An autonomous, multimodal AI agent running 100% locally on your machine.**  
> Powered by **Qwen 2.5 14B**, designed for **Blender automation**, **system control**, and **complex task execution** without cloud dependencies.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![LLM](https://img.shields.io/badge/Model-Qwen2.5--14B-green.svg)
![Status](https://img.shields.io/badge/status-God%20Mode%20Enabled-red.svg)

---

## 🚀 What is MIKE AI?

MIKE AI is not just a chatbot. It is an **autonomous agent** inspired by *AutoGPT*, *Hermes*, and *OpenInterpreter*. It possesses "God Mode" permissions to execute shell commands, manipulate files, control external applications (like Blender), and manage its own memory.

Unlike standard LLM interfaces that only *talk* about tasks, MIKE **executes** them.

### 🔥 Key Features

*   **🧠 Local Brain**: Runs on **Qwen 2.5 14B** via Ollama. No data leaves your computer.
*   **⚡ God Mode Execution**: Direct access to file systems, shell commands, and application APIs. No "Are you sure?" prompts.
*   **🔄 Autonomous Loops**: Uses a **ReAct (Reason + Act)** loop to plan, execute, observe errors, and self-correct until the task is done.
*   **🗣️ Voice Interface**: Built-in Text-to-Speech (pyttsx3) for hands-free operation.
*   **🛠️ Multi-Agent Tools**: Specialized sub-agents for Trading, File Ops, Web Search, and 3D Modeling (Blender).
*   **💾 Persistent Memory**: Remembers project context and past actions across sessions.

---

## 🏗️ Architecture

MIKE AI combines the best of modern agentic frameworks:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Core Engine** | Python + Ollama | Hosts the local Qwen 2.5 14B model. |
| **Orchestrator** | ReAct Loop | Plans steps → Executes Tool → Observes Result → Retries if failed. |
| **Toolbox** | Native Python | `os`, `subprocess`, `bpy` (Blender), `requests`. |
| **Memory** | JSON/Vector | Stores conversation history and project state. |
| **Voice** | pyttsx3 | Offline, low-latency speech synthesis. |

---

## 📦 Installation

### Prerequisites
1.  **Python 3.10+** installed.
2.  **Ollama** installed and running ([Download Ollama](https://ollama.com)).
3.  **Git** (optional, for cloning).

### Step 1: Pull the Model
Ensure you have the required local model:
```bash
ollama pull qwen2.5:14b
