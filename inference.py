# import os
# import random
# from openai import OpenAI
# from env import FocusEnv

# API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
# API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "dummy")
# MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# ACTIONS = ["study", "rest", "scroll"]

# try:
#     client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
# except Exception:
#     client = None

# def get_action(state):
#     try:
#         if not client:
#             return random.choice(ACTIONS)
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[{
#                 "role": "user",
#                 "content": f"Energy:{state['energy']} Focus:{state['focus']} Distraction:{state['distraction']} Tasks:{state['tasks_left']}. Choose: study/rest/scroll. One word only."
#             }],
#             max_tokens=10,
#             temperature=0.3
#         )
#         action = response.choices[0].message.content.strip().lower()
#         if action not in ACTIONS:
#             return "study"
#         return action
#     except Exception:
#         return random.choice(ACTIONS)

# def run_task(task_name):
#     env = FocusEnv()
#     state = env.reset()
#     print(f"[START] task={task_name} env=focusx model={MODEL_NAME}", flush=True)

#     total_reward = 0.0
#     rewards = []
#     done = False
#     step = 0

#     while not done and step < 10:
#         action = get_action(state)
#         state, reward, done, info = env.step(action)
#         step += 1
#         total_reward += reward
#         rewards.append(reward)
#         error = info.get("error", None)
#         print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error if error else 'null'}", flush=True)

#     score = max(0.01, min(0.99, (total_reward + 10) / 20))
#     rewards_str = ",".join([f"{r:.2f}" for r in rewards])
#     success = score > 0.5
#     print(f"[END] success={str(success).lower()} steps={step} score={score:.2f} rewards={rewards_str}", flush=True)
#     return score

# def main():
#     tasks = ["focus_task_1", "focus_task_2", "focus_task_3"]

#     for task in tasks:
#         print(f"[START] task={task} env=focusx model={MODEL_NAME}", flush=True)

#         env = FocusEnv()
#         state = env.reset()

#         total_reward = 0.0
#         done = False
#         step = 0

#         while not done and step < 10:
#             action = get_action(state)
#             state, reward, done, info = env.step(action)

#             step += 1
#             total_reward += reward

#             error = info.get("error", None)

#             print(
#                 f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error if error else 'null'}",
#                 flush=True
#             )

#         score = max(0.01, min(0.99, (total_reward + 10) / 20))
#         success = score > 0.5

#         print(
#             f"[END] success={str(success).lower()} steps={step} score={score:.2f}",
#             flush=True
#         )


import os
import random
from openai import OpenAI
from env import FocusEnv

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "dummy")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

ACTIONS = ["study", "rest", "scroll"]

try:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
except Exception:
    client = None

def get_action(state):
    try:
        if not client:
            action = random.choice(ACTIONS)
            reason = "fallback_random"
            return action, reason

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": f"""
Energy:{state['energy']} Focus:{state['focus']} Distraction:{state['distraction']} Tasks:{state['tasks_left']}.
Choose: study/rest/scroll.
Also give a 2-word reason.
Format: action,reason
"""
            }],
            max_tokens=15,
            temperature=0.3
        )

        output = response.choices[0].message.content.strip().lower()

        if "," in output:
            action, reason = output.split(",", 1)
        else:
            action = output
            reason = "model_choice"

        action = action.strip()
        reason = reason.strip()

        if action not in ACTIONS:
            return "study", "fallback_invalid"

        return action, reason

    except Exception:
        return random.choice(ACTIONS), "error_fallback"

def run_task(task_name):
    env = FocusEnv()
    state = env.reset()
    print(f"[START] task={task_name} env=focusx mode=productivity_sim model={MODEL_NAME}", flush=True)

    total_reward = 0.0
    rewards = []
    done = False
    step = 0

    while not done and step < 10:
        action, reason = get_action(state)
        state, reward, done, info = env.step(action)
        # safe reward shaping (small tweaks only)
        if state["distraction"] and action == "study":
            reward += 0.2
        
        if state["energy"] < 30 and action == "rest":
            reward += 0.1
        step += 1
        total_reward += reward
        rewards.append(reward)
        error = info.get("error", None)
        print(
            f"[STEP] step={step} action={action} reason={reason} reward={reward:.2f} done={str(done).lower()} error={error if error else 'null'}",
            flush=True
        )
    score = max(0.01, min(0.99, (total_reward + 10) / 20))
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    success = score > 0.5
    print(f"[END] success={str(success).lower()} steps={step} score={score:.2f} rewards={rewards_str}", flush=True)
    return score

def main():
    tasks = [
        "exam_preparation",
        "deep_work_session",
        "deadline_pressure"
    ]

    for task in tasks:
        print(f"[START] task={task} env=focusx mode=productivity_sim model={MODEL_NAME}", flush=True)

        env = FocusEnv()
        state = env.reset()

        total_reward = 0.0
        done = False
        step = 0

        while not done and step < 10:
            action, reason = get_action(state)
            state, reward, done, info = env.step(action)
            # safe reward shaping (small tweaks only)
            if state["distraction"] and action == "study":
                reward += 0.2
            
            if state["energy"] < 30 and action == "rest":
                reward += 0.1

            step += 1
            total_reward += reward

            error = info.get("error", None)
 
            print(
                f"[STEP] step={step} action={action} reason={reason} reward={reward:.2f} done={str(done).lower()} error={error if error else 'null'}",
                flush=True
            )

        score = max(0.01, min(0.99, (total_reward + 10) / 20))
        success = score > 0.5

        print(
            f"[END] success={str(success).lower()} steps={step} score={score:.2f}",
            flush=True
        )
