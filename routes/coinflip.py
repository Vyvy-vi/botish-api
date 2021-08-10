import random

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/coinflip")
def flip_coin(num: int = Query(1, ge=1, le=10000)):
    return {
        "task": f"coinflip x {num}",
        "result": random.choices(["Heads", "Tails"], k=num),
    }
