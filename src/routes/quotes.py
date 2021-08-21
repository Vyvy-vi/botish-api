import random

from fastapi import APIRouter, Path, Query

router = APIRouter()

quotes = {
    0: ("Quotes are going through", "potato"),
    1: ("Quotes", "person"),
}


@router.get("/quotes/all")
async def all_quotes():
    return {
        "quotes": [
            {"id": q_id, "quote": quotes[q_id][0], "author": quotes[q_id][1]}
            for q_id in quotes
        ]
    }


@router.get("/quotes/{quote_id}")
async def quotes_by_id(quote_id: int = Path(..., ge=0, lt=len(quotes))):
    return {"id": quote_id, "quote": quotes[quote_id][0], "author": quotes[quote_id][1]}


@router.get("/quotes")
async def get_quotes(num: int = Query(1, ge=1, lt=len(quotes))):
    random_ids = sorted(random.sample(range(len(quotes)), num))
    return {
        "quotes": [
            {
                "id": quote_id,
                "quote": quotes[quote_id][0],
                "author": quotes[quote_id][1],
            }
            for quote_id in random_ids
        ]
    }
