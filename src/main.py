import uvicorn
from fastapi import FastAPI, responses

from .dependencies import get_meta
from .routes import coinflip, diceroll, jokes, quotes

# from pydantic import BaseModel

META = get_meta()

app = FastAPI(
    title=META["name"],
    description=META["description"],
    contact=META["author"],
    license_info=META["license"],
    version=META["version"],
)
app.include_router(coinflip.router)
app.include_router(jokes.router)
app.include_router(diceroll.router)
app.include_router(quotes.router)


@app.get("/")
async def index():
    body = "<h1>The Heptagram API</h1>"
    return responses.HTMLResponse(content=body)


if __name__ == "__main__":
    uvicorn.run("src.main:app")
