---
title: FocusX Env
emoji: 🚀
colorFrom: indigo
colorTo: green
sdk: docker
pinned: false
license: mit
short_description: FocusX is an AI-powered productivity environment built.
---

# 🚀 FocusX – AI Productivity Optimization Environment

FocusX is an **OpenEnv-compatible AI environment** designed to simulate real-world productivity challenges such as **focus loss, energy depletion, and digital distractions**.

It enables intelligent agents to make decisions under constraints and optimize task completion — similar to how humans manage productivity in daily life.

---

## 🧠 Problem Statement

Modern productivity is not just about working harder — it involves:

- Managing focus 🧠  
- Avoiding distractions 📱  
- Balancing energy ⚡  
- Making optimal decisions under constraints  

FocusX models this as a **sequential decision-making problem**, allowing AI agents to learn and evaluate productivity strategies.

---

## 🌍 Real-World Applications

FocusX can be used for:

- 📚 Student productivity modeling  
- 💻 Developer focus optimization  
- 🤖 AI personal assistant training  
- 🧪 Benchmarking decision-making agents  

This makes it a **human-centric AI environment**, not just a synthetic simulation.

---

## ⚙️ Environment Design

At each step, the agent observes:

python
{
  "focus": int,          # Attention level (0–100)
  "energy": int,         # Energy level (0–100)
  "tasks_left": int,     # Remaining tasks
  "distraction": bool    # Presence of distraction
}

---

##🎮 Action Space
The agent chooses one action:
study → Progress on tasks
rest → Recover energy
scroll → Lose focus (distraction behavior)

---

## 🔄 Environment Dynamics

- Focus and energy are bounded within **[0,100]**
- Distractions appear dynamically during execution
- Episode ends when:
  - All tasks are completed ✅
  - Step limit is reached ⛔

---

## 🎯 Task Structure

FocusX includes **3 evaluation tasks**:

| Task   | Description                  |
|--------|------------------------------|
| Easy   | Basic task completion        |
| Medium | Handle distractions          |
| Hard   | Optimize under constraints   |

Each task increases difficulty in:
- Distraction frequency
- Resource management complexity
- Decision pressure

---

## 🧪 Agent (Inference Logic)

The agent is powered by an **LLM via LiteLLM proxy**:

bash

python
Energy: X, Focus: Y, Distraction: Z → choose action

Uses external model (Qwen2.5-72B-Instruct)
Falls back to random policy if API fails
Ensures robustness and reproducibility

---

##🔗 API Integration

FocusX uses the provided OpenEnv API:

Python
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)
✔ Required for evaluation
✔ Ensures compatibility with OpenEnv grading

---

##📊 Evaluation & Scoring
Each task produces a score:

0 < score < 1
Score is based on:
Total reward accumulated
Task completion efficiency
Decision quality
Python
score = (total_reward + 10) / 20
score = clamp(0.01, 0.99)

---

##🧾 Output Format (OpenEnv Compatible)
FocusX follows strict structured logging:

[START] task=...
[STEP] step=... action=... reward=...
[END] success=... score=...

This ensures:
✅ Machine-readable evaluation
✅ Deterministic validation
✅ Compatibility with OpenEnv pipeline

---

##🏗️ Project Architecture

env.py        → Environment logic
task.py       → Task configurations
grader.py     → Evaluation rules
inference.py  → Agent + API interaction

Flow:

Agent → Environment → Action → Reward → Score

---

🎥 Sample Execution

[START] task=focus_task_1 env=focusx
[STEP] step=1 action=study reward=1.00
[STEP] step=2 action=rest reward=0.50
...
[END] success=true score=0.72

---

##💡 Why FocusX Stands Out
Unlike traditional RL environments, FocusX models:
🧠 Cognitive states (focus, energy)
📱 Real-world distractions
⚖️ Trade-offs between short-term vs long-term rewards
This makes it a step toward human-aware AI systems.

---

##⚡ Key Features
Dynamic distraction system
Multi-task evaluation (Easy → Hard)
Reward-driven environment
LLM-powered agent decision making
OpenEnv-compatible design

---

##🚧 Limitations
Rule-based reward shaping
No learning agent (yet)
Simplified human behavior modeling

---

##🔮 Future Improvements
Reinforcement Learning (Q-learning / PPO)
Adaptive difficulty scaling
Smarter distraction modeling
Multi-agent collaboration
Analytics dashboard for performance tracking

---

##🏁 Summary
FocusX is a compact yet powerful AI environment that bridges:
👉 Reinforcement Learning
👉 Human productivity modeling
👉 Decision-making under constraints
It serves as a strong foundation for building intelligent productivity agents.
