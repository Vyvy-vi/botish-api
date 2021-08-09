import random
from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/diceroll")
def roll_dice(
    num: int = Query(1, ge=1, le=10000),
    sides: int = Query(6, ge=3, le=10000)
    ):
    return {
        "task": f"diceroll - d{sides} x {num}",
        "result": random.choices(
            range(1, sides + 1),
            k = num
        )
    }

