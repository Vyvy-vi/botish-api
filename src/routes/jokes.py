import random

from fastapi import APIRouter, Path, Query

from ..dependencies import get_json

router = APIRouter()

jokes = get_json("jokes")


@router.get("/jokes/all")
async def all_jokes():
    return {
        "jokes": [
            {"id": joke_id, "joke": jokes[joke_id]} for joke_id in range(len(jokes))
        ]
    }


@router.get("/jokes/{joke_id}")
async def jokes_by_id(joke_id: int = Path(..., ge=0, lt=len(jokes))):
    return {"joke": jokes[joke_id], "id": joke_id}


@router.get("/jokes")
async def get_jokes(num: int = Query(1, ge=1, lt=len(jokes))):
    random_ids = sorted(random.sample(range(len(jokes)), num))
    return {
        "jokes": [{"id": joke_id, "joke": jokes[joke_id]} for joke_id in random_ids]
    }
