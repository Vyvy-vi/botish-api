import uvicorn
import random

from typing import Optional, List, Dict
from fastapi import FastAPI, responses, HTTPException

from fastapi import Path, Query

# from pydantic import BaseModel

app = FastAPI()

jokes = [
    "Jokes are going through",
    "hehe this is a joke",
    "more jokes"
]


@app.get('/')
def index():
    body = "<h1>The Heptagram API</h1>"
    return responses.HTMLResponse(content=body)

@app.get('/jokes/{joke_id}')
def jokes_by_id(joke_id: int):
    if joke_id > len(jokes):
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": [
                    "path",
                    "joke_id"
                ],
                "msg": f"Error: joke with ID = {joke_id} not found",
                "type": "Bad Request"
            }]
        )

    return responses.JSONResponse(
        content={
            "joke": jokes[joke_id],
            "id": joke_id
        }
    )

@app.get('/jokes')
def _jokes(num: Optional[int] = None):
    if not num:
        num = len(jokes)

    if num > len(jokes):
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": [
                    "query",
                    "num"
                ],
                "msg": f"Error: the API currently stores less than {num} jokes",
                "type": "Bad Request"
            }]
        )

    random_joke_ids = sorted(random.sample(range(0, len(jokes)), num))
    return responses.JSONResponse(
        content=[
            {'id': joke_id, 'joke': jokes[joke_id]} for joke_id in random_joke_ids
        ]
    )

@app.get('/coinflip')
def _coinflip(num: int = 1):
    if num < 1:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": [
                    "query",
                    "num"
                ],
                "msg": f"Error: num should be greater than 0",
                "type": "Bad Request"
            }]
        )

    if num > 10000:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": [
                    "query",
                    "num"
                ],
                "msg": f"Error: num should be smaller than 10000",
                "type": "Bad Request"
            }]
        )

    return responses.JSONResponse(
        content={
            "task": f"coinflip x {num}",
            "result": random.choices(["Heads", "Tails"], k = num)
        }
    )

@app.get('/diceroll')
def _diceroll(num: int = 1, sides: int = 6):
    if num < 1:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": [
                    "query",
                    "num"
                ],
                "msg": "Error: num should be greater than 0",
                "type": "Bad Request"
            }]
        )
    if num > 10000:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": [
                    "query",
                    "num"
                ],
                "msg": "Error: num should be smaller than 10000",
                "type": "Bad Request"
            }]
        )
    if sides > 100 or sides < 3:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": [
                    "query",
                    "num"
                ],
                "msg": "Error: sides must be beween 3 and 100",
                "type": "Bad Request"
            }]
        )

    return responses.JSONResponse(
        content={
            "task": f"Diceroll - d{sides} x {num}",
            "result": random.choices(range(1, sides), k=num)
        }
    )



def run():
    uvicorn.run("src.main:app", reload=True)

if __name__ == '__main__':
    run()
