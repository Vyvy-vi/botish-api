import random

from fastapi import APIRouter, Path, Query

router = APIRouter()

jokes = ["Jokes are going through", "hehe this is a joke", "more jokes"]


@router.get("/jokes/all")
def all_jokes():
    return {
        "jokes": [
            {"id": joke_id, "joke": jokes[joke_id]} for joke_id in range(len(jokes))
        ]
    }


@router.get("/jokes/{joke_id}")
def jokes_by_id(joke_id: int = Path(..., ge=0, le=len(jokes))):
    return {"joke": jokes[joke_id], "id": joke_id}


@router.get("/jokes")
def get_jokes(num: int = Query(1, ge=1, le=len(jokes))):
    random_ids = sorted(random.sample(range(len(jokes)), num))
    return {
        "jokes": [{"id": joke_id, "joke": jokes[joke_id]} for joke_id in random_ids]
    }
