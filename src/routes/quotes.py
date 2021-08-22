import random

from fastapi import APIRouter, Path, Query
from ..dependencies import get_json

router = APIRouter()

quotes = get_json("quotes")
print(f"Quotes - {quotes}\n")

@router.get("/quotes/all")
async def all_quotes():
    return {
        "quotes": [
            {"id": int(q_id), "quote": quotes[q_id][0], "author": quotes[q_id][1]}
            for q_id in quotes
        ]
    }


@router.get("/quotes/{quote_id}")
async def quotes_by_id(quote_id: int = Path(..., ge=0, lt=len(quotes))):
    quote_id = str(quote_id)
    return {
        "id": int(quote_id),
        "quote": quotes[quote_id][0],
        "author": quotes[quote_id][1]
    }


@router.get("/quotes")
async def get_quotes(num: int = Query(1, ge=1, lt=len(quotes))):
    random_ids = sorted(random.sample(range(len(quotes)), num))
    return {
        "quotes": [
            {
                "id": quote_id,
                "quote": quotes[str(quote_id)][0],
                "author": quotes[str(quote_id)][1],
            }
            for quote_id in random_ids
        ]
    }
