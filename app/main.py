from fastapi import FastAPI
from pydantic import BaseModel

from env.core.environment import GridEnv
from env.tasks.easy import get_task

app = FastAPI()

env = None


class ActionInput(BaseModel):
    action: int


@app.post("/reset")
def reset():
    global env
    task = get_task()
    env = GridEnv(task)
    state = env.reset()
    return {"state": state}


@app.post("/step")
def step(input: ActionInput):
    state, reward, done, info = env.step(input.action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.get("/tasks")
def tasks():
    return ["easy", "medium", "hard"]


@app.get("/baseline")
def baseline():
    return {"message": "Baseline runs via script"}