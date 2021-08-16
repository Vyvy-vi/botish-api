import uvicorn
from fastapi import FastAPI, responses

# from pydantic import BaseModel
from .routes import coinflip, diceroll, jokes

app = FastAPI(
    title="heptagram-api",
    description="An API for the Heptagram Bot",
    contact={"name": "Vyvy-vi", "url": "https://github.com/Vyvy-vi"},
    license_info={
        "name": "BSD-3-Clause",
        "url": "https://github.com/Heptagram-Bot/api/blob/master/LICENSE.md",
    },
)
app.include_router(coinflip.router)
app.include_router(jokes.router)
app.include_router(diceroll.router)


@app.get("/")
async def index():
    body = "<h1>The Heptagram API</h1>"
    return responses.HTMLResponse(content=body)


if __name__ == "__main__":
    uvicorn.run("src.main:app")
