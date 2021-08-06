import random

import uvicorn
from fastapi import FastAPI, Path, Query, responses

# from pydantic import BaseModel

app = FastAPI()

jokes = ["Jokes are going through", "hehe this is a joke", "more jokes"]


@app.get("/")
def index():
    body = "<h1>The Heptagram API</h1>"
    return responses.HTMLResponse(content=body)


@app.get("/jokes/{joke_id}")
def jokes_by_id(
    joke_id: int = Path(..., title="ID of the Joke to get", ge=0, le=len(jokes))
):

    return responses.JSONResponse(content={"joke": jokes[joke_id], "id": joke_id})


@app.get("/jokes")
def _jokes(num: int = Query(1, ge=1, le=len(jokes))):
    random_joke_ids = sorted(random.sample(range(0, len(jokes)), num))
    return responses.JSONResponse(
        content=[{"id": joke_id, "joke": jokes[joke_id]} for joke_id in random_joke_ids]
    )


@app.get("/coinflip")
def _coinflip(num: int = Query(1, ge=1, le=10000)):
    return responses.JSONResponse(
        content={
            "task": f"coinflip x {num}",
            "result": random.choices(["Heads", "Tails"], k=num),
        }
    )


@app.get("/diceroll")
def _diceroll(
    num: int = Query(1, ge=1, le=10000), sides: int = Query(6, ge=3, le=10000)
):
    return responses.JSONResponse(
        content={
            "task": f"Diceroll - d{sides} x {num}",
            "result": random.choices(range(1, sides + 1), k=num),
        }
    )

if __name__ == "__main__":
    uvicorn.run("src.main:app")
