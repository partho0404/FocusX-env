import os
import time
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

def run_task(task_name):
    steps = 3
    total_reward = 0

    print(f"[START] task={task_name} env=focusx mode=productivity_sim", flush=True)

    for step in range(1, steps + 1):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a focus assistant."},
                {"role": "user", "content": "Choose one: study, rest, scroll. Also give a 1-2 word reason. Format: action,reason"}
            ],
            max_tokens=10
        )

        output = response.choices[0].message.content.strip().lower()

        if "," in output:
            action, reason = output.split(",", 1)
        else:
            action = output
            reason = "model_choice"
        
        action = action.strip()
        reason = reason.strip()
        
        # fallback safety
        if action not in ["study", "rest", "scroll"]:
            action = "study"

        # reward logic
        if "study" in action:
            reward = 1.0
        elif "rest" in action:
            reward = 0.6
        else:
            reward = 0.2

        # small safe improvement
        if "study" in action and step == 1:
            reward += 0.1

        total_reward += reward
        # self-evaluation (safe)
        # self-evaluation (safe, no API call)
        if reward >= 1.0:
            self_eval = "good"
        elif reward >= 0.5:
            self_eval = "ok"
        else:
            self_eval = "bad"

        print(
            f"[STEP] step={step} action={action} reason={reason} reward={reward:.2f} self_eval={self_eval}",
            flush=True
        )
        time.sleep(0.3)

    score = total_reward / (steps * 1.5)
    score = max(0.01, min(0.99, score))

    print(f"[END] task={task_name} score={score:.2f} steps={steps}", flush=True)


if __name__ == "__main__":
    run_task("focus_session_1")
    run_task("focus_session_2")
    run_task("focus_session_3")
