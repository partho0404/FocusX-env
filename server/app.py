from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from env import FocusEnv
from task import get_tasks

app = FastAPI()
env = FocusEnv()

class ActionBody(BaseModel):
    action: str

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def tasks():
    return get_tasks()

@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}

@app.post("/step")
def step(body: ActionBody):
    state, reward, done, info = env.step(body.action)
    return {"state": state, "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    return {"state": env.get_state()}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
